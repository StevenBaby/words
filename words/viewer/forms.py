import logging
from django.contrib.auth.forms import UserCreationForm

from django.forms import Form
from django.forms import ModelForm
from django.forms import CharField
from django.forms import IntegerField
# from django.forms import MultiValueField
# from django.forms import ModelMultipleChoiceField

# from django.contrib.auth.models import User

# from django.
from words import models

logger = logging.getLogger("words")


class EmptyForm(Form):
    pass


class FilterForm(Form):
    review = IntegerField(required=False)
    level = IntegerField(required=False)
    hard = IntegerField(required=False)


class CheckForm(Form):

    input_line = CharField(required=False)
    id = IntegerField(required=False)


class EditForm(Form):
    para_type = CharField(required=False)
    para_content = CharField(required=False)
    title = CharField(required=False)


class RegisterSuperUserForm(UserCreationForm):

    def save(self, commit=True):
        user = super(RegisterSuperUserForm, self).save(commit=False)
        user.id = 1
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
        return user


class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.UserProfile
        exclude = ['user', ]
