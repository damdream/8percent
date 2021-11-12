from django.urls import path

from accounts.views import TransactionHistoryView

urlpatterns = [
    path('/history', TransactionHistoryView.as_view())
]