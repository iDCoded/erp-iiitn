from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import StudentViewSet, FeeSubmissionViewSet, TransactionViewSet, ProofUploadViewSet, AdminViewSet, \
    UserRegistrationView

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'fee_submissions', FeeSubmissionViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'proof_uploads', ProofUploadViewSet)
router.register(r'admins', AdminViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
