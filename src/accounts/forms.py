from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import MyUser


class RegistrationForm(forms.Form):
    
    email = forms.EmailField(label="",
                            required=True,
                            widget=forms.TextInput(attrs={'placeholder': 'E-mail address'}))
    username = forms.CharField(label="",
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Username'}))

    first_name = forms.CharField(label="",
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(label="",
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    password1 = forms.CharField(label="",
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label="",
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password confirmation'}))
    
    def __init__(self, data=None, files=None, **kwargs):
        super(RegistrationForm, self).__init__(data, files, kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_show_errors = True
        self.helper.add_input(Submit('submit', 'Register', css_class='btn btn-primary btn-lg'))
        
        
    
    #clean email
    def clean_email(self):
        data = self.cleaned_data['email']
        
        if MyUser.objects.filter(email=data).exists():
            raise forms.ValidationError("%s is already in use." %(data))
        if "@brandeis.edu" not in data:   # any check you need
            raise forms.ValidationError("Must be a Brandeis address")
        return data

    def clean_username(self):
        data = self.cleaned_data['username']
        
        if MyUser.objects.filter(username=data).exists():
            raise forms.ValidationError("%s is already in use." %(data))
        return data
        

    #clean password
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        if len(password1) <= 5:
            raise forms.ValidationError("Password is too short.")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2
    
    #modify save() method so that we can set user.is_active to False when we first create our user
    def save(self, commit=True):        
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.is_active = False # not active until he opens activation link
            user.save()
        return user
    
    

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ( 'email', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'first_name', 'last_name', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
