from rest_framework import permissions
from bank.models import Account


class IsOwnerOrNoAccess(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.account.user == request.user
