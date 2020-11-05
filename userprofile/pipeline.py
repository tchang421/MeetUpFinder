from .models import UserProfile
from django.core.exceptions import ObjectDoesNotExist

def print_profile(backend, user, response, *args, **kwargs):
    try:
        profile = user.profile
        print(profile)
    except ObjectDoesNotExist:
        print('no profile')

def make_profile(backend, user, response, *args, **kwargs):
    if not hasattr(user, 'profile'):
        newProfile = UserProfile(user=user)
        newProfile.save();
