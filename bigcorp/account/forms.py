from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        """
        Initializes a UserCreateForm instance.

        This method initializes the UserCreateForm instance by calling the __init__ method of the parent class
        (UserCreationForm) with the provided arguments and keyword arguments. It also customizes the form fields
        by setting the label and required properties for the 'email' field, and removing help text for the 'username'
        and 'password1' fields.
        """
        super(UserCreateForm, self).__init__(*args, **kwargs)

        self.fields['email'].label = 'Email'
        self.fields['email'].required = True
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''

    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        if User.objects.filter(email=email).exists() or len(email) > 254:
            raise forms.ValidationError('Email already exists or too long')

        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['email'].label = 'Email'
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ('username', 'email')
        exclude = ('password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        if User.objects.filter(email=email).exclude(id=self.instance.id).exists() or len(email) > 254:
            raise forms.ValidationError('Email already in use or too long')

        return email
