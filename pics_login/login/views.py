from django.shortcuts import render
import json, re, traceback
from django.http            import JsonResponse  
from django.views           import View          
from django.core.exceptions import ValidationError
from django.db.models       import Q                                                                                                                
from .models                import User
from django.views.decorators.csrf import csrf_exempt
from .serializer import User_basic_serializer


class LoginView(View):
     @csrf_exempt
     def post(self, request):
        data = json.loads(request.body)

        try:
            request_id = data.get('user_id')
            request_password = data.get('user_pw')

            id = User.objects.filter(user_id = request_id)
            if id.exists():
                account = User.objects.get(user_id = request_id)
                if account.user_pw == request_password:
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

        try :
            if User.objects.filter(user_id = data['user_id']).exists() or\
                User.objects.filter(user_phone = data['user_phone']).exists():
                return JsonResponse({'message' : "ID ALREADY EXISTS"},status =400) 

            User( 
                user_id    = data['user_id'],
                user_pw    = data['user_pw'],
                user_phone = data['user_phone']
                
            ).save()
            

            #7.성공적으로 저장이 되었으면 성공 메시지를 보낸다.  
            return JsonResponse({'message':'회원가입 성공'}, status=200)

        # 8.예외처리
        except KeyError:
            return JsonResponse({'message' : "INVALID_KEYS"},status =400) 

    # 9.조회 get id값으로 !get_all 보내면 전체 조회 특정 아이디 보내면 해당 아이디 정보 반환
    def get(self, request):
        data = json.loads(request.body)
        if data['user_id'] == "!get_all":
            user_data = User.objects.values()
            return JsonResponse({'users':list(user_data)}, status=200)
        
        else:
            request_id = data['user_id']
            
            if User.objects.filter(user_id = request_id).exists():
                account = User.objects.get(user_id = request_id)
                serializer = User_basic_serializer(account)
                return JsonResponse(serializer.data, status= 200)
            else:
                return JsonResponse({'message' : "INVALID_KEYS"},status=400)
            
class FindIdView(View):

    # 9.조회 get id값으로 !get_all 보내면 전체 조회 특정 아이디 보내면 해당 아이디 정보 반환
    def get(self, request):
        data = json.loads(request.body)

        if User.objects.filter(user_phone = data['user_phone']).exists():
            user_data = User.objects.get(user_phone = data['user_phone'])
            return JsonResponse({'users':user_data}, status=200)
        
        else:
            return JsonResponse({'message' : "INVALID_KEYS"},status=400) 
        

class FindPwView(View):
    # 1.post방식으로 요청할 경우 회원가입한다.
    def get(self, request):
        # 2.data에 request에 담긴 정보를 넣어준다
        data = json.loads(request.body)

        try :
            if User.objects.filter(user_id = data['user_id']).exists():
                user_data = User.objects.get(user_id = data['user_id'])
                if user_data.user_phone == data['user_phone']:
                   return JsonResponse({'user_pw':user_data.user_pw}, status=200)
            else:
                return JsonResponse({'message' : "ID NOT EXISTS"},status =400) 

        # 8.예외처리
        except KeyError:
            return JsonResponse({'message' : "INVALID_KEYS"},status =400) 
               