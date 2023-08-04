# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from online_bookstore.apps.book.models import BookReview, Customer, Book, DeliveryAddress


class RegistrationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username', 'email', 'password1', 'password2']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['review_text']
        labels = {
            'review_text': 'Write your review here:'
        }
        widgets = {
            'review_text': forms.Textarea(attrs={'style': 'min-width: 0;'}),
        }


class OrderForm(forms.Form):
    pk = forms.IntegerField(widget=forms.HiddenInput)
    quantity = forms.IntegerField(initial=1)
    delivery_address = forms.CharField(widget=forms.TextInput(attrs={'required': True}))
    city = forms.CharField(widget=forms.TextInput(attrs={'required': True}))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={'required': True}))


class ShippingInfoForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = ['country', 'city', 'address', 'zip_code', 'shipping_method']

    def __init__(self, *args, **kwargs):
        super(ShippingInfoForm, self).__init__(*args, **kwargs)

        labels = {
            'country': 'Country',
            'city': 'City',
            'address': 'Address',
            'zip_code': 'ZIP Code',
            'shipping_method': 'Shipping Method',
        }

        for field_name, label in labels.items():
            self.fields[field_name].label = label

        widget_placeholders = {
            'country': 'Enter your Country',
            'address': 'Enter your address',
            'city': 'Enter your city',
            'zip_code': 'Enter your ZIP code',
            'shipping_method': 'Enter your Shipping Method',
        }

        for field_name, placeholder in widget_placeholders.items():
            self.fields[field_name].widget.attrs['placeholder'] = placeholder


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'age', 'profile_picture', 'delivery_address']
        widgets = {
            'delivery_address': forms.Textarea(attrs={'rows': 3, 'cols': 32}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']

        if not all(char.isalpha() or char.isspace() for char in name):
            raise ValidationError('Name can only contain letters and whitespace.')
        if len(name) < Customer.NAME_MIN_LEN or len(name) > Customer.NAME_MAX_LEN:
            raise ValidationError(
                f'Name must be between {Customer.NAME_MIN_LEN} and {Customer.NAME_MAX_LEN} characters.')
        return name

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('.com'):
            raise ValidationError('Invalid email format. Please use an email ending with @example.com.')
        return email

    def clean_age(self):
        age = self.cleaned_data['age']
        if age is not None and (age < Customer.MIN_AGE_VALUE or age > Customer.MAX_AGE_VALUE):
            raise ValidationError('Age cannot be 0, lower than 0, or higher than 150.')
        return age

    def clean_delivery_address(self):
        delivery_address = self.cleaned_data['delivery_address']
        if len(delivery_address) < Customer.DELIVERY_ADDRESS_MIN_LEN:
            raise ValidationError(
                f'Delivery address must be at least {Customer.DELIVERY_ADDRESS_MIN_LEN} characters.')
        return delivery_address


class BookPublishForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'cols': 32, 'rows': 7}),
        }
