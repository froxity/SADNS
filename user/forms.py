from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 
        'password1', 'password2']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }
    
    #Modify the attribute to the sync with CSS stylesheet
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control','id': 'floatingInput', 'placeholder': 'placeholder'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'username', 
        'phone_no']

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone_no': 'Phone number (optional)',
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})