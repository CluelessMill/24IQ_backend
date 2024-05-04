from rest_framework.response import Response
from rest_framework.views import APIView

from ..decorators.response import response_handler
from ..models import User
from ..utils.cript_utils import decrypt, encrypt
from ..utils.request_utils import check_not_none
from ..utils.roles_utils import admin_check
from ..utils.token_utils import AccessToken


class RoleListAPIView(APIView):
    @response_handler
    def get(self, request) -> Response:
        users = User.objects.all()
        response_data = []
        for user in users:
            response_data.append(
                {
                    "email": decrypt(user.email),
                    "nickname": decrypt(user.nickname),
                    "role": user.role,
                }
            )
        return Response(data=response_data)

    @response_handler
    def put(self, request) -> Response:
        nickname = request.data.get("nickname", "")
        token_req = request.data.get("token", "")
        new_role = request.data.get("role", "")
        check_not_none((nickname, "nickname"), (token_req, "token"), (new_role, "role"))

        token = AccessToken(token_value=token_req)
        # ! TOKEN CHECK FUNC
        is_admin = admin_check(token=token)
        if is_admin:
            try:
                user = User.objects.get(nickname=encrypt(data=nickname))
                user.role = new_role
                user.save()
            except User.DoesNotExist:
                return Response(data={"message": "User not found"}, status=404)
            return Response(data={"message": "Success"}, status=200)
        else:
            return Response(data={"message": "You don't have permission"}, status=400)


class IsAdminAPIView(APIView):
    @response_handler
    def post(self, request) -> Response:
        token_req = request.data.get("token", "")
        check_not_none((token_req, "token"))
        token = AccessToken(token_value=token_req)
        response = {"isAdmin": admin_check(token=token)}
        return Response(data=response)
