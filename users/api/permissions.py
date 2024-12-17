from rest_framework import permissions

class IsProfessor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Professores").exists()