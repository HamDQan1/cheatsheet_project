from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title']
        labels = {'title': 'Topic Title'}
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g., Python Basics'})
        }

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'summary', 'content']
        labels = {
            'title': 'Entry Title',
            'summary': 'Summary (Front of Flashcard)',
            'content': 'Details (Back of Flashcard)'
        }
        widgets = {
            'summary': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Quick summary or key points (supports Markdown)...'
            }),
            'content': forms.Textarea(attrs={
                'rows': 10, 
                'placeholder': 'Detailed explanation, code examples, etc. (supports Markdown)...'
            }),
        }