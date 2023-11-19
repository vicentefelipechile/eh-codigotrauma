from django import forms
from .models import Emergencia, Paciente

class NuevaEmergenciaForm(forms.ModelForm):
    class Meta:
        model = Emergencia
        fields = ['emerg_desc', 'emerg_color', 'emerg_fecha', 'emerg_pac_id', 'emerg_doc_id']

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['pac_rut','pac_dv', 'pac_nacimiento','pac_primernombre', 'pac_segundonombre', 'pac_apellidopaterno', 'pac_apellidomaterno', 'pac_direccion', 'pac_ciudad']