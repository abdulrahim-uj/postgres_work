from django.db.models.signals import post_save
from django.dispatch import receiver
from basics.functions import get_auto_id
from .models import User, UserProfile


@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        autoid = get_auto_id(UserProfile)
        creator = instance
        updater = instance
        UserProfile.objects.create(user=instance, auto_id=autoid, creator=creator,
                                   updater=updater)
    else:
        # If created == False [update case]
        try:
            user_profile = UserProfile.objects.get(user=instance)
            user_profile.save()
        except:
            # Create Userprofile if it does not exist
            autoid = get_auto_id(UserProfile)
            creator = instance
            updater = instance
            UserProfile.objects.create(user=instance, auto_id=autoid,
                                       creator=creator, updater=updater)
