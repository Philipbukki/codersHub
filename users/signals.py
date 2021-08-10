from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Profile


# @receiver(post_save, sender=User)
def createUser(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

# @receiver(post_delete, sender=Profile)


def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_save.connect(createUser, sender=User)
post_delete.connect(deleteUser, sender=Profile)
