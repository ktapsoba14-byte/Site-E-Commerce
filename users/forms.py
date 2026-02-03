from django import forms
from users.models import Users


class UserForm(forms.ModelForm):

    class Meta:
        model = Users
        fields = [
            "last_name",
            "first_name",
            "username",
            "email",
            "role_ecole",
            "est_membre",
            "est_fidele",
            ]