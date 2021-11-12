from django.urls import path
from accounts.views import TransactionHistoryView, WithdrawView, DepositView

urlpatterns = [
    path('/history', TransactionHistoryView.as_view()),
    path('/withdraw',WithdrawView.as_view()),
    path('/deposit', DepositView.as_view()),
]