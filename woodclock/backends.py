from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from project.models import User


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        UserModel = get_user_model()
        try:
            user = User.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.password == password:
                return user
        return None
