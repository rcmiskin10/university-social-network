from django import forms
from .models import Member, Frat
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class FratForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ['user', 'frat_id']


class AddFratForm(forms.ModelForm):
    def __init__(self, data=None, files=None, **kwargs):
        super(AddFratForm, self).__init__(data, files, kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.add_input(Submit('submit', 'Add Fraternity/Sorority', css_class='btn btn-primary'))
        
    name = forms.CharField(label='',
                            widget=forms.TextInput( attrs={'placeholder': 'Fraternit/Sorority Name'} ))
    description = forms.CharField(label='',
                            widget=forms.TextInput( attrs={'placeholder': 'Description of fraternity/sorority'} ))
    class Meta:
        model = Frat
        fields = ['logo', 'frat_or_sorority', 'name', 'description']