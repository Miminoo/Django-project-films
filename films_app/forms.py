from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import *
from django.core.exceptions import ValidationError

class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_janr'].empty_label = 'Жанр не выбран'
        self.fields['name'].empty_label = 'Название фильма не введено'

    class Meta:
        model = Film
        fields = ['id_janr','name', 'slug', 'photo', 'years', 'country', 'discription', 'is_published']
        widgets = {
            'discription':forms.Textarea(attrs={'cols':100,'rows':10}),
        }
        
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name)<10:
            raise ValidationError('Длина превышает 200 символов')

        return name

class EditPostForm(forms.ModelForm):
    
    class Meta:
        model = Film
        fields = ['id_janr','name', 'slug', 'photo', 'years', 'country', 'discription', 'is_published']

class AddtoFavour(forms.ModelForm):
    class Meta:
        model = Film_to_user
        fields='__all__'

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
    #
