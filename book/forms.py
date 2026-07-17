from django import forms
from book.models import Login


class logindb(forms.ModelForm):
    class Meta:
        model = Login
        fields = '__all__'