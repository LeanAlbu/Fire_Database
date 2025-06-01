
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *

class RegiaoImediataForm(forms.ModelForm):
    class Meta:
        model = RegiaoImediata
        fields = '__all__'

class MunicipioForm(forms.ModelForm):
    class Meta:
        model = Municipio
        fields = '__all__'

class SateliteForm(forms.ModelForm):
    class Meta:
        model = Satelite
        fields = ['nome_satelite', 'pais_origem', 'tipo_orbita']
        
        widgets = {
            'nome_satelite': forms.TextInput(attrs={'class': 'form-control'}),
            'pais_origem': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_orbita': forms.Select(attrs={'class': 'form-select'}),
        }




class FocoQueimadaForm(forms.ModelForm):
    satelites = forms.ModelMultipleChoiceField(
        queryset=Satelite.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Satélites"
    )

    class Meta:
        model = FocoQueimada
        fields = '__all__'
        widgets = {
            'data_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_municipio'].queryset = Municipio.objects.all()
        self.fields['satelites'].queryset = Satelite.objects.all()



class SateliteQueimadaForm(forms.ModelForm):
    class Meta:
        model = SateliteQueimada
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id_password'})
    )

