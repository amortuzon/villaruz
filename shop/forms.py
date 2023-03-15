from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django import forms
from django.forms import CheckboxSelectMultiple
from datetime import date, time
from . models import *
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TermsRecaptchaForm(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = '__all__'
        # exclude = ['customer', 'status']


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class ReservationUpdateForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = '__all__'
        exclude = ['customer', 'status']
        widgets = {
            'date': DateInput(attrs={'min': date.today(), 'required': True}),
            'time': TimeInput(format='%H:%M', attrs={'min': '09:00', 'max': '17:00', 'required': True}),
            'service': CheckboxSelectMultiple()
        }


class ReservationUpdateFormAdmin(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['status']
        exclude = ['customer']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user', 'profile_pic']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['email', 'message', 'rating']


class MessageFormUpdate(forms.ModelForm):
    class Meta:
        model = Comments
        fields = '__all__'
        exclude = ['customer', 'name']


class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['review', 'rating', 'service']


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']


class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
