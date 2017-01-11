from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Product


class ProductForm(forms.ModelForm):
    def __init__(self, data=None, files=None, **kwargs):
        super(ProductForm, self).__init__(data, files, kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.add_input(Submit('submit', 'Add Product', css_class='btn btn-primary'))
     
    title = forms.CharField(label='', required=False,
                            widget=forms.TextInput( attrs={'placeholder': 'Title: 50 character limit.'} ))
    description = forms.CharField(label='', required=False,
                            widget=forms.TextInput( attrs={'placeholder': 'Description: 200 character limit.'} ))
    price = forms.CharField(label='', required=True,
                            widget=forms.TextInput( attrs={'placeholder': 'Price'} ))
    image = forms.ImageField(required=False)
    class Meta:
        model = Product
        fields = ['image', 'category', 'title', 'description', 'price']