from rest_framework import  serializers
from django.contrib.auth.models import User

# User serializer class (Inherited from DJANGO Auth)
# Contains user information fields - ID, username, email, password
class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name']
