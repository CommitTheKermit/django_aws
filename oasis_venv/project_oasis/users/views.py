from django.shortcuts import render
import json, re, traceback
from django.http            import JsonResponse  
from django.views           import View          
from django.core.exceptions import ValidationError
from django.db.models       import Q                                                                                                                
from .models                import User, EmailCode#, CafeInfo
from django.views.decorators.csrf import csrf_exempt
from .serializer import User_basic_serializer#, Cafe_info_serializer
from .email_verification import email_validate
import random

#로그인
class LoginView(View):
     @csrf_exempt
     def post(self, request):
        data = json.loads(request.body)

        try:
            request_email = data.get('user_email')
            request_password = data.get('user_pw')

            id = User.objects.filter(user_email = request_email)
            if id.exists():
                account = User.objects.get(user_email = request_email)
                if account.user_pw == request_password:
                    serialzer = User_basic_serializer(account)
                    return JsonResponse(serialzer.data, status=200)
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
        print(data)
        try :
            if User.objects.filter(user_email = data['user_email']).exists() or\
                User.objects.filter(user_phone = data['user_phone']).exists():
                return JsonResponse({'message' : "email or phone ALREADY EXISTS"},status =400) 
            
            User(
                user_email    = data['user_email'],
                user_pw    = data['user_pw'],
                user_name = data['user_name'],
                user_phone = data['user_phone'],
                user_type = data['user_type'],
                user_sex = data['user_sex'],
                user_age = data['user_age'],
                user_nickname = data['user_nickname']
            ).save()
            #7.성공적으로 저장이 되었으면 성공 메시지를 보낸다.  
            return JsonResponse({'message':'회원가입 성공'}, status=200)

        # 8.예외처리
        except KeyError:
            return JsonResponse({'message' : "INVALID_KEYS"},status =400) 

    # 9.조회 get id값으로 !get_all 보내면 전체 조회 특정 아이디 보내면 해당 아이디 정보 반환
    def get(self, request, bid):
        if bid == "!get_all":
            user_data = User.objects.values()
            return JsonResponse({'users':list(user_data)}, status=200)
        
        else:
            if User.objects.filter(user_email = bid).exists():
                account = User.objects.get(user_email = bid)
                # serializer = User_basic_serializer(account)
                return JsonResponse({"user_email" : account.user_email}, status= 200)
            else:
                return JsonResponse({'message' : "INVALID_KEYS"},status=400)

#이메일 찾기   
class FindEmailView(View):
    # 9.조회 get id값으로 !get_all 보내면 전체 조회 특정 아이디 보내면 해당 아이디 정보 반환
    def post(self, request):
        data = json.loads(request.body)

        if User.objects.filter(user_phone = data['user_phone']).exists():
            user_data = User.objects.get(user_phone = data['user_phone'])
            return JsonResponse({'user_email': user_data.user_email}, status=200)
        
        else:
            return JsonResponse({'message' : "INVALID_KEYS"},status=400) 
        
#비번 찾기
class FindPwView(View):
    # 1.post방식으로 요청할 경우 회원가입한다.
    def post(self, request):
        # 2.data에 request에 담긴 정보를 넣어준다
        data = json.loads(request.body)

        try :
            if User.objects.filter(user_email = data['user_email']).exists():
                user_data = User.objects.get(user_email = data['user_email'])
                if user_data.user_phone == data['user_phone']:
                   return JsonResponse({'user_pw':user_data.user_pw}, status=200)
            else:
                return JsonResponse({'message' : "ID NOT EXISTS"},status =400) 

        # 8.예외처리
        except KeyError:
            return JsonResponse({'message' : "INVALID_KEYS"},status =400) 
        
class EmailSendView(View):
    def post(self, request):
        data = json.loads(request.body)
        code = random.sample(range(10), 6)
        code = ''.join(map(str,code))
        try:
            existFlag = EmailCode.objects.filter(user_email = data['user_email']).exists()
            if not existFlag:
                EmailCode(
                    user_email    = data['user_email'],
                    user_code     = code
                ).save()
                
                try:
                    email_validate(data['user_email'], code)
                    return JsonResponse({'message':"mail sent successfully"}, status=200)
                except:
                    return JsonResponse({'message' : "MAIL ERROR"},status =400) 
            elif existFlag:
                email_code = EmailCode.objects.get(user_email = data["user_email"])
                email_code.delete()

                EmailCode(
                    user_email    = data['user_email'],
                    user_code     = code
                ).save()
                try:
                    email_validate(data['user_email'], code)
                    return JsonResponse({'message':"mail sent again"}, status=200)
                except:
                    return JsonResponse({'message' : "MAIL ERROR"},status =400) 
        except:
            return JsonResponse({'message' : "INVALID_KEYS"},status =400)
        
class EmailVerifyView(View):
    def post(self, request):
        print("shit")
        data = json.loads(request.body)

        try:
           if EmailCode.objects.filter(user_email = data["user_email"]).exists():
                email_code = EmailCode.objects.get(user_email = data["user_email"])
                try:
                    if email_code.user_code == data["user_code"]:
                        email_code.delete()
                        return JsonResponse({'message':"verifiation successful"}, status=200)
                    else:
                        return JsonResponse({'message' : "VERIFY ERROR"},status =400) 
                except:
                    return JsonResponse({'message' : "VERIFY ERROR"},status =400) 

        except:
            return JsonResponse({'message' : "INVALID_KEYS"},status =400)
        
# class CafeInfoView(View):
#     def post(self, request):
#         print(request)
#         data = json.loads(request.body)

#         try:
#            if CafeInfo.objects.filter(cafe_id = data['cafe_id']).exists():
#                 cafe_info = CafeInfo.objects.get(cafe_id = data['cafe_id'])
#                 try:
#                     serialzer = Cafe_info_serializer(cafe_info)
#                     return JsonResponse(serialzer.data, status=200)

#                 except:
#                     return JsonResponse({'message' : "RETURN ERROR"},status =400) 
#            else:
#             return JsonResponse({'message' : "NONE EXIST ERROR"},status =400) 
#         except:
#             return JsonResponse({'message' : "INVALID_KEYS"},status =400)