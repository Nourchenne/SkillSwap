from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """Form for leaving reviews"""
    class Meta:
        model = Review
        fields = ['rating', 'skill_quality', 'communication', 'reliability', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
            'skill_quality': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
            'communication': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
            'reliability': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'rating': 'Overall Rating',
            'skill_quality': 'Skill Quality',
            'communication': 'Communication',
            'reliability': 'Reliability',
            'comment': 'Your Review (optional)',
        }

