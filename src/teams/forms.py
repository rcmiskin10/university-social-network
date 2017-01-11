from django import forms
from .models import TeamMember, Team
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class TeamForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        exclude = ['user', 'team_id']

class AddTeamForm(forms.ModelForm):
    def __init__(self, data=None, files=None, **kwargs):
        super(AddTeamForm, self).__init__(data, files, kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.add_input(Submit('submit', 'Add Team', css_class='btn btn-primary'))
        
    name = forms.CharField(label='',
                            widget=forms.TextInput( attrs={'placeholder': 'Team Name'} ))
    description = forms.CharField(label='',
                            widget=forms.TextInput( attrs={'placeholder': 'Description of Team'} ))
    class Meta:
        model = Team
        fields = ['logo', 'choice', 'name', 'description']