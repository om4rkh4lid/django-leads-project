from django import forms
# from django.contrib.auth import get_user_model
from leads.models import User
# User = get_user_model()


class AgentModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name'
        )


# class LeadModelForm(forms.ModelForm):
#     class Meta:
#         model = Lead
#         fields = (
#             'first_name',
#             'last_name',
#             'age',
#             'agent',
#             'description',
#             'phone_number',
#             'email',
#         )
