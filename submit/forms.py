from django import forms

from submit.models import Submit


class TaskSubmitForm(forms.Form):
    submit_file = forms.FileField(max_length=100000)
    language = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Jazyk',
        choices=Submit.LANGUAGE_CHOICES
    )
