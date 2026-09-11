from django import forms
from .models import Order, PAYMENT_METHOD_CHOICES


class CheckoutForm(forms.ModelForm):
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.RadioSelect,
        initial='cod',
    )
    transaction_id = forms.CharField(
        required=False,
        max_length=100,
        label='Transaction ID',
        help_text='Required for JazzCash / EasyPaisa — enter the transaction ID after payment.',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. TXN123456789'}),
    )

    class Meta:
        model = Order
        fields = [
            'full_name', 'email', 'phone',
            'address', 'city', 'postal_code',
            'payment_method', 'transaction_id', 'notes',
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'notes':   forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Any special delivery instructions? (optional)',
            }),
        }
        labels = {
            'notes': 'Delivery Notes (optional)',
        }
