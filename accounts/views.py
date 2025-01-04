
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import generics,status
from rest_framework.views import APIView
from django.contrib.auth import authenticate

from .serializer.signup_serializer import SignUpSerializer
from .controller.tokens import create_jwt_pair_for_user


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request:Request):
        try: 
            data = request.data
            if data :
                serializer = self.serializer_class(data = data)
                if serializer.is_valid():
                    serializer.save()
                    response = {'status': True, 'message': 'Signup successful', 'data': serializer.data}
                    return Response(data=response, status=status.HTTP_201_CREATED)
                else:
                    formatted_errors = ''
                    print(serializer.errors)
                    for field, errors in serializer.errors.items():
                        formatted_errors = f"{errors[0].lower().replace('this', f'{field}')}"
                    response = {'status': False, 'message': formatted_errors, 'data': None}
                    return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {'status': False, 'message': 'No data provided', 'data': None}
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {'status': False, 'message': str(e), 'data': None}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    


class LoginView(APIView):

    permission_classes = []
    def post(self, request:Request):
        try: 
            data = request.data
            if data :
                email = request.data.get("email")
                password = request.data.get('password')
                user = authenticate(email = email, password = password)

                if(user is not None):
                        token = create_jwt_pair_for_user(user)
                        response = {'status': True, 'message': 'Login successful', 'data': {
                            # "user_token": user.auth_token.key,
                            "token": token
                        }}
                        return Response(data=response, status=status.HTTP_200_OK)
                else:
                    response = {'status': False, 'message': "Invalid email or password", 'data': None}
                    return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {'status': False, 'message': 'No data provided', 'data': None}
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            response = {'status': False, 'message': str(e), 'data': None}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request:Request):
        content= {
             "user":str(request.user),
             "auth":str(request.auth)
        }
        return Response(data=content, status=status.HTTP_200_OK)

# Create your views here.
