from django.urls import path

from accounts.views import TransactionHistoryView, DepositView

urlpatterns = [
    path('/history', TransactionHistoryView.as_view()),
    path('/deposit', DepositView.as_view())
]