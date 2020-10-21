from ..models import Event
from django.contrib.auth.models import User
   
def make_event(**kwargs):
    newEvent = Event(**kwargs)
    newEvent.save();
    return newEvent

def make_User(**kwargs):
    newUser = User(**kwargs)
    newUser.save();
    return newUser