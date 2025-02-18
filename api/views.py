from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .serializers import UserSerializer

# POST request for login
@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])

    # Throw the same 404 (Not Found) error as incorrect username
    # When the password is incorrect to avoid disclosing invalid field.
    if not user.check_password(request.data['password']):
        return Response({"detail": "No User matches the given query."}, status=status.HTTP_404_NOT_FOUND)

    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)

    return  Response({
        "token": token.key,
        "user": serializer.data
    })

# POST request for signing up
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({
            "token": token.key,
            "user": serializer.data
        })
    return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET request for validating token
@api_view(['GET'])
def validate_token(request):
    return  Response({})