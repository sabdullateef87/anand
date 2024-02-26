from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken

from .userdto import UserResponse
from .models import CustomUser
from .serializers import UserSerializer
from django.contrib.sites.shortcuts import get_current_site
from .utils import Utils
from .permissions import IsAdminOrOwner, IsVerified, IsAdmin
import jwt
from django.conf import settings
from rest_framework.decorators import action


from django.utils.translation import gettext_lazy as _
from rest_framework import status, viewsets


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
    def get_object(self, email):
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return False
    
    def create(self, request, *args, **kwargs):
        request_body = request.data
        serialized_request_body = UserSerializer(data=request_body)
        if serialized_request_body.is_valid():
            try:
                serialized_request_body.save()
                new_user = self.get_object(serialized_request_body.validated_data["email"])
                confirmation_token = RefreshToken.for_user(new_user).access_token
                current_site_url = get_current_site(request)
                # activation_link = f"http://{current_site_url}/user/verify_email?confirmation_token={confirmation_token}&user_id={new_user.id}"
                response = UserResponse(new_user.email, new_user.first_name, new_user.last_name).json()
                # Utils.sendMail(data)
                return Response(response, status=200)
            except ValidationError as ve:
                return Response(ve, status=400)
        return Response(serialized_request_body.errors, status=400)
    
    
    def retrieve(self, request, pk):     
        
        user = self.get_object(email=pk)
        if user:
            response = UserResponse(user.email, user.first_name, user.last_name, user.is_verified).json()
            return Response(response, status=202)
        else:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        user_list = []
        for item in self.queryset:
            user_list.append(UserResponse(item.email, item.first_name, item.last_name, item.is_verified).json())
        return Response(user_list, status=200)
    
    def update_user(self, request, **kwargs):
        request_body = request.data
        email = request_body.get("email")
        instance = self.get_object(email=email)
        serializer = UserSerializer(instance, data=request_body, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                updated_user = self.get_object(
                    serializer.validated_data["email"]
                )
                response = UserResponse(updated_user.email, updated_user.first_name, updated_user.last_name, updated_user.is_verified).json()
                return Response(response, status=200)
            except Exception as e:
                return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=400)
    
    # def partial_update(self, request, *args, **kwargs):
    #     return super().partial_update(request, *args, **kwargs)
        

    @action(detail=True, methods=['get'])
    def verify(self, request, *args, **kwargs):
        confirmation_token = request.query_params.get("confirmation_token")
        id = int(request.query_params.get("user_id"))

        decoded_token = jwt.decode(confirmation_token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_token.get("user_id")
        user = self.get_object(pk=user_id)
        if not user:
            return Response({"message": "user not found"}, status=400)
        print(user_id, id, type(user_id), type(id))
        if user_id != id:
            return Response({"message": "User token is invalid, proceed to login"}, status=400)
        user.is_verified = True
        user.save()
        return Response({"message": "User Verified Successfully, Proceed to login"})
        
    
    def login(self, request, *args, **kwargs):
        request_body = request.data
        try:
            user = Utils.validate_login_parameters(request_body, CustomUser)
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            serializer = UserSerializer(user)
            return Response(
                {
                    "data": serializer.data,
                    "access_token": f"{access_token}",
                    "refresh_token": f"{refresh}",
                },
                status=200,
            )
        except ValueError as err:
            return Response({"message": str(err)}, status=400)
        
        
    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticated(), IsAdmin()]
        elif self.action == 'retrieve':
            return [IsAuthenticated(), IsAdminOrOwner()]
        else:
            return []
    

# class UserCreateView(APIView):
#     def get_object(self, email, Model=None, **kwargs):
#         try:
#             return CustomUser.objects.get(email=email)
#         except CustomUser.DoesNotExist:
#             return False

#     def post(self, request, *args, **kwargs):
#         request_body = request.data
#         serialized_request_body = UserSerializer(data=request_body)

#         if serialized_request_body.is_valid():
#             try:
#                 serialized_request_body.save()
#                 new_user = self.get_object(
#                     serialized_request_body.validated_data["email"]
#                 )
#                 confirmation_token = RefreshToken.for_user(new_user).access_token
#                 current_site_url = get_current_site(request)
#                 # activation_link = f"http://{current_site_url}/user/verify_email?confirmation_token={confirmation_token}&user_id={new_user.id}"


#                 response = UserResponse(new_user.email, new_user.first_name, new_user.last_name).json()
#                 # Utils.sendMail(data)
#                 return Response(response, status=200)
#             except Exception as e:
#                 return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         return Response(serialized_request_body.errors, status=400)
    
#     def put(self, request):
#         request_body = request.data
#         email = request_body.get("email")
#         existing_user = self.get_object(email)
        
#         serialized_request_body = UserSerializer(data=request_body)
#         if serialized_request_body.is_valid():
#             try:
#                 serialized_request_body.save()
#                 response = UserResponse(existing_user.email, existing_user.first_name, existing_user.last_name, existing_user.is_verified).json()
#                 return Response(response, status=200)
#             except Exception as e:
#                 return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         return Response(serialized_request_body.errors, status=400)


# class VerifyEmail(APIView):
#     def get_object(self, pk=None, email=None, Model=None, **kwargs):
#         try:
#             return CustomUser.objects.get(pk=pk)
#         except CustomUser.DoesNotExist:
#             return False

#     def get(self, request, pk=None):
#         confirmation_token = request.query_params.get("confirmation_token")
#         id = int(request.query_params.get("user_id"))

#         decoded_token = jwt.decode(confirmation_token, settings.SECRET_KEY, algorithms=["HS256"])
#         user_id = decoded_token.get("user_id")
#         user = self.get_object(pk=user_id)
#         if not user:
#             return Response({"message": "user not found"}, status=400)
#         print(user_id, id, type(user_id), type(id))
#         if user_id != id:
#             return Response(
#                 {"message": "User token is invalid, proceed to login"}, status=400
#             )
#         user.is_verified = True
#         user.save()
#         return Response({"message": "User Verified Successfully, Proceed to login"})


# class Login(APIView):
#     def post(self, request):
#         request_body = request.data
#         try:
#             user = Utils.validate_login_parameters(request_body, CustomUser)
#             refresh = RefreshToken.for_user(user)
#             access_token = refresh.access_token
#             serializer = UserSerializer(user)
#             return Response(
#                 {
#                     "data": serializer.data,
#                     "access_token": f"{access_token}",
#                     "refresh_token": f"{refresh}",
#                 },
#                 status=200,
#             )
#         except ValueError as err:
#             return Response({"message": str(err)}, status=400)
        
# class GetUserDetails(APIView):
#     def get_object(self, email, Model=None, **kwargs):
#         try:
#             return CustomUser.objects.get(email=email)
#         except CustomUser.DoesNotExist:
#             return False
        
#     def get(self, request, **kwargs):
#         email = request.query_params.get("email")        
#         user = self.get_object(email=email)
#         response = UserResponse(user.email, user.first_name, user.last_name, user.is_verified).json()
#         return Response(response, status=202)
    
    

    
# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh_token"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response(
#                 {"message": "Logged out successfully !"},
#                 status=status.HTTP_205_RESET_CONTENT,
#             )
#         except Exception as e:
#             return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


# class DummyAuthView(APIView):
#     authentication_classes = [SessionAuthentication,BasicAuthentication,JWTAuthentication]
#     permission_classes = [IsAuthenticated, IsAdmin, IsVerified]

#     def get(request, *args, **kwargs):
#         return Response("Hello")
