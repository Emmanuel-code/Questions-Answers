from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email = models.EmailField(max_length=150)
    image = models.ImageField(default='IMG-20190328-WA0003_o0agDuw.jpg',upload_to='users/%Y/%m/%d/',blank=True)
    bio=models.TextField(blank=True)
    signup_confirmation=models.BooleanField(default=False)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


def create_profile(sender, instance, created, **kwargs):
    if created:
        profile=Profile.objects.create(user=instance)


post_save.connect(create_profile,sender=User)



