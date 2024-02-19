from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        return request.user == view.get_object().owner

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsModer(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderator').exists()

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='moderator').exists()


class IsOwnerOrModerator(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='moderator').exists():
            return True

        return obj.owner == request.user
