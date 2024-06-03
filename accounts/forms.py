from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from django.core.exceptions import ValidationError
from .models import Profile

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100,  widget=forms.TextInput(attrs={'class':'search-box__input', 'placeholder':'Tìm kiếm'}))

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'signup_input', 'placeholder':'Email'}), required=True)
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'signup_input', 'placeholder':'Tên'}), required=True)
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'signup_input', 'placeholder':'Họ'}), required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'signup_input'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = ''

        self.fields['password1'].widget.attrs['class'] = 'signup_input'
        self.fields['password1'].widget.attrs['placeholder'] = 'Mật khẩu'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = ''

        self.fields['password2'].widget.attrs['class'] = 'signup_input'
        self.fields['password2'].widget.attrs['placeholder'] = 'Nhập lại mật khẩu'
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already exists')
        return email

class UpdateProfileForm(UserChangeForm):
    password = None
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class':'signup_input', 'placeholder':'Email'}))
    first_name = forms.CharField(label="Tên", max_length=100, widget=forms.TextInput(attrs={'class':'signup_input', 'placeholder':'Tên'}))
    last_name = forms.CharField(label="Họ", max_length=100, widget=forms.TextInput(attrs={'class':'signup_input', 'placeholder':'Họ'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
    
    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'signup_input'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = 'Tên tài khoản'
        self.fields['username'].help_text = ''

class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs['class'] = 'signup_input'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Mật khẩu'
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].help_text = ''

        self.fields['new_password2'].widget.attrs['class'] = 'signup_input'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Nhập lại mật khẩu'
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].help_text = ''

class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'signup_input', 'placeholder':'Số điện thoại'}), required=True)
    address = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'signup_input', 'placeholder':'Địa chỉ'}), required=True)

    class Meta:
        model = Profile
        fields = ('phone', 'address')