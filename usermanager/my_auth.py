from django.contrib.auth import get_user_model
#from django.contrib.auth.hashers import check_password

User = get_user_model()

class UserBackend:
    def authenticate(self, userid=None, password=None):
        try:
            user = User.objects.get(userid = userid)
            if user.check_password(password):
                return user
            
            else:
                return None
        except User.DoesNotExist:
            return None

    
    def get_user(self, user_pk):
        try:
            return User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return None