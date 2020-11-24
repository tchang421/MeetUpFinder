from ..models import Event
from userprofile.models import UserProfile
from django.contrib.auth.models import User
   
def make_event(**kwargs):
    newEvent = Event(**kwargs)
    newEvent.save();
    return newEvent

def make_user(**kwargs):
    newUser = User(**kwargs)
    newUser.set_password(kwargs['password']);
    newUser.save();
    newProfile = UserProfile(user=newUser)
    newProfile.save();
    return newUser