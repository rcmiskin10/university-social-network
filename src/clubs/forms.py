from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import ClubMember, Club

class ClubForm(forms.ModelForm):
    class Meta:
        model = ClubMember
        exclude = ['user', 'club_id']

class AddClubForm(forms.ModelForm):
    def __init__(self, data=None, files=None, **kwargs):
        super(AddClubForm, self).__init__(data, files, kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.add_input(Submit('submit', 'Add Club', css_class='btn btn-primary'))
        
    club_name = forms.CharField(label='',
                            widget=forms.TextInput( attrs={'placeholder': 'Club Name'} ))
    description = forms.CharField(label='',
                            widget=forms.TextInput( attrs={'placeholder': 'Description of Club'} ))
    class Meta:
        model = Club
        fields = ['logo','club_name', 'description']