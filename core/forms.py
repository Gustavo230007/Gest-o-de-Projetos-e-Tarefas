from django import forms
from .models import Time, Jogador
from django.core.exceptions import ValidationError

class TimeForm(forms.ModelForm):
    class Meta:
        model = Time
        fields = ['nome', 'cidade', 'data_fundacao']
        widgets = {
            'data_fundacao': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if Time.objects.filter(nome=nome).exists():
            raise ValidationError("Um time com este nome já existe.")
        return nome
    
class JogadorForm(forms.ModelForm):
    class Meta:
        model = Jogador
        fields = ['nome', 'posicao', 'idade', 'time']
    