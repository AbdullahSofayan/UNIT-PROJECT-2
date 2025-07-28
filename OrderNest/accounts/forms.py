from django import forms

from .models import User, Address

class LoginForm(forms.Form):
    
    username = forms.CharField(
        max_length=128,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Username'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter Password'})
    )

class SignUpForm(forms.Form):

    username = forms.CharField(
        max_length=128,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Username'})
    )

    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Full name'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Password'})
    )

    email = forms.EmailField(
        widget = forms.TextInput(attrs={'class': 'form-control','placeholder': 'Email'})
    )

    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Phone number'})
    )

    address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Address'})
    )

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['password','role', 'shop']  
        widgets = {
            'username':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Username'}),
            'full_name':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Full name'}),
            'password':forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Password'}),
            'email':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Email'}),
            'phone':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Phone number'}),
            'address':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Address'})
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['title', 'address', 'latitude', 'longitude']
