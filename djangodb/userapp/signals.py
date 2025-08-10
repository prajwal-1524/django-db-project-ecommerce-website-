from django.db.models.signals import post_save
from django.dispatch import receiver
from django.models import Profile,vendor
from django.from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
# user save garey vani profile data model ma pani automatically save hos vanera
def create_profile(sender,instance,created,**kwargs):
    # automatically create a profile when a user is created
    if created:
        Profile.objects.create(user=instance)

    if hasattr(instance, 'is_vendor') and instance.is_vendor:
        # Automatically create a vendor when a user is created
        vendor.objects.create(user=instance)    

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, **kwargs):
    # save the profile when the user is saved
    instance.profile.save()