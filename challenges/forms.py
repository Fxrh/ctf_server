from django import forms
from challenges.models import ChallengeCategory

class InfoForm(forms.Form):
    try_solution = forms.CharField(max_length=200, label='Enter solution')

class CreateChallengeForm(forms.Form):
    challenge_name = forms.CharField(label='Challenge Name', max_length=40)
    category = forms.ModelChoiceField(queryset=ChallengeCategory.objects.all(),
                                      label='Category')

#class CreateForm(forms.Form):
#    challenge_name = forms.CharField(label='Challenge Name', max_length=100)
