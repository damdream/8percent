import json
import bcrypt
import jwt

from django.views     import View
from django.http      import JsonResponse

from users.models import User
from users.regex  import email_validator, password_validator, name_validator
from my_settings  import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
            name     = data['name']

            if not email_validator.match(email):
                return JsonResponse({'MESSAGE':'wrong e-mail form'}, status=400)

            if not password_validator.match(password):
                return JsonResponse({'MESSAGE':'wrong password form'}, status=400)

            if not name_validator.match(name):
                return JsonResponse({'MESSAGE':'wrong nickname form'}, status=400)

            if User.objects.filter(email = email).exists():
                    return JsonResponse({'MESSAGE':'existing e-mail'}, status = 409)
            
            if User.objects.filter(name = name).exists():
                    return JsonResponse({'MESSAGE':'existing nickname'}, status = 409)

            decoded_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                email    = email,
                password = decoded_password,
                name     = name,
            )

            return JsonResponse({'MESSAGE':'user created'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status=400)


class SignInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            if not User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE':'non-existing e-mail'}, status=409)

            user = User.objects.get(email=email)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'MESSAGE':'wrong password'}, status=401)

            token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm=ALGORITHM)

            return JsonResponse({'MESSAGE':'sign in success', 'TOKEN':token, 'USER_NAME':user.name}, status=200)
        
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status=400)
