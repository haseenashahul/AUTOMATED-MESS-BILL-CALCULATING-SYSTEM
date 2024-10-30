# from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth import get_user_model

# class EmailBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         User = get_user_model()
#         try:
#             # Here, 'username' refers to the email field
#             user = User.objects.get(email=username)
#         except User.DoesNotExist:
#             return None

#         # Check the password and ensure the user can authenticate
#         if user.check_password(password) and self.user_can_authenticate(user):
#             return user
#         return None
