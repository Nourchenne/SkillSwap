from django import forms
from .models import Exchange


class ExchangeProposalForm(forms.ModelForm):
    """Form for proposing an exchange"""
    class Meta:
        model = Exchange
        fields = ['scheduled_datetime', 'notes']
        widgets = {
            'scheduled_datetime': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
            'notes': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Any questions or special requests?'
                }
            ),
        }
        help_texts = {
            'scheduled_datetime': 'Propose a time (can be adjusted later)',
        }
