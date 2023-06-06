from django.http            import JsonResponse  
from django.views           import View          
from django.core.exceptions import ValidationError
from django.db.models       import Q                                                                                                                
from django.views.decorators.csrf import csrf_exempt

from .models                import Customer, EmailCode, UserKeywords
from .serializer import Customer_basic_serializer
from .email_verification import email_validate

import random
import json

#로그인
class LoginView(View):
     @csrf_exempt
     def post(self, request):
        data = json.loads(request.body)

        try:
            request_email = data.get('email')
            request_password = data.get('pasword')

            id = Customer.objects.filter(email = request_email)
            if id.exists():
                account = Customer.objects.get(email = request_email)
                if account.password == request_password:
                    serialzer = Customer_basic_serializer(account)
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
            if Customer.objects.filter(email = data['email']).exists() or\
                Customer.objects.filter(phone_no = data['phone_no']).exists():
                return JsonResponse({'message' : "email or phone ALREADY EXISTS"},status =400) 
            
            Customer(
                email    = data['email'],
                password    = data['password'],
                name = data['name'],
                phone_no = data['phone_no'],
                user_type = data['user_type'],
                sex = data['sex'],
                age = data['age'],
                nickname = data['nickname']
            ).save()
            #7.성공적으로 저장이 되었으면 성공 메시지를 보낸다.  
            return JsonResponse({'message':'회원가입 성공'}, status=200)

        # 8.예외처리
        except KeyError:
            return JsonResponse({'message' : "INVALID_KEYS"},status =400) 

    # 9.조회 get id값으로 !get_all 보내면 전체 조회 특정 아이디 보내면 해당 아이디 정보 반환
    def get(self, request):
        reqString = request.GET.get('email', None)
        if reqString == "!get_all":
            user_data = Customer.objects.values()
            return JsonResponse({'users':list(user_data)}, status=200)
        
        else:
            if Customer.objects.filter(email = reqString).exists():
                account = Customer.objects.get(email = reqString)
                # serializer = User_basic_serializer(account)
                return JsonResponse({"email" : "exist"}, status= 200)
            else:
                return JsonResponse({'message' : "INVALID_KEYS"},status=400)

#이메일 찾기   
class FindEmailView(View):
    # 9.조회 get id값으로 !get_all 보내면 전체 조회 특정 아이디 보내면 해당 아이디 정보 반환
    def post(self, request):
        data = json.loads(request.body)

        if Customer.objects.filter(phone_no = data['phone_no']).exists():
            user_data = Customer.objects.get(phone_no = data['user_phone'])
            return JsonResponse({'email': user_data.email}, status=200)
        
        else:
            return JsonResponse({'message' : "INVALID_KEYS"},status=400) 
        
#비번 찾기
class FindPwView(View):
    # 1.post방식으로 요청할 경우 회원가입한다.
    def post(self, request):
        # 2.data에 request에 담긴 정보를 넣어준다
        data = json.loads(request.body)

        try :
            if Customer.objects.filter(email = data['email']).exists():
                user_data = Customer.objects.get(email = data['email'])
                if user_data.phone_no == data['phone_no']:
                   return JsonResponse({'password':user_data.password}, status=200)
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
            existFlag = EmailCode.objects.filter(user_email = data['email']).exists()
            if not existFlag:
                EmailCode(
                    user_email    = data['email'],
                    user_code     = code
                ).save()
                
                try:
                    email_validate(data['email'], code)
                    return JsonResponse({'message':"mail sent successfully"}, status=200)
                except:
                    return JsonResponse({'message' : "MAIL ERROR"},status =400) 
            elif existFlag:
                email_code = EmailCode.objects.get(user_email = data["email"])
                email_code.delete()

                EmailCode(
                    user_email    = data['email'],
                    user_code     = code
                ).save()
                try:
                    email_validate(data['email'], code)
                    return JsonResponse({'message':"mail sent again"}, status=200)
                except:
                    return JsonResponse({'message' : "MAIL ERROR"},status =400) 
        except:
            return JsonResponse({'message' : "INVALID_KEYS"},status =400)
        
class EmailVerifyView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
           if EmailCode.objects.filter(user_email = data["email"]).exists():
                email_code = EmailCode.objects.get(user_email = data["email"])
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
        
class EditProfileView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            existFlag = Customer.objects.filter(email = data['email']).exists()
            if existFlag:
                customer = Customer.objects.get(email = data["email"])
                customer.delete()
                try:
                    Customer(
                        email    = data['email'],
                        password    = data['password'],
                        name = data['name'],
                        phone_no = data['phone_no'],
                        user_type = data['user_type'],
                        sex = data['sex'],
                        age = data['age'],
                        nickname = data['nickname']
                    ).save()
                    return JsonResponse({'message':"register success"}, status=200)
                except:
                    return JsonResponse({'message' : "REGISTER ERROR"},status =400) 
        except:
            return JsonResponse({'message' : "INVALID_KEYS"},status =400)
        
class CreateUserKeywords(View):
    def post(self, request):
        data = json.loads(request.body)
        user_keyword_value = list(data['user_keyword_value'])

        user = Customer.objects.filter(email = data['email'])
        if user.exists():
            user = user[0]
            if not UserKeywords.objects.filter(user_id = user).exists():
                UserKeywords.objects.create(
                    user_id=user,
                    beverage=user_keyword_value[0],
                    dessert=user_keyword_value[1],
                    various_menu=user_keyword_value[2],
                    special_menu=user_keyword_value[3],
                    large_store=user_keyword_value[4],
                    background=user_keyword_value[5],
                    talking=user_keyword_value[6],
                    concentration=user_keyword_value[7],
                    trendy_store=user_keyword_value[8],
                    gift_packaging=user_keyword_value[9],
                    parking=user_keyword_value[10],
                    price=user_keyword_value[11]
                )

                return JsonResponse({'message': "User Keywords Created Successfully"}, status=200)
            else:
                return JsonResponse({'message' : "User keywords already exist"},status =400)
        else:
            return JsonResponse({'message' : "INVALID_KEYS"},status =400)

        # try:
        #     user_id = Customer.objects.get(email = data['email'])
        #     if not UserKeywords.objects.get(user_id = user_id).exists():
        #             try:
        #                 UserKeywords.objects.create(
        #                     user_id=user_id,
        #                     beverage=data.get('beverage'),
        #                     dessert=data.get('dessert'),
        #                     various_menu=data.get('various_menu'),
        #                     special_menu=data.get('special_menu'),
        #                     large_store=data.get('large_store'),
        #                     background=data.get('background'),
        #                     talking=data.get('talking'),
        #                     concentration=data.get('concentration'),
        #                     trendy_store=data.get('trendy_store'),
        #                     gift_packaging=data.get('gift_packaging'),
        #                     parking=data.get('parking'),
        #                     price=data.get('price')
        #                 )

        #                 return JsonResponse({'message': "User Keywords Created Successfully"}, status=200)
        #             except:
        #                 return JsonResponse({'message' : "Create User Keywords ERROR"},status =400)
        #     else:
        #         return JsonResponse({'message' : "User keywords already exist"},status =400)
                        
        # except:
        #     return JsonResponse({'message' : "INVALID_KEYS"},status =400)


class UpdateUserKeywords(View):
    def post(self, request):
        data = json.loads(request.body)
        user_keyword_value = list(data['user_keyword_value'])

        # Check if customer exists
        user = Customer.objects.filter(email=data['email'])
        if not user.exists():
            return JsonResponse({'message': 'INVALID_KEYS'}, status=400)

        # Check if UserKeywords exists
        try:
            user_keywords = UserKeywords.objects.get(user_id=user[0])
        except UserKeywords.DoesNotExist:
            return JsonResponse({'message': 'UserKeywords does not exist'}, status=400)

        # Update fields from request
        user_keyword_attribute = ['beverage', 'dessert', 'various_menu', 'special_menu', 'large_store', 'background', 'talking', 'concentration', 'trendy_store', 'gift_packaging', 'parking', 'price']
        for idx in range(len(user_keyword_attribute)):
            setattr(user_keywords, user_keyword_attribute[idx], user_keyword_value[idx])

        # Save the updated instance
        user_keywords.save()

        return JsonResponse({'message': 'UserKeywords updated successfully'}, status=200)

        # try:
        #     existFlag = Customer.objects.filter(email = data['email']).exists()
        #     if existFlag:
        #         user_keywords = UserKeywords.objects.get(user_id = data['user_id'])
                
        #         try:
        #             # Update fields from request
        #             user_keywords.beverage = data['beverage']
        #             user_keywords.dessert = data['dessert']
        #             user_keywords.various_menu = data['various_menu']
        #             user_keywords.special_menu = data['special_menu']
        #             user_keywords.large_store = data['large_store']
        #             user_keywords.background = data['background']
        #             user_keywords.talking = data['talking']
        #             user_keywords.concentration = data['concentration']
        #             user_keywords.trendy_store = data['trendy_store']
        #             user_keywords.gift_packaging = data['gift_packaging']
        #             user_keywords.parking = data['parking']
        #             user_keywords.price = data['price']

        #             # Save the updated instance
        #             user_keywords.save()
        #             return JsonResponse({'message': 'UserKeywords updated successfully'}, status=200)
        #         except:
        #             return JsonResponse({'message' : "UserKeywords updated ERROR"},status =400)
        # except:
        #     return JsonResponse({'message' : "INVALID_KEYS"},status =400)

            
class isKeywordExist(View):
    def post(self, request):
        # Check if customer exists
        data = json.loads(request.body)
        user = Customer.objects.filter(email=data['email'])
        if not user.exists():
            return JsonResponse({'message': 'INVALID_KEYS'}, status=400)

        # Check if UserKeywords exists
        try:
            user_keywords = UserKeywords.objects.get(user=user.user_id)
            return JsonResponse({'message': 'UserKeywords exist'}, status=200)
        except UserKeywords.DoesNotExist:
            return JsonResponse({'message': 'UserKeywords does not exist'}, status=400)



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