from django import forms
from .models import Task, TaskPhoto, User
from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

class TaskPhotoForm(forms.ModelForm):
    class Meta:
        model = TaskPhoto
        fields = ['photo']
