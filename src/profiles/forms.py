from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import ProfileInfo, UserPicture, Post, Bio, Work, Interest


class ProfileInfoForm(forms.ModelForm):
    major = forms.CharField(label="",required=False,
                               widget=forms.TextInput(attrs={'size':'70', 'placeholder': 'Major'}))
    minor = forms.CharField(label="",required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'Minor'}))
    loc_from = forms.CharField(label="",required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'Where are you from?'}))
    class Meta:
        model = ProfileInfo
        exclude=['user']
        
    def __init__(self, data=None, files=None, **kwargs):
        super(ProfileInfoForm, self).__init__(data, files, **kwargs)
        self.fields["year"].choices = [("", "Graduating Class"),] + list(self.fields["year"].choices)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_show_errors = False
        self.helper.add_input(Submit('submit', 'Save', css_class='btn btn-primary btn-lg'))

class BioForm(forms.ModelForm):
    
    bio = forms.CharField(label="", required=False,
                               widget=forms.Textarea(attrs={'placeholder': 'Say something about yourself...'}))
    class Meta:
        model = Bio
        exclude=['user']
        
    def __init__(self, data=None, files=None, **kwargs):
        super(BioForm, self).__init__(data, files, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_show_errors = False
        self.helper.add_input(Submit('submit', 'Save', css_class='btn btn-primary btn-lg'))

class UserPictureForm(forms.ModelForm):
    
    class Meta:
        model = UserPicture
        exclude=['user']
    
    def __init__(self, data=None, files=None, **kwargs):
        super(UserPictureForm, self).__init__(data, files, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_show_errors = True
        self.helper.add_input(Submit('submit', 'Save', css_class='btn btn-primary btn-lg'))
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # exclude = ['author', 'updated', 'created', ]
        fields = ['text']



class WorkForm(forms.ModelForm):
    position = forms.CharField(label="",
                               widget=forms.TextInput(attrs={'placeholder': 'Position.'}))
    company = forms.CharField(label="",
                               widget=forms.TextInput(attrs={'placeholder': 'Company.'}))
    location = forms.CharField(label="",
                               widget=forms.TextInput(attrs={'placeholder': 'Location.'}))
    start_date = forms.DateField(label="",
        widget=forms.DateInput(attrs={"class":"datepicker","placeholder":"Start Date.", "cols":3,})
    )
    end_date = forms.DateField(label="",
        widget=forms.DateInput(attrs={"class":"datepicker","placeholder":"End Date.", "cols":3,})
    )
    class Meta:
        model = Work
        exclude=['user']

class InterestForm(forms.ModelForm):
    interest = forms.CharField(label="",
                               widget=forms.TextInput(attrs={'placeholder': 'Interest.'}))
    
    class Meta:
        model = Interest
        exclude=['user']
        
    
