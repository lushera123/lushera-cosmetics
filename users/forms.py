from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Address


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address', 'profile_picture']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'phone', 'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country', 'is_default']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-rose focus:border-transparent', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-rose focus:border-transparent', 'placeholder': '+92 300 1234567'}),
            'address_line1': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-rose focus:border-transparent', 'placeholder': 'Street Address'}),
            'address_line2': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-rose focus:border-transparent', 'placeholder': 'Apartment, suite, etc. (optional)'}),
            'city': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-rose focus:border-transparent', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-rose focus:border-transparent', 'placeholder': 'State/Province (optional)'}),
            'postal_code': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-rose focus:border-transparent', 'placeholder': 'Postal Code'}),
            'country': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-rose focus:border-transparent', 'placeholder': 'Country'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-rose border-gray-300 rounded focus:ring-rose'}),
        }
