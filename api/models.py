from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    """ Model for storing student information """
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to User model
    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.student_id})"


class FeeSubmission(models.Model):
    """ Model for tracking fee submissions """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('incomplete', 'Incomplete'),
        ('complete', 'Complete'),
    ]

    submission_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="fee_submissions")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission {self.submission_id} - {self.student.name}"

    def total_paid(self):
        """ Sum of all transactions linked to this submission """
        return self.transactions.aggregate(total=models.Sum('amount_paid'))['total'] or 0

    def is_fully_paid(self):
        """ Check if the total paid matches the required amount """
        return self.total_paid() >= self.total_amount


class Transaction(models.Model):
    """ Model for tracking multiple payments in a submission """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    transaction_id = models.AutoField(primary_key=True)
    submission = models.ForeignKey(FeeSubmission, on_delete=models.CASCADE, related_name="transactions")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[
        ('upi', 'UPI'),
        ('bank_transfer', 'Bank Transfer'),
        ('card', 'Credit/Debit Card')
    ])
    transaction_reference = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_date = models.DateTimeField()

    def __str__(self):
        return f"Txn {self.transaction_id} - {self.amount_paid} ({self.status})"


class ProofUpload(models.Model):
    """ Model for storing payment proof (screenshot) """
    proof_id = models.AutoField(primary_key=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="proof_uploads")
    file_url = models.FileField(upload_to='payment_proofs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Proof {self.proof_id} for Txn {self.transaction.transaction_id}"


class Admin(models.Model):
    """ Model for storing admin information """
    ADMIN_ROLES = [
        ('superadmin', 'Super Admin'),
        ('finance', 'Finance'),
        ('moderator', 'Moderator')
    ]

    admin_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ADMIN_ROLES, default='superadmin')

    def __str__(self):
        return f"{self.user.username} ({self.role})"
