from django import forms
from functools import partial
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms import layout
from crispy_forms.bootstrap import AppendedText
  


from .models import TeamSchedule

class TeamScheduleForm(forms.Form):
    
    
    
    text = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder":"Schedule name", "cols":3})
        )
    duedate = forms.DateField(
        widget=forms.DateInput(attrs={"class":"datepicker","placeholder":"e.g. 2015-06-24", "cols":3,})
    )
    
    def __init__(self, data=None, files=None, **kwargs):
        super(TeamScheduleForm, self).__init__(data, files, kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.add_input(Submit('submit', 'Add', css_class='btn btn-primary'))