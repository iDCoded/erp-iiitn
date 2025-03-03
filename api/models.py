from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Payments(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    dateDue = models.DateField()


class Transactions(models.Model):
    id = models.AutoField(primary_key=True)
    Payments= models.ForeignKey(Payments, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    no_of_payments = models.IntegerField(default=1)
    transaction_id = models.TextField()
    payment_pic = models.ImageField()
    verified = models.BooleanField(default=False)
    payment_datetime = models.DateTimeField()
    


