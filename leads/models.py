from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    This is our own implementation of the default User class by extending AbstractUser which is
    an abstract base class implementing a fully featured User model with admin-compliant permissions.
    Username and password are required. Other fields are optional.
    to properly access this class use:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    """
    is_organizer = models.BooleanField(
        default=True)  # create account for your own org
    # organizer creates the account for you
    is_agent = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# Create your models here.
class Lead(models.Model):
    # fields corresponding to db columns
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # related_name is the name of the property that we can access the leads from the category object using
    category = models.ForeignKey(
        "Category", related_name='leads', null=True, blank=True, on_delete=models.CASCADE)
    # this is a reference to the agent as it's a one-to-many relation
    agent = models.ForeignKey(
        "Agent", null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Agent(models.Model):
    # only one agent for each user (basically like inheritance)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(
        UserProfile, related_name='agents', on_delete=models.CASCADE)

    # this method specifies the string representation of the object
    def __str__(self):
        return self.user.email


class Category(models.Model):
    # New / Contacted / Converted / Unconverted
    name = models.CharField(max_length=30)
    # because each organsation may have different categories
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# A signal is like an event listener for certain events that enables us to do something when a certain event is triggered
def post_user_created_event(sender, instance, created, **kwargs):
    # created refers to whether this object was created for the first time (TRUE) or saved as an update (FALSE)
    if created:
        UserProfile.objects.create(user=instance)


# let the post_save signal call the function passed as the first argument AFTER the model passed as the second argument performs a save
post_save.connect(post_user_created_event, sender=User)
