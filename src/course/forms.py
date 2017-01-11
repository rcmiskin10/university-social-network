from django import forms
from .models import StudentCourse, Syllabus, Assignment, CourseNote
from dateutil.parser import parse

class CourseForm(forms.ModelForm):
    class Meta:
        model = StudentCourse
        exclude = ['user', 'course_id']

class SyllabusForm(forms.ModelForm):
	syllabus = forms.FileField(label='',required=True, widget=forms.FileInput)
	class Meta:
		model = Syllabus
		fields=('syllabus',)

	


class AssignmentForm(forms.Form):
	due_date = forms.CharField(label="",
                                required=True,
                                widget=forms.TextInput(     # '25 October, 2006'
 attrs={'placeholder': 'Due Date of Assignment'}))
	name = forms.CharField(label="",
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Name of Assignment'}))

class CourseNoteForm(forms.ModelForm):
    
    text = forms.CharField(label="", required=True,
                               widget=forms.Textarea(attrs={'placeholder': 'Add a note to your class.'}))
    class Meta:
        model = CourseNote
        fields=['text']