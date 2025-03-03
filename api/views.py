from django.template.context_processors import request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .serializers import UserSerializer, PaymentsSerializer, TransactionsSerializer
from .models import Payments, Transactions

# POST request for login
@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, email=request.data['email'])

    # Throw the same 404 (Not Found) error as incorrect username
    # When the password is incorrect to avoid disclosing invalid field.
    if not user.check_password(request.data['password']):
        return Response({"detail": "No User matches the given query."}, status=status.HTTP_404_NOT_FOUND)

    # Get the token and instantiate user serializer.
    # Create token in case of missing token.
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)

    # Return token key and user object
    return  Response({
        "token": token.key,
        "user": serializer.data
    })

# POST request for signing up
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)  # Create user serializer based on request data
    if serializer.is_valid():
        serializer.save()
        # Fetch user by their username
        user = User.objects.get(username=request.data['username'])

        # Set user information from the request
        user.set_password(request.data['password'])  # Hash the user password
        user.first_name = request.data['firstName']
        user.last_name = request.data['lastName']
        user.save()  # Save the hashed password

        token = Token.objects.create(user=user)  # Generate token for user
        return Response({
            "token": token.key,
            "user": serializer.data
        })
    return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET request for validating token

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def validate_token(request):
    user = request.user

    return Response({
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    })


# Retrieve all payments
class PaymentsListView(generics.ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


# Retrieve all Transactions
class TransactionsListView(generics.ListAPIView):
    queryset = Transactions.objects.all()
    serializer_class = TransactionsSerializer


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_payment_form(request):
    serializer = PaymentsSerializer(data=request.data)

    if serializer.is_valid():
        instance = serializer.save()  # Save to the database
        return Response({
            "message": "Payment form submitted successfully!",
            "payment": PaymentsSerializer(instance).data  # Serialize saved instance
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_transaction_form(request):
    serializer = TransactionsSerializer(data=request.data)

    if serializer.is_valid():
        instance = serializer.save()
        return Response({
            "message": "Transaction submitted successfully!",
            "transaction": TransactionsSerializer(instance).data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
