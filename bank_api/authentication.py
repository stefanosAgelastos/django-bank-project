from django.contrib.auth.models import User
from .models import Entity
from rest_framework import authentication
from rest_framework import exceptions


class EntityAuthentication(authentication.BaseAuthentication):

    # this method handles only the initial authorization provided a username
    def authenticate(self, request):
        username = request.POST.get('username')
        print(username)
        if not username:
            return None

        try:
            user = User.objects.get(username=username)
            entity = Entity.objects.get(user=user)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        except Entity.DoesNotExist:
            raise exceptions.AuthenticationFailed('User is not a bank')

        return (entity, None)
