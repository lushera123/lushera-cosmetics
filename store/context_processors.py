from django.conf import settings


def store_settings(request):
    """Inject store contact/payment details into every template."""
    return {
        'STORE_EMAIL':      getattr(settings, 'STORE_EMAIL',      'contact@glowcare.com'),
        'STORE_PHONE':      getattr(settings, 'STORE_PHONE',      '+92 300 1234567'),
        'JAZZCASH_NUMBER':  getattr(settings, 'JAZZCASH_NUMBER',  '0300-1234567'),
        'EASYPAISA_NUMBER': getattr(settings, 'EASYPAISA_NUMBER', '0300-1234567'),
    }
