import json
from django.views           import View
from django.http.response import JsonResponse

from users.decorator import login_decorator

from .models    import User, Account, Transaction, TimeStampModel


class DepositView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            # 1번 방법: 잔고를 불러온다 + transaction_money를 더한다 + 총 잔고를 다시 저장해 계좌 잔고로 리턴
            # user_balance = Account.objects.get(id=data["balance"])
            # transaction_money = Transaction.objects.get(id=data["transaction_money"])
            # deposit = user_balance + transaction_money
            # all_balance = user_balance.save()

            # 입금이 동시에 여러번 이루어진다면?
            # 2번 방법 : 리스트를 만들어 balance를 넣고, 그 값에 transaction_money를 append. for문 활용해서 값 더하기
            balance = [Account.objects.get(id=data["balance"])]
            balance.append(Transaction.objects.get(id=data["transaction_money"]))
            brief = data["brief"]
            num = 0
            for i in balance:
                num += i
                return balance
            balance.save()   
            #[a for a in balance if balance[1] == " "] 
            Account.objects.create(
                user_balance = Account.objects.get(id=data["balance"]),
            )
            Transaction.objects.create(
                balance = data["balance"],
                transaction_money = data["transaction_money"],
                brief = data["brief"]
            )


            return JsonResponse ({"balance": balance}, {"brief": brief} ,{"message":"success deposit"},status = 201)

        except KeyError:
            return JsonResponse ({"message": "KeyError"}, status = 400)


class WithdrawView(View):
    @login_decorator
    def post(self,request):
        try:
            data = json.loads(request.body)
            # 잔고보다 많은 금액을 출금 요구하면 에러처리
            if data["balance"] <= data["transaction_money"]:
                return JsonResponse ({"message":"lack of balance"},status = 404)

            # 잔고를 불러온다 / 트랜잭션머니만큼 뺀다 / 남은 잔고 리턴 
            balance = [Account.objects.get(id=data["balance"])]
            balance.append(Transaction.objects.get(id=data["transaction_money"]))
            num = 0
            for i in balance:
                num -= i
                return balance
            balance.save()   

            return JsonResponse ({"balance": balance} ,{"message":"success withdraw"},status = 201)

        except KeyError:
            return JsonResponse ({"message": "KeyError"}, status = 400)  