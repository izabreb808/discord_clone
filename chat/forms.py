from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Channel


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
        self.fields["email"].required = True

    def clean_email(self):
        email = self.cleaned_data["email"]
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ten email jest juz zajety.")
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("email", "avatar_url", "bio")
        labels = {
            "avatar_url": "Link do avatara",
            "bio": "Opis",
        }
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    def clean_email(self):
        email = self.cleaned_data["email"]
        User = get_user_model()
        qs = User.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ten email jest juz zajety.")
        return email


class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ("name",)
        labels = {"name": "Nazwa kanalu"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "form-control"})
