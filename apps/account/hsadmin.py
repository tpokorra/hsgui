from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

from hsutilities import users as hsusers
from hsutilities import admin as hsadmin

class HsAdminBackend(BaseBackend):
    """
    Authenticate against the pac user with hsadmin.

    The user will be created on the first login.
    """

    def authenticate(self, request, username=None, password=None):
        pac = hsusers.get_current_pac()
        login_valid = (pac == username)

        pwd_valid = False
        try:
            api = hsadmin.get_api(username = username, password = password)
            pwd_valid = True
        except Exception as e:
            None

        if login_valid and pwd_valid:
            try:
                user = User.objects.get(username=username)
                #user.delete()
                #user = User.objects.get(username=username)
            except User.DoesNotExist:
                #raise Exception("new user")
                # Create a new user. There's no need to set a password
                # because only the password from hsadmin is checked.
                user = User(username=username)
                user.is_staff = True
                user.is_superuser = True
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
