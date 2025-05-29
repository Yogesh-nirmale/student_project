from django import forms
from django.forms import widgets
from .models import *
from django.contrib.auth.forms import UserCreationForm  # ✅


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'description']

    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), help_text="Enter a detailed description.")

class DateInput(forms.DateInput):
    input_type = 'date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due': DateInput()}
        fields = ['subject', 'title', 'description', 'due', 'is_finished']
    
    def clean_is_finished(self):
        is_finished = self.cleaned_data.get('is_finished')
        if not isinstance(is_finished, bool):
            raise forms.ValidationError('This field must be a boolean value (True or False).')
        return is_finished

class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100, label="Enter YouTube Search:")

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text) < 3:
            raise forms.ValidationError("Search term must be at least 3 characters.")
        return text

class TodoForm(forms.ModelForm):  # Fixed typo here
    class Meta:
        model = Todo
        fields = ['title', 'is_finished']
        help_texts = {
            'title': 'Enter the title of the task.',
        }

    title = forms.CharField(max_length=200, help_text="Enter the title of the task.")

    # Custom validation for the 'title' field to ensure it's not too short
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']