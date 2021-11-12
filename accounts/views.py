import datetime, json

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



class DepositView(View):
    @login_decorator
    def post(self,request):
        # try:
            data = json.loads(request.body)
            user_balance = data["user_balance"],
            transaction_money = data["transaction_money"]
            all = user_balance[0] + transaction_money
            #Account.save()

            # result = Account.objects.get(id=request.user.id).user_balance
            #result = account.user_balance
            # user = Account.objects.get(id=request.user.id)


            # # 잔고를 불러온다 + transaction_money를 더한다 + 총 잔고를 다시 저장해 계좌 잔고로 리턴
            # user_balance = Account.objects.get(id=request.user.id).balance
            # transaction_money = data["transaction_money"]
            # all_balance = user_balance + transaction_money
            # Account.save()
            
            # account = Account.objects.get(id=request.user.id).balance
            # # transaction = Transaction.objects.get(id=request.user.id)

            # result = Account.objects.create(
            #     balance = account.balance,
            #     )

            brief = data["brief"]
            #Transaction.save()
            # result로 적요랑 금액 묶어서 보내기

            return JsonResponse ({"result": all},{"brief": brief},{"message":"success deposit"},status = 201)

        # except KeyError:
        #     return JsonResponse ({"message": "KeyError"}, status = 400)


class WithdrawView(View):
    @login_decorator
    def post(self,request):
        # try:
            data = json.loads(request.body)
            # 잔고보다 많은 금액을 출금 요구하면 에러처리
            if data["balance"] <= data["transaction_money"]:
                return JsonResponse ({"message":"lack of balance"},status = 404)

            # 잔고를 불러온다 / 트랜잭션머니만큼 뺀다 / 남은 잔고 리턴 
            user_balance = Account.objects.get(id=request.user.id).balance
            transaction_money = data["transaction_money"]
            all_balance = user_balance - transaction_money
            Account.save()
  
            # account = Account.objects.get(id=request.user.id).balance
            # # transaction = Transaction.objects.get(id=request.user.id)

            # result = Transaction.objects.create(
            #     balance = account.balance,
            #     transaction_money = data["transaction_money"],

            #     brief = data["brief"]
            #     )


            return JsonResponse ({"balance": all_balance} ,{"message":"success withdraw"},status = 201)

        # except KeyError:
        #     return JsonResponse ({"message": "KeyError"}, status = 400)  

