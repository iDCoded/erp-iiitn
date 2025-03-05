from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student, FeeSubmission, Transaction, ProofUpload, Admin


class UserRegistrationSerializer(serializers.ModelSerializer):
    """ Serializer for registering new users and creating Student entries """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        # Automatically create a Student profile
        Student.objects.create(user=user, name=user.username, email=user.email)
        return user


class StudentSerializer(serializers.ModelSerializer):
    """ Serializer for Student Model """

    class Meta:
        model = Student
        fields = '__all__'


class FeeSubmissionSerializer(serializers.ModelSerializer):
    """ Serializer for Fee Submission Model """
    total_paid = serializers.SerializerMethodField()
    is_fully_paid = serializers.SerializerMethodField()

    class Meta:
        model = FeeSubmission
        fields = ['submission_id', 'student', 'total_amount', 'status', 'submitted_at', 'total_paid', 'is_fully_paid']
        read_only_fields = ['submitted_at']

    def get_total_paid(self, obj):
        """ Calculate total paid from transactions """
        return obj.total_paid()

    def get_is_fully_paid(self, obj):
        """ Check if the submission is fully paid """
        return obj.is_fully_paid()


class TransactionSerializer(serializers.ModelSerializer):
    """ Serializer for Transaction Model """

    class Meta:
        model = Transaction
        fields = ['transaction_id', 'submission', 'amount_paid', 'payment_method', 'transaction_reference', 'status',
                  'transaction_date']
        read_only_fields = ['status']

    def validate_transaction_reference(self, value):
        """ Ensure transaction reference is unique """
        if Transaction.objects.filter(transaction_reference=value).exists():
            raise serializers.ValidationError("Transaction reference already exists.")
        return value


class ProofUploadSerializer(serializers.ModelSerializer):
    """ Serializer for Proof Upload Model """

    class Meta:
        model = ProofUpload
        fields = ['proof_id', 'transaction', 'file_url', 'uploaded_at']
        read_only_fields = ['uploaded_at']


class AdminSerializer(serializers.ModelSerializer):
    """ Serializer for Admin Model """

    class Meta:
        model = Admin
        fields = '__all__'
