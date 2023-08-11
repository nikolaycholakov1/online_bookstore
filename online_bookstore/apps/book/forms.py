# forms.py

# Import statements for forms
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError

# Importing model classes from different apps
from online_bookstore.apps.book.models import BookReview, Customer, Book
from online_bookstore.apps.store.models import Order


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

    def __init__(self, *args, **kwargs):
        self.review_id = kwargs.pop('review_id', None)
        super().__init__(*args, **kwargs)
        if self.review_id:
            self.fields['review_id'] = forms.IntegerField(
                initial=self.review_id,
                widget=forms.HiddenInput()
            )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'email', 'age', 'profile_picture', 'delivery_address']
        widgets = {
            'delivery_address': forms.Textarea(
                attrs={'rows': 3, 'placeholder': 'Enter your delivery address'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']

        if not all(char.isalpha() or char.isspace() for char in username):
            raise ValidationError('Username can only contain letters and whitespace.')

        return username

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']

        if not all(char.isalpha() or char.isspace() for char in first_name):
            raise ValidationError('First name can only contain letters and whitespace.')

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']

        if not all(char.isalpha() or char.isspace() for char in last_name):
            raise ValidationError('Last name can only contain letters and whitespace.')

        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']

        return email

    def clean_delivery_address(self):
        delivery_address = self.cleaned_data['delivery_address']

        if delivery_address:
            length = len(delivery_address)
            if length < Customer.DELIVERY_ADDRESS_MIN_LEN or length > Customer.DELIVERY_ADDRESS_MAX_LEN:
                raise ValidationError(
                    f'Delivery address must be between {Customer.DELIVERY_ADDRESS_MIN_LEN} and {Customer.DELIVERY_ADDRESS_MAX_LEN} characters long.'
                )

        return delivery_address


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current Password'}),
        label="Current Password",
        required=True
    )

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
        label="New Password",
        required=True
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
        label="Confirm New Password",
        required=True
    )

    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']


class BookPublishForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'cols': 32, 'rows': 7}),
        }


class OrderUpdateForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=Order.ORDER_STATUS
    )

    class Meta:
        model = Order
        fields = ['status']
