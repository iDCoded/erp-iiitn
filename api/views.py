from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Student, FeeSubmission, Transaction, ProofUpload, Admin
from .serializers import StudentSerializer, FeeSubmissionSerializer, TransactionSerializer, ProofUploadSerializer, \
    AdminSerializer, UserRegistrationSerializer


# permission_classes = [permissions.IsAuthenticated] For requiring JWT Access Token.

class UserRegistrationView(APIView):
    """ API endpoint to register new users (creates User + Student) """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Require authentication

    def get(self, request):
        user = request.user  # Get the user from the JWT token

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        })

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.AllowAny]


class FeeSubmissionViewSet(viewsets.ModelViewSet):
    queryset = FeeSubmission.objects.all()
    serializer_class = FeeSubmissionSerializer
    permission_classes = [permissions.AllowAny]


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.AllowAny]


class ProofUploadViewSet(viewsets.ModelViewSet):
    queryset = ProofUpload.objects.all()
    serializer_class = ProofUploadSerializer
    permission_classes = [permissions.AllowAny]


class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [permissions.AllowAny]
