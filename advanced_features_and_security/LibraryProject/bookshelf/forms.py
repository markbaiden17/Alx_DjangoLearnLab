from django import forms

class ExampleForm(forms.Form):
    """
    An example form used to demonstrate secure data handling.
    Django forms automatically provide protection against 
    several types of attacks by validating user input.
    """
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)