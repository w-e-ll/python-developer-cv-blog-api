from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate
from accounts.models import User
# User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        # user_qs = User.objects.filter(username=username)
        # if user_qs.count() == 1:
        #     user = user_qs.first()
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist.")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password.")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    email2 = forms.EmailField(label='Confirm Email')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError('Emails must match.')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already registered.")
        return email


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'username', 'email',)  # 'username',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserDetailChangeForm(forms.ModelForm):
    username = forms.CharField(
        label='Name', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))

    class Meta:
        model = User
        fields = ['username']


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('full_name', 'username', 'email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
