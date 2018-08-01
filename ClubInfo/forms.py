from django import forms
from django.forms import ModelForm
from .validators import validate_date_time
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Announcement, Score, Contest
# class RegisterForm(forms.Form):
#     first_name = forms.CharField(label="First name", max_length=20)
#     last_name = forms.CharField(label="Last name", max_length=20)
#     username = forms.CharField(label="Your username", max_length=20)
#     email = forms.EmailField(label="Email", max_length=26)
#     password = forms.CharField(label="Password", max_length=20, widget=forms.PasswordInput)

class AnnouncementForm(forms.Form):
    title = forms.CharField(label="Title", max_length=128)
    body = forms.CharField(widget=forms.Textarea, label="Body", max_length=511)

class CommentForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea, label="Body", max_length=512)
    ann_id = forms.CharField(widget=forms.HiddenInput)
    # announcement = forms.CharField(widget=forms.HiddenInput(), required=False)

class ModifyContestInfoForm(forms.Form):
    name = forms.CharField(label="Name of Contest", max_length=64)
    date = forms.DateTimeField(label="Date Taken", input_formats=['%m-%d-%Y'])

class AddContestUserForm(forms.Form):
    score = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        # https://stackoverflow.com/questions/19007990/django-form-validation-with-parameters-from-view
        self.form_contest_id = kwargs.pop("contest_id")
        super(AddContestUserForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        c = Contest.objects.get(id=self.form_contest_id)
        if cleaned_data['score'] < 0 or cleaned_data['score'] > c.out_of:
            raise forms.ValidationError("{} is an invalid score. Contest is out of {}".format(cleaned_data['score'],
                                                                                              c.out_of))
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    # email = forms.EmailField(max_length=254, required=True, label="Email", help_text="Required")
    class Meta:
        model=User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        # exclude = ['first_name']
        # fields =

#TODO: validators
#TODO: confirm password