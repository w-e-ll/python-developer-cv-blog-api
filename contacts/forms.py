from django import forms
from phonenumber_field.formfields import PhoneNumberField
# How long the length of the textarea should be.
MAX_LENGTH_TEXTAREA = 120


class ContactForm(forms.Form):

    name_cst = {
        'placeholder': 'Enter your name.',
        'class': 'form-control cst__radius',
        'maxlength': '120',
        'autocomplete': 'off',
        'type': 'text'
    }
    email_cst = {
        'placeholder': 'A valid email address, please.',
        'class': 'form-control cst__radius',
        'maxlength': '120',
        'autocomplete': 'off',
        'type': 'text'
    }
    phone_cst = {
        'placeholder': 'Phone * (With country code)',
        'class': 'form-control cst__radius',
        'maxlength': '120',
        'autocomplete': 'off',
        'type': 'text'
    }
    company_cst = {
        'placeholder': 'Company',
        'class': 'form-control cst__radius',
        'maxlength': '120',
        'autocomplete': 'off',
        'type': 'text'
    }
    url_cst = {
        'placeholder': 'Your Web site',
        'class': 'form-control cst__radius',
        'maxlength': '120',
        'autocomplete': 'off',
        'type': 'text'
    }
    subject_cst = {
        'placeholder': 'Enter your subject.',
        'class': 'form-control cst__radius',
        'maxlength': '120',
        'autocomplete': 'off',
        'type': 'text'
    }
    message_cst = {
        'placeholder': 'Enter your message here.',
        'class': 'form-control cst__radius',
        'maxlength': '256',
        'autocomplete': 'off',
        'type': 'text'
    }

    name = forms.CharField(required=True, widget=forms.TextInput(attrs=name_cst))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs=email_cst))
    phone = PhoneNumberField(required=False, widget=forms.TextInput(attrs=phone_cst))
    company = forms.CharField(required=False, widget=forms.TextInput(attrs=company_cst))
    url = forms.URLField(required=False, widget=forms.TextInput(attrs=url_cst))
    subject = forms.CharField(required=True, widget=forms.TextInput(attrs=subject_cst))
    message = forms.CharField(required=True, widget=forms.Textarea(attrs=message_cst))
