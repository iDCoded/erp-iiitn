from django.urls import re_path
from .views import login, signup, validate_token

urlpatterns = [
    re_path('login/' , login , name='login'), # /{{base_url}}/api/login/
    re_path('signup/', signup, name='signup'), # /{{base_url}}/api/signup/
    re_path('token', validate_token, name='validate') # /{{base_url}}/api/token/
]
