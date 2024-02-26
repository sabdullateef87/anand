from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet


router = DefaultRouter()
# router.register(r'users', UserViewSet)

user_detail = UserViewSet.as_view({'get': 'retrieve'})
user_list_update = UserViewSet.as_view({'get':'list', 'patch':'update_user', 'post':'create'})
user_verify = UserViewSet.as_view({'get':'verify'})
user_login = UserViewSet.as_view({'post':'login'})


urlpatterns = [
    # path('', include(router.urls)),
    path('users/<str:pk>', user_detail, name='user-detail'),
    path('users', user_list_update, name='user-list'),
    path('users/verify', user_verify, name='user-verify'),
    path('user/login', user_login, name='user-login'),


    # path('user/register', UserCreateView.as_view()),
    # path('user/verify_email', VerifyEmail.as_view()),
    # path('user/login', Login.as_view()),
    # path('user/dummy', DummyAuthView.as_view()),
    # path('logout', LogoutView.as_view()),
    # path('user/details', GetUserDetails.as_view())
]

