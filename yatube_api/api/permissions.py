from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """
    Пользовательское разрешение,
    позволяющее только владельцам объекта редактировать его.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
