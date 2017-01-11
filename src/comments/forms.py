from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from .models import MyPost

HOUR_CHOICES = (
        ('12AM','12AM'),
        ('1AM','1AM'),
        ('2AM','2AM'),
        ('3AM','3AM'),
        ('4AM','4AM'),
        ('5AM','5AM'),
        ('6AM','6AM'),
        ('7AM','7AM'),
        ('8AM','8AM'),
        ('9AM','9AM'),
        ('10AM','10AM'),
        ('11AM','11AM'),
        ('12PM','12PM'),
        ('1PM','1PM'),
        ('2PM','2PM'),
        ('3PM','3PM'),
        ('4PM','4PM'),
        ('5PM','5PM'),
        ('6PM','6PM'),
        ('7PM','7PM'),
        ('8PM','8PM'),
        ('9PM','9PM'),
        ('10PM','10PM'),
        ('11PM','11PM'),
        
    )

class ReplyForm(forms.Form):
    mypost = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder":"Post on the profile.","rows":1, "cols":12})
        )
    
class MyPostForm(forms.Form):
    mypost = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder":"Post on the profile.","rows":1, "cols":12})
        )
    user = forms.CharField(
        widget=forms.HiddenInput(), required=False
    )
    path = forms.CharField(
        widget=forms.HiddenInput(), required=False
    )
    parent = forms.CharField(
        widget=forms.HiddenInput(), required=False
    )
    def __init__(self, data=None, files=None, **kwargs):
        super(MyPostForm, self).__init__(data, files, kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('mypost', id="post-text"),
            Field('user', id="post-user"),
            Field('path', id="post-path"),
            Field('parent', id="post-parent"),
            )
       
        

class LinkMyPostForm(forms.Form):
    mypost = forms.CharField(required=True,
        widget=forms.Textarea(attrs={"placeholder":"Post on the profile.","rows":1, "cols":12})
        )
    link = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder":"Post a YouTube link.","rows":1, "cols":12})
    )
    

    def clean_link(self):
        data = self.cleaned_data['link']
        if 'https://www.youtube.com/watch?v=' not in data:
            raise forms.ValidationError("Must be a Youtube link")
        return data

        
    def __init__(self, data=None, files=None, **kwargs):
        super(LinkMyPostForm, self).__init__(data, files, kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.add_input(Submit('submit', 'Add Post', css_class='btn btn-primary'))
        
                        

class ImageMyPostForm(forms.Form):
    mypost = forms.CharField(required=True,
        widget=forms.Textarea(attrs={"placeholder":"Post on the profile.","rows":1, "cols":12})
        )
    image = forms.ImageField()
    

    def __init__(self, data=None, files=None, **kwargs):
        super(ImageMyPostForm, self).__init__(data, files, kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.add_input(Submit('submit', 'Add Post', css_class='btn btn-primary'))

class EventForm(forms.Form):
    mypost = forms.CharField(required=True,
        widget=forms.Textarea(attrs={"placeholder":"Describe the event","rows":1, "cols":12})
        )
    event = forms.CharField(max_length=20,required=True,
                widget=forms.Select(choices=MyPost.EVENT_CHOICES))
    date = forms.DateField(label='', required=True,
                            widget=forms.DateInput(attrs={'class':'datepicker','placeholder':'Pick a date.'}))
    start_time = forms.ChoiceField(choices = HOUR_CHOICES, label="", initial='', widget=forms.Select(), required=True)
    end_time = forms.ChoiceField(choices = HOUR_CHOICES, label="", initial='', widget=forms.Select(), required=True)

    def __init__(self, data=None, files=None, **kwargs):
        super(EventForm, self).__init__(data, files, kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.add_input(Submit('submit', 'Add Event', css_class='btn btn-primary'))
        self.fields["start_time"].choices = [("", "Pick a start time."),] + list(self.fields["start_time"].choices)[1:]
        self.fields["end_time"].choices = [("", "Pick an end time."),] + list(self.fields["end_time"].choices)[1:]
        