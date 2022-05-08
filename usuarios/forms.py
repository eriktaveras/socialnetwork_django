from django.forms import ModelForm
from usuarios.models import Post, Comment, Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, User
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit
from django import forms

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
          'content': forms.Textarea(attrs={'rows':3,  'placeholder':"What are you thinking?"}),
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'email',
            'password1',
            'password2',
            ButtonHolder(
            Submit('register', 'Register', css_class='btn-primary')
            )
        )

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            ButtonHolder(

            Submit('login', 'Login', css_class='btn-primary')
            )
        )
#
# class UserEditForm(UserChangeForm):
#     password = None
#
#     class Meta:
#         model = Profile
#         fields = ['username', 'email', 'first_name', 'last_name' ]
#         widgets = {
#             'username': forms.TextInput(attrs={'readonly': 'readonly'}),
#             'email': forms.TextInput(attrs={'readonly': 'readonly'})
#         }


class UserEditForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout('username', 'password', ButtonHolder(
                    Submit('Edit', 'Edit', css_class='btn-primary')
                )
            )
