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
    
    
class IsAdminOrOwner(BasePermission):
    SAFE_METHODS = ['POST', 'GET', 'PATCH', 'PUT', 'DELETE']
    def has_permission(self, request, view):
        user = CustomUser.objects.get(email=request.user)
        print(user)
        if request.method in self.SAFE_METHODS and not user.is_verified or user != request.user:
            return False
        return True