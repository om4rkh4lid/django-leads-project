from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Lead, Agent

User = get_user_model()

# create a subclass of Forms that will create a Django form for us


class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',
            'description',
            'phone_number',
            'email',
        )


class LeadForm(forms.Form):
    # the input fields inside the form
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=0)


class CustomCreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}


class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())
    # we need to choose only the agents that are part of the organization but how can we access the organization?
    # we need to pass it to the form through th view's kwargs
    # then we edit the form by overriding the constructor

    def __init__(self, *args, **kwargs):
        # first pop the request because the form will not be expecting it
        request = kwargs.pop('request')
        # get the queryset we want
        agents = Agent.objects.filter(organization=request.user.userprofile)
        # initialize the form using super()
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        # edit the queryset on the field
        self.fields["agent"].queryset = agents


class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ("category",)
