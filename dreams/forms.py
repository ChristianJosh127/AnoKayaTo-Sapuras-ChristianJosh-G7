from django import forms
from .models import DreamEntry


class DreamEntryForm(forms.ModelForm):
    class Meta:
        model = DreamEntry
        fields = ['title', 'dream_text', 'dream_date', 'symbols']

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Give your dream a title',
            }),
            'dream_text': forms.Textarea(attrs={
                'placeholder': 'Describe what happened in your dream...',
                'rows': 6,
            }),
            'dream_date': forms.DateInput(attrs={
                'type': 'date',
            }),
            'symbols': forms.CheckboxSelectMultiple(),
        }

    def clean_dream_text(self):
        dream_text = self.cleaned_data.get('dream_text')

        if not dream_text or not dream_text.strip():
            raise forms.ValidationError(
                'Please enter a description of your dream.'
            )

        return dream_text.strip()