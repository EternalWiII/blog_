from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from .models import CustomUser, Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'your@email.com'})
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': "Ім'я користувача"})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Користувач з таким email вже існує.')
        return email


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'your@email.com', 'autofocus': True})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'})
    )


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'bio', 'website', 'location')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Розкажіть про себе...'}),
            'website': forms.URLInput(attrs={'placeholder': 'https://yoursite.com'}),
            'location': forms.TextInput(attrs={'placeholder': 'Місто, Країна'}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email')


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'your@email.com'})
    )


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Новий пароль',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'})
    )
    new_password2 = forms.CharField(
        label='Підтвердіть пароль',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'})
    )
