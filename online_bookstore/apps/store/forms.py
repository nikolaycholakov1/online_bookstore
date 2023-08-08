# store/forms.py

from django import forms
from django.core import validators

from validators import validate_letters_only


class CheckoutForm(forms.Form):
    NAME_MAX_LEN = 30
    NAME_MIN_LEN = 2

    SHIPPING_COUNTRY_MAX_LEN = 100
    SHIPPING_COUNTRY_MIN_LEN = 4
    SHIPPING_CITY_MAX_LEN = 100
    SHIPPING_CITY_MIN_LEN = 2
    SHIPPING_ADDRESS_MAX_LEN = 200

    shipping_full_name = forms.CharField(
        max_length=NAME_MAX_LEN, validators=[
            validators.MinLengthValidator(NAME_MIN_LEN),
            validate_letters_only,
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'}),

    )
    shipping_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    shipping_country = forms.CharField(
        max_length=SHIPPING_COUNTRY_MAX_LEN,
        validators=[
            validators.MinLengthValidator(SHIPPING_COUNTRY_MIN_LEN)
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    shipping_city = forms.CharField(
        max_length=SHIPPING_CITY_MAX_LEN,
        validators=[
            validators.MinLengthValidator(SHIPPING_CITY_MIN_LEN)
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    shipping_address = forms.CharField(
        max_length=SHIPPING_ADDRESS_MAX_LEN,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    shipping_zipcode = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    payment_method = forms.ChoiceField(label='Payment Method', choices=(
        ('debit_card', 'Debit Card'),
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    ))
