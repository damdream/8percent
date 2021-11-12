import jwt
import json
import datetime

from datetime import timedelta

from django.http import response
from django.test import TestCase, Client

from users.models    import User
from accounts.models import Account, Transaction
from my_settings     import SECRET_KEY, ALGORITHM

class TransactionHistoryViewTest(TestCase):
    def setUp(self):
        user1 = User.objects.create(id=1, email='test1@test.com', password='TESTtest1234!!', name='testman1')
        user2 = User.objects.create(id=2, email='test2@test.com', password='TESTtest1234!!', name='testman2')

        Transaction1 = Transaction.objects.create(id=1, balance=4000000, transaction_money=1000000, type=1, brief='입금', user=user1)
        Transaction2 = Transaction.objects.create(id=2, balance=3000000, transaction_money=1000000, type=0, brief='출금', user=user1)
        Transaction3 = Transaction.objects.create(id=3, balance=2000000, transaction_money=1000000, type=0, brief='출금', user=user1)


    # 성공 (200)
    def test_transacion_get_success(self):
        client = Client()

        token   = jwt.encode({'id' : 1}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"HTTP_Authorization": token} 

        response = client.get('/accounts/history', **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'MESSAGE': [
            {
                '거래 일시' : '2021-11-12',
                '거래 금액' : '1000000.00',
                '거래 잔액' : '4000000.00',
                '거래 종류' : 1,
                '적요' : '입금'
            },
            {
                '거래 일시' : '2021-11-12',
                '거래 금액' : '1000000.00',
                '거래 잔액' : '3000000.00',
                '거래 종류' : 0,
                '적요' : '출금'
            },
            {
                '거래 일시' : '2021-11-12',
                '거래 금액' : '1000000.00',
                '거래 잔액' : '2000000.00',
                '거래 종류' : 0,
                '적요' : '출금'
            }
        ]})


    # 입금 내역 필터링
    def test_transactin_get_1_success(self):
        client = Client()

        token   = jwt.encode({'id' : 1}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"HTTP_Authorization": token} 

        response = client.get('/accounts/history?type=1', **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'MESSAGE': [
            {
                '거래 일시' : '2021-11-12',
                '거래 금액' : '1000000.00',
                '거래 잔액' : '4000000.00',
                '거래 종류' : 1,
                '적요' : '입금'
            }
        ]})


    # 출금 내역 필터링
    def test_transactin_get_0_success(self):
        client = Client()

        token   = jwt.encode({'id' : 1}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"HTTP_Authorization": token} 

        response = client.get('/accounts/history?type=0', **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'MESSAGE': [
            {
                '거래 일시' : '2021-11-12',
                '거래 금액' : '1000000.00',
                '거래 잔액' : '3000000.00',
                '거래 종류' : 0,
                '적요' : '출금'
            },
            {
                '거래 일시' : '2021-11-12',
                '거래 금액' : '1000000.00',
                '거래 잔액' : '2000000.00',
                '거래 종류' : 0,
                '적요' : '출금'
            }
        ]})


    # 날짜별 필터링
    def test_transaction_get_date_success(self):
        client = Client()

        token   = jwt.encode({'id' : 1}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"HTTP_Authorization": token} 

        response = client.get('/accounts/history?start_date=2021-11-01&end_date=2021-12-30', **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'MESSAGE': [
            {
                '거래 일시' : '2021-11-12',
                '거래 금액' : '1000000.00',
                '거래 잔액' : '4000000.00',
                '거래 종류' : 1,
                '적요' : '입금'
            },
            {
                '거래 일시' : '2021-11-12',
                '거래 금액' : '1000000.00',
                '거래 잔액' : '3000000.00',
                '거래 종류' : 0,
                '적요' : '출금'
            },
            {
                '거래 일시' : '2021-11-12',
                '거래 금액' : '1000000.00',
                '거래 잔액' : '2000000.00',
                '거래 종류' : 0,
                '적요' : '출금'
            }
        ]})


    #  검색 내역이 없을 시
    def test_transaction_get_not_existing_transaction_error(self):
        client = Client()

        token   = jwt.encode({'id' : 1}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"HTTP_Authorization": token} 

        response = client.get('/accounts/history?start_date=2021-12-01&end_date=2021-12-30', **headers)


        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'MESSAGE':'거래 내역이 존재하지 않습니다.'})


    # 잘못된 유저로 접근 시 
    def test_transaction_get_wrong_user_error(self):
        client = Client()

        token   = jwt.encode({'id' : 2}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"HTTP_Authorization": token} 

        response = client.get('/accounts/history', **headers)


        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'MESSAGE':'wrong user'})


    # 잘못된 형식의 OFFSET, LIMIT입력)
    def test_transaction_get_wronf_offset_limit_error(self):
        client = Client()

        token   = jwt.encode({'id' : 1}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"HTTP_Authorization": token} 

        response = client.get('/accounts/history?offset=-1', **headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'MESSAGE':'please request positive number'})


    # Validation Error Handling (잘못된 형식의 날짜 입력)
    def test_transaction_get_validatoin_error(self):
        client = Client()

        token   = jwt.encode({'id' : 1}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"HTTP_Authorization": token} 

        response = client.get('/accounts/history?start_date=2021&end_date=2021', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'VALIDATION_ERROR'})


    # Value Error Handling (잘못된 형식의 type입력)
    def test_transaction_get_value_error(self):
        client = Client()

        token   = jwt.encode({'id' : 1}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"HTTP_Authorization": token} 

        response = client.get('/accounts/history?type=1.5', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'VALUE_ERROR'})
