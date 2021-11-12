from django.db    import models

from users.models import User
from core.models  import TimeStampModel

class Account(models.Model):
    user_balance = models.DecimalField(max_digits=16, decimal_places=2)
    user         = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'accounts'

class Transaction(TimeStampModel):
    balance           = models.DecimalField(max_digits=16, decimal_places=2)
    transaction_money = models.DecimalField(max_digits=16, decimal_places=2)
    type              = models.PositiveIntegerField()
    brief             = models.TextField(max_length=100)
    user              = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'transactions'
