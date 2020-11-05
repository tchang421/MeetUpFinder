from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=40, null=True)
    bio = models.CharField(max_length=200, default='')
    join_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.user.username
        super().save(*args, **kwargs);