import datetime

from datetime import timedelta

from django.http.response   import JsonResponse
from django.db.models       import Q
from django.views           import View
from django.core.exceptions import ValidationError

from users.models    import User
from users.decorator import login_decorator
from accounts.models import Account, Transaction


class TransactionHistoryView(View):
    @login_decorator
    def get(self, request):
        try:

            OFFSET = int(request.GET.get('offset', 0))
            LIMIT  = int(request.GET.get('limit', 3))

            if OFFSET < 0 or LIMIT < 0:
                return JsonResponse({'MESSAGE':'please request positive number'}, status=404) 

            now = datetime.datetime.now()

            start_date = request.GET.get('start_date', (now - timedelta(weeks=1)).strftime('%Y-%m-%d'))
            end_date   = request.GET.get('end_date', now)
            type       = request.GET.get('type', None)

            q = Q()

            if type:
                q = Q(type = type)

            q &= Q(created_at__range = (start_date, end_date))

            transactions = Transaction.objects.filter(q).order_by()[OFFSET:LIMIT]

            if not transactions.exists():
                return JsonResponse({'MESSAGE':'거래 내역이 존재하지 않습니다.'}, status=404)

            if not transactions[0].user_id == request.user.id:
                return JsonResponse({'MESSAGE':'wrong user'}, status=401)


            transaction_info = [
                {
                    '거래 일시'    : transaction.created_at.strftime('%Y-%m-%d'),
                    '거래 금액'    : transaction.transaction_money,
                    '거래 잔액'    : transaction.balance,
                    '거래 종류'    : transaction.type,
                    '적요'        : transaction.brief
                } for transaction in transactions
            ]

            return JsonResponse({'MESSAGE':transaction_info}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

        except ValidationError:
            return JsonResponse({'MESSAGE':'VALIDATION_ERROR'}, status=400)

        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status=400)

