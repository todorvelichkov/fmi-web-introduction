from django import forms
from calc.models import CalcResult

class CalcForm(forms.ModelForm):
    # x = forms.IntegerField(label='x value')
    # operation = forms.ChoiceField(choices=[
    #     ('add', 'Add'),
    #     ('substract', 'Substract'),
    # ])
    # y = forms.IntegerField(label='y value')

    class Meta:
        model = CalcResult
        fields = ['x', 'operation', 'y']
