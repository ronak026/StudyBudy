from django import forms
from django.forms import ModelForm
from .models import Login,Room,Topic,Message
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=8)
    
    class Meta:
        model = Login
        fields = ['name', 'email', 'password']

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput, max_length=8)

class RoomForm(ModelForm):
    
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','participants']
        
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email']
        
class TopicForm(ModelForm):
    
    class Meta:
        model=Topic
        fields='__all__'

