from django import forms
from .models import Reseña
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import Profile

class ReseñaForm(forms.ModelForm):
    class Meta:
        model = Reseña
        fields = ['nombre', 'correo', 'ciudad_visitada', 'comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 4}),
        }
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image'] 
        
        
