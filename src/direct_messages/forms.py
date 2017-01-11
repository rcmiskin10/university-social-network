from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import DirectMessage

class ComposeForm(forms.ModelForm):
    def __init__(self, data=None, files=None, **kwargs):
        super(ComposeForm, self).__init__(data, files, kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.add_input(Submit('submit', 'Send Message', css_class='btn btn-primary'))
    class Meta:
        model = DirectMessage
        fields = ('subject', 'body')
        widgets = {
            'body': forms.Textarea(attrs={'cols':40, 'rows':5, 'placeholder': 'Enter message here!'}),
            'subject': forms.TextInput(attrs={'cols':20, 'rows':1, 'placeholder': 'Subject'})
        }
        
class ProductComposeForm(forms.ModelForm):
    def __init__(self, data=None, files=None, **kwargs):
        super(ProductComposeForm, self).__init__(data, files, kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.add_input(Submit('submit', 'Send Message', css_class='btn btn-primary'))
    class Meta:
        model = DirectMessage
        fields = ( 'subject', 'body')
        widgets = {
            'body': forms.Textarea(attrs={'cols':40, 'rows':5, 'placeholder': 'Enter message here!'}),
            'subject': forms.TextInput(attrs={'cols':20, 'rows':1, 'placeholder': 'Subject'})
        }

class ReplyForm(forms.ModelForm):
    def __init__(self, data=None, files=None, **kwargs):
        super(ReplyForm, self).__init__(data, files, kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.add_input(Submit('submit', 'Send Message', css_class='btn btn-primary'))
    class Meta:
        model = DirectMessage
        fields = {'body'}
        widgets = {
            'body': forms.Textarea(attrs={'cols':40, 'rows':5, 'placeholder': 'Enter message here!'}),
            
        }