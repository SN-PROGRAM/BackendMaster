from django import forms
from .models import User

class UserForm(forms.ModelForm):
    nickname = forms.CharField(max_length=50, label="Никнейм")
    email = forms.EmailField(label="Email")
    # По умолчанию поля для пароля делаем необязательными, но при регистрации мы их сделаем обязательными в __init__
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль', required=False)
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label='Подтверждение пароля', required=False)
    first_name = forms.CharField(required=False, label="Имя")
    last_name = forms.CharField(required=False, label="Фамилия")
    avatar = forms.ImageField(required=False, label="Аватар")

    class Meta:
        model = User
        fields = ['nickname', 'email', 'first_name', 'last_name', 'avatar', 'password', 'password_confirm']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance or not self.instance.pk:
            self.fields['password'].required = True
            self.fields['password_confirm'].required = True

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        # Если хотя бы одно из полей заполнено, то оба должны совпадать.
        if password or password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        # Если пользователь указал пароль (т.е. при регистрации или при изменении пароля)
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
