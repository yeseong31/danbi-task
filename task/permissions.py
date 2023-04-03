from rest_framework import permissions


class CustomReadOnly(permissions.BasePermission):
    """커스텀 권한
    Task 조회: 누구나
    Task 생성: 로그인 한 사용자
    Task 수정 및 삭제: 글 작성자
    """

    def has_permission(self, request, view):
        """전체 객체에 대한 권한"""
        if request.method == 'GET':
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """객체별 권한"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.create_user == request.user
