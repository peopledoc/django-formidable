from rest_framework.permissions import BasePermission


class NoOne(BasePermission):

    def has_permission(self, *args, **kwargs):
        return False
