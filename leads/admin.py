from django.contrib import admin
from .models import User, Agent, Lead, UserProfile, Category
# Register our models here to be able to accesss them from the Django Admin.

admin.site.register(Category)
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Agent)
admin.site.register(Lead)
