from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'shipping_input', 'placeholder':'Họ và Tên'}))
    shipping_email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'shipping_input', 'placeholder':'Email'}))
    shipping_address = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'shipping_input', 'placeholder':'Địa chỉ'}))
    shipping_phone = forms.CharField(label="", max_length=10, widget=forms.TextInput(attrs={'class':'shipping_input', 'placeholder':'Số điện thoại'}))

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_address', 'shipping_phone']
        exclude = ['user',]

class PaymentForm(forms.Form):
    card_name =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'billing_input', 'placeholder':'Tên chủ thẻ'}), required=True)
    card_bank =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'billing_input', 'placeholder':'Tên ngân hàng'}), required=True)
    card_number =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'billing_input', 'placeholder':'Số thẻ'}), required=True)
    card_exp_date =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'billing_input', 'placeholder':'Ngày cấp thẻ'}), required=True)