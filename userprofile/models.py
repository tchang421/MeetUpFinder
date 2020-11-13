from django.db import models
from django.contrib.auth.models import User
from django.urls.base import reverse

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=40, null=True)
    bio = models.CharField(max_length=200, blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(upload_to = 'profile_pics', blank = True)

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.user.username
        super().save(*args, **kwargs);

    def get_absolute_url(self):
        return reverse("userprofile:show", kwargs={"pk": self.pk})
    