from rest_framework.permissions import BasePermission
from .models import CustomUser

class IsAdmin(BasePermission):
    SAFE_METHODS = ['POST', 'GET', 'PATCH', 'PUT', 'DELETE']
    def has_permission(self, request, view):
        user = CustomUser.objects.get(email=request.user)
        if request.method in self.SAFE_METHODS and not user.is_admin:
            return False
        return True

class IsVerified(BasePermission):
    SAFE_METHODS = ['POST', 'GET', 'PATCH', 'PUT', 'DELETE']
    def has_permission(self, request, view):
        print(request.user)
        user = CustomUser.objects.get(email=request.user)
        if request.method in self.SAFE_METHODS and not user.is_verified:
            return False
        return True
    
class IsOwner(BasePermission):
    SAFE_METHODS = ['POST', 'GET']
    def has_permission(self, request, view):
        print(f'request object {request}')
        user = CustomUser.objects.get(email=request.user)
        if request.method in self.SAFE_METHODS:
            if str(request.user) != str(user.email):
                return False
        return True