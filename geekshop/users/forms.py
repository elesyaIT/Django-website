import hashlib
import random

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from django import forms

from users.models import User


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4',
                                                               'placeholder': 'Ведите имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4',
                                                              'placeholder': 'Ведите Фамилию'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control py-4',
                                                              'readonly': True}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name','age', 'image')


    # def clean_image(self):
    #     data = self.cleaned_data['image']
    #     if data.size > 1024:
    #         raise forms.ValidationError("Слишком большой файл!")
    #
    #     return data


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('password', 'username')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput())
    email = forms.CharField(widget=forms.EmailInput())
    first_name = forms.CharField(widget=forms.TextInput())
    age = forms.IntegerField(widget=forms.NumberInput())
    last_name = forms.CharField(widget=forms.TextInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'age','last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['email'].widget.attrs['placeholder'] = 'Ведите эл.почту'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['age'].widget.attrs['placeholder'] = 'Введите возраст'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Ведите фамилию'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтвердите пароль'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

    def clean_age(self):
        data= self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError('Вы слишком молоды!')
        return data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Данный Email зарегистрирован.')
        return email

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save()
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()
        return user

