from django.contrib import admin
from .models import Student, FeeSubmission, Transaction, ProofUpload, Admin

admin.site.register(Student)
admin.site.register(FeeSubmission)
admin.site.register(Transaction)
admin.site.register(ProofUpload)
admin.site.register(Admin)
