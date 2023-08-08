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

    name_validators = [
        validators.MinLengthValidator(NAME_MIN_LEN),
        validate_letters_only,
    ]

    country_city_validators = {
        'country': [
            validators.MinLengthValidator(SHIPPING_COUNTRY_MIN_LEN)
        ],
        'city': [
            validators.MinLengthValidator(SHIPPING_CITY_MIN_LEN)
        ]
    }

    shipping_full_name = forms.CharField(
        label='Full Name',
        max_length=NAME_MAX_LEN,
        validators=name_validators,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Doe'}),
    )

    shipping_email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@email.com'})
    )

    shipping_country = forms.CharField(
        label='Country',
        max_length=SHIPPING_COUNTRY_MAX_LEN,
        validators=country_city_validators['country'],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    shipping_city = forms.CharField(
        label='City',
        max_length=SHIPPING_CITY_MAX_LEN, validators=country_city_validators['city'],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    shipping_address = forms.CharField(
        label='Address',
        max_length=SHIPPING_ADDRESS_MAX_LEN,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234 Elm Street'}),
    )

    shipping_zipcode = forms.IntegerField(
        label='Zip Code',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345'}),
    )

    payment_method = forms.ChoiceField(
        label='Payment Method',
        choices=(
            ('debit_card', 'Debit Card'),
            ('credit_card', 'Credit Card'),
            ('paypal', 'PayPal'),
            ('bank_transfer', 'Bank Transfer'),
        )
    )
