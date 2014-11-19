from django import forms

class InfoForm(forms.Form):
    try_solution = forms.CharField(max_length=200, label='Enter solution')

#class CreateForm(forms.Form):
#    challenge_name = forms.CharField(label='Challenge Name', max_length=100)
