from django import forms
from .models import Emergencia

class NuevaEmergenciaForm(forms.ModelForm):
    class Meta:
        model = Emergencia
        fields = ['emerg_desc', 'emerg_color', 'emerg_fecha', 'emerg_pac_id', 'emerg_doc_id']
