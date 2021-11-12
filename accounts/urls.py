from django.urls import path
from accounts.views import WithdrawView, DepositView

urlpatterns = [
    path('/withdraw',WithdrawView.as_view()),
    path('/deposit', DepositView.as_view()),
]