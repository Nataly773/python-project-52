from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        ]
        help_texts = {
            "username": _(
                "Required. 150 characters or fewer. "
                "Letters, digits and @/./+/-/_ only."
            ),
            "password1": _(
                "<ul><li>Your password must be at "
                "least 3 characters long.</ul></li>"
            ),
            "password2": _("To confirm, please enter your password again."),
        }
        labels = {
            "first_name": _("First Name"),
            "last_name": _("Last Name"),
            "username": _("Username"),
            "password1": _("Password"),
            "password2": _("Confirm Password"),
        }
        widgets = {
            "password": forms.PasswordInput(),
        }

    def clean(self):
        password = self.cleaned_data.get("password1")
        confirm_password = self.cleaned_data.get("password2")
        if not password:
            self.add_error("password1", _("You must enter a password."))
        elif password != confirm_password:
            self.add_error(
                "password2", _("The passwords entered do not match.")
            )
        elif len(password) < 3:
            self.add_error(
                "password2",
                _(
                    "The password you entered is too short. "
                    "It must contain at least 3 characters."
                ),
            )
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data["username"]
        if len(username) > 150:
            self.add_error(
                "username", _("Username is too long (maximum 150 characters).")
            )
        if not all(c.isalnum() or c in "@.+-_" for c in username):
            self.add_error(
                "username",
                _(
                    "Please enter a valid username. "
                    "It can only contain letters, numbers and @/./+/-/_ signs.",
                ),
            )

        User = get_user_model()
        existing_user = User.objects.filter(username=username).first()

        if existing_user:
            if (
                not hasattr(self, "instance")
                or self.instance.pk != existing_user.pk
            ):
                self.add_error(
                    "username", _("A user with this name already exists.")
                )
        return username
    

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")
        labels = {
            "username": "Username",
            "first_name": "First Name",
            "last_name": "Last Name",
        }

    def clean_username(self):
        username = self.cleaned_data["username"]
        if len(username) > 150:
            raise forms.ValidationError(
                "Username is too long"
                "(maximum 150 characters)."
                )
        if not all(c.isalnum() or c in "@.+-_" for c in username):
            raise forms.ValidationError(
                "Please enter a valid username."
                "Letters, numbers and @/./+/-/_ only."
            )
        # Проверка уникальности, исключая текущего пользователя
        existing_user = (
            User.objects
            .filter(username=username)
            .exclude(pk=self.instance.pk)
            .first()
        )
        if existing_user:
            raise forms.ValidationError(
                "A user with this username already exists."
                )
        return username
