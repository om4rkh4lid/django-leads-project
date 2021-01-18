from django.contrib import admin
from .models import User, Agent, Lead
# Register our models here to be able to accesss them from the Django Admin.

admin.site.register(User)
admin.site.register(Agent)
admin.site.register(Lead)
