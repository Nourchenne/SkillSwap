from django import forms
from decimal import Decimal, InvalidOperation
from .models import SkillOffer, SkillRequest


class SkillOfferForm(forms.ModelForm):
    """Form for creating skill offers"""
    # Accept comma or dot as decimal separator for duration
    duration_hours = forms.CharField()

    class Meta:
        model = SkillOffer
        fields = [
            'title', 'description', 'category', 'delivery_method',
            'session_type', 'max_group_size', 'duration_hours', 'skill_level'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        help_texts = {
            'duration_hours': 'Typical session length (determines credits)',
            'max_group_size': 'Maximum number of learners per session',
        }

    def clean_duration_hours(self):
        raw = self.cleaned_data.get('duration_hours', '')
        s = str(raw).replace(',', '.')
        try:
            value = Decimal(s)
        except InvalidOperation:
            raise forms.ValidationError('Please enter a valid number (e.g., 1.5).')
        if value < Decimal('0.5'):
            raise forms.ValidationError('Minimum duration is 0.5 hour.')
        # limit to one decimal place
        return value.quantize(Decimal('0.1'))


class SkillRequestForm(forms.ModelForm):
    """Form for posting skill learning requests"""
    class Meta:
        model = SkillRequest
        fields = ['title', 'description', 'category', 'preferred_delivery', 'urgency']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class SkillSearchForm(forms.Form):
    """Form for searching and filtering skills"""
    search = forms.CharField(required=False, max_length=100)
    category = forms.CharField(required=False, max_length=50)
    delivery = forms.ChoiceField(
        required=False,
        choices=[('', 'Any')] + SkillOffer.DELIVERY_CHOICES
    )
    city = forms.CharField(required=False, max_length=100)
