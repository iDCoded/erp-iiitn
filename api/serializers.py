from rest_framework import  serializers
from django.contrib.auth.models import User

from api.models import Payments, Transactions


# User serializer class (Inherited from DJANGO Auth)
# Contains user information fields - ID, username, email, password
class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name']


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"  # Serialize all fields


class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        payment = PaymentsSerializer(source="Payments")  # Serialize ForeignKey

        class Meta:
            model = Transactions
            fields = "__all__"
