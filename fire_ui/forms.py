from django import forms
from .models import FocosDeQueimada

class FocosDeQueimadaForm(forms.ModelForm):
    class Meta:
        model = FocosDeQueimada
        fields = '__all__'  # Ou liste os campos específicos que você quer incluir
        widgets = {
            # Adicione widgets personalizados para cada campo conforme necessário
            # Por exemplo:
            # 'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
