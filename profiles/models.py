from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver


class UserProfile(models.Model):
    """
    A user profile model for maintaining
     default delivery information and order history
    """

    # One-to-one field attached to the user.
    # This is just like a foreign key except that it specifies that each user can only have one profile.
    # And each profile can only be attached to one user
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Rest of the fields in this model are the delivery information fields we want the
    # user to be able to provide defaults for.
    # These can come directly from the order model

    # Want all these fields to be optional - null = True and blank = True for each of them
    default_phone_number = models.CharField(
        max_length=20, null=True, blank=True
    )
    # blank_label - use "Country" with the star to indicate it's a required field
    # since select boxes don't have a placeholder
    default_country = CountryField(
        blank_label="Country *", null=True, blank=True
    )
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_town_or_city = models.CharField(
        max_length=40, null=True, blank=True
    )
    default_street_address1 = models.CharField(
        max_length=80, null=True, blank=True
    )
    default_street_address2 = models.CharField(
        max_length=80, null=True, blank=True
    )
    default_county = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return self.user.username


# Since there's only one signal I'm not putting it in a separate "signals.py" module
# like we did for the ones on the order model.

# Each time a User object is saved
# Automatically either create a profile for them if the user has just been created,
# Or just save the profile (updating it) if the user already exists
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    print(f"Is this profile created?  {created}")
    if created:
        UserProfile.objects.create(user=instance)

    # Existing user => just save the profile
    instance.userprofile.save()
