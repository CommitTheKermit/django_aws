from django.shortcuts import render
import json, re, traceback
from django.http            import JsonResponse  
from django.views           import View          
from django.core.exceptions import ValidationError
from django.db.models       import Q                                                                                                                
from .models                import User
from django.views.decorators.csrf import csrf_exempt


class LoginView(View):
     @csrf_exempt
     def post(self, request):
        data = json.loads(request.body)

        try:
            request_id = data.get('id')
            request_password = data.get('pw')

            # 입력한 값이 Email인지 핸드폰 번호인지 검사
            id = User.objects.filter(user_id = request_id)
            if id.exists():
                account = User.objects.get(user_id = request_id)
                if account.password == request_password:
                    return JsonResponse({'message' : 'SUCCESS'}, status=200)
                else:
                    return JsonResponse({"message": "INVALID_PASSWORD"}, status=401)

            # ID 틀렸을시 return    
            return JsonResponse({"message": "INVALID_USER"}, status=401)
        # 다른 값을 입력했을시 return
        except KeyError: 
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
 #회원가입
class SignUpView(View):
    # 1.post방식으로 요청할 경우 회원가입한다.
    def post(self, request):
        
        # 2.data에 request에 담긴 정보를 넣어준다
        data = json.loads(request.body)
        # 3.이때 비밀번호의 경우 따로 암호화를 해줘야하기 때문에 password_not_hashed에 따로 담아준다
        
        try :
            User( 
                user_id     = data['id'],
                email    = data['email'],
                password = data['pw']
            ).save()

            #7.성공적으로 저장이 되었으면 성공 메시지를 보낸다.  
            return JsonResponse({'message':'회원가입 성공'}, status=200)

        # 8.예외처리
        except KeyError: 
            return JsonResponse({'message' : "INVALID_KEYS"},status =400) 

    # 9.테스트를 위한 get
    def get(self, request):
        user_data = User.objects.values()
        return JsonResponse({'users':list(user_data)}, status=200)   