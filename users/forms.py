from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

class CustomUserChangeForm(UserChangeForm):
    """Form for updating user information."""
    
    password = None
    
    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'role', 'phone', 'address', 'is_active')
        field_classes = {'email': forms.EmailField}
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            
class ProfilePictureForm(forms.ModelForm):
    """Form for updating user's profile picture."""
    
    class Meta:
        model = get_user_model()
        fields = ('avatar',)
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 2 * 1024 * 1024:  # 2MB
                raise forms.ValidationError(_('Image file too large ( > 2MB )'))
            return avatar
        return None 