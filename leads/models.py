from django.db import models
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
    pass  # this means we will not add anything to the superclass and will use the subclass as is (for now)


# Create your models here.
class Lead(models.Model):
    # fields corresponding to db columns
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    # this is a reference to the agent as it's a one-to-many relation
    agent = models.ForeignKey("Agent", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Agent(models.Model):
    # only one agent for each user (basically like inheritance)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # this method specifies the string representation of the object
    def __str__(self):
        return self.user.email
