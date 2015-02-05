from django import forms
from challenges.models import ChallengeCategory, Challenge, User


class InfoForm(forms.Form):
    try_solution = forms.CharField(max_length=200, label='Enter solution')


class CreateChallengeForm(forms.Form):
    challenge_name = forms.CharField(label='Challenge Name', max_length=40)
    category = forms.ModelChoiceField(queryset=ChallengeCategory.objects.all(),
                                      label='Category')


class EditChallengeForm(forms.ModelForm):
    points = forms.IntegerField(max_value=500, min_value=0, label='Points')

    class Meta:
        model = Challenge
        fields = ['category', 'solution', 'points', 'description', 'is_published']

    # category = forms.ModelChoiceField(queryset=ChallengeCategory.objects.all(),
    #                                   label='Category')
    # solution = forms.CharField(max_length=200, label='Solution')
    # points = forms.IntegerField(max_value=500, min_value=0, label='Points')
    # description = forms.CharField(label='Description')
    # is_published = forms.BooleanField(label='Publish')


class EditAccountForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['ssh_key']

