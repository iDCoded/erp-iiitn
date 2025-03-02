from django.urls import re_path
from .views import login, signup, validate_token, PaymentsListView, TransactionsListView

urlpatterns = [
    re_path('login/' , login , name='login'), # /{{base_url}}/api/login/
    re_path('signup/', signup, name='signup'), # /{{base_url}}/api/signup/
    re_path('token', validate_token, name='validate'),  # /{{base_url}}/api/token/
    re_path('payments', PaymentsListView.as_view(), name="payments-list"),  # /{{base_url}}/api/payments/
    re_path('transactions', TransactionsListView.as_view(), name="transactions-list")  # /{{base_url}}/api/transactions/
]
