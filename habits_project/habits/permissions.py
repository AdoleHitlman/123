from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешить GET, HEAD, OPTIONS запросы всем пользователям
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешить только владельцу доступ к привычке для остальных методов
        return obj.user == request.user

class IsPublicOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешить только GET запросы всем пользователям
        if request.method == 'GET':
            return True

        # Запретить остальные методы для публичных привычек
        return not obj.is_public