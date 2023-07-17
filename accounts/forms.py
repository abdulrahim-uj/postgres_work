from django import forms
from .models import User, UserProfile
from django.utils.translation import gettext_lazy as _
from django.forms import TextInput, NumberInput, EmailField, PasswordInput


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password',
                                                                 'class': 'required form-control form-control-lg'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password',
                                                                         'class': 'required form-control form-control-lg'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'Enter first name',
                                           'class': 'required form-control form-control-lg'}),
            'last_name': TextInput(attrs={'placeholder': 'Enter last name',
                                          'class': 'required form-control form-control-lg'}),
            'username': TextInput(attrs={'placeholder': 'Enter username',
                                         'class': 'required form-control form-control-lg'}),
            # 'email': EmailField(),
        }
        error_messages = {
            'first_name': {
                'required': _("This field is required"),
            },
            'last_name': {
                'required': _("This field is required"),
            },
            'username': {
                'required': _("This field is required"),
            },
            'email': {
                'required': _("This field is required"),
            },
            'password': {
                'required': _("This field is required"),
            },
        }
        labels = {
            "first_name": "First name",
            "email": "E-mail",
            "password": "Password",
        }

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password does not  match!")


country_list = (
    ('', '-- Please select one country --'),
    ('IN', 'India'),
    ('US', 'United States'),
    ('CA', 'Canada'),
    ('UK', 'United Kingdom'),
    ('AU', 'Australia'),
    ('UAE', 'United Arab Emirates'),
)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']
        fields = ['address', 'country_code', 'country',
                  'state', 'city', 'district', 'pin_code', 'landmark']
        widgets = {
            'address': TextInput(attrs={'placeholder': 'Enter address',
                                        'class': 'required form-control form-control-lg'}),
            'country_code': TextInput(attrs={'placeholder': 'Enter country code',
                                             'class': 'required form-control form-control-lg'}),
            'country':  forms.Select(choices=country_list),
            'state': TextInput(attrs={'placeholder': 'Enter state',
                                      'class': 'required form-control form-control-lg'}),
            'city': TextInput(attrs={'placeholder': 'Enter city',
                                     'class': 'required form-control form-control-lg'}),
            'district': TextInput(attrs={'placeholder': 'Enter district',
                                         'class': 'required form-control form-control-lg'}),
            'pin_code': NumberInput(attrs={'placeholder': 'Enter pincode',
                                           'class': 'required form-control form-control-lg'}),
            'landmark': TextInput(attrs={'placeholder': 'Enter nearest landmark',
                                         'class': 'required form-control form-control-lg'}),
        }
        labels = {
            'address': "Address",
            'country_code': "Country code",
            'country': "Country",
            'state': "State",
            'city': "City",
            'district': "District",
            'pin_code': "Zip Code",
            'landmark': "Landmark",
        }
        error_messages = {
            'address': {
                'required': _("This field is required"),
            },
            'country': {
                'required': _("This field is required"),
            },
            'state': {
                'required': _("This field is required"),
            },
            'city': {
                'required': _("This field is required"),
            },
            'pin_code': {
                'required': _("This field is required"),
            },
            'landmark': {
                'required': _("This field is required"),
            },
        }
