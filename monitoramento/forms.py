from django import forms
from .models import Acao

class AcaoForm(forms.ModelForm):
    class Meta:
        model = Acao
        fields = ["symbol", "monitor_price", "recent_price", "monitor_type"]
        


