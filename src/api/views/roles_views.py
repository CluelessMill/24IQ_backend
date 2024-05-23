from rest_framework.response import Response
from rest_framework.views import APIView

from ..decorators.response import response_handler
from ..models import User
from ..utils.cript_utils import decrypt, encrypt
from ..utils.request_utils import check_not_none
from ..utils.token_utils import AccessToken, to_message


class RoleListAPIView(APIView):
    @response_handler
    def get(self, request) -> Response:
        token_req: str = request.COOKIES.get("accessToken")
        check_not_none((token_req, "accessToken"))

        token = AccessToken(token_value=token_req)
        check_res: User = token.check()
        if check_res.__class__ == int:
            return Response(
                data={"message": to_message(result_code=check_res)}, status=400
            )
        user_role = check_res.role
        if user_role != "admin":
            return Response(data={"message": "You don't have a permission"}, status=400)
        users = User.objects.all()
        response_data = []
        for user in users:
            response_data.append(
                {
                    "email": decrypt(data=user.email),
                    "nickname": decrypt(data=user.nickname),
                    "role": user.role,
                }
            )
        return Response(data=response_data, status=200)


class RoleSetAPIView(APIView):
    @response_handler
    def put(self, request) -> Response:
        nickname: str = request.data.get("nickname", "")
        token_req: str = request.COOKIES.get("accessToken")
        new_role: str = request.data.get("role", "")
        check_not_none((nickname, "nickname"), (token_req, "token"), (new_role, "role"))

        token = AccessToken(token_value=token_req)
        check_res: int | User = token.check()
        if check_res.__class__ == int:
            return Response(
                data={"message": to_message(result_code=check_res)}, status=400
            )
        user_role = check_res.role
        if user_role != "admin":
            return Response(data={"message": "You don't have a permission"}, status=400)
        try:
            user = User.objects.get(nickname=encrypt(data=nickname))
            user.role = new_role
            user.save()
        except User.DoesNotExist:
            return Response(data={"message": "User not found"}, status=404)
        return Response(data={"message": "Success"}, status=201)


class IsAdminAPIView(APIView):
    @response_handler
    def get(self, request) -> Response:
        token_req: str = request.COOKIES.get("accessToken")
        check_not_none((token_req, "accessToken"))

        token = AccessToken(token_value=token_req)
        check_res: int | User = token.check()
        if check_res.__class__ == int:
            return Response(
                data={"message": to_message(result_code=check_res)}, status=400
            )
        user_role = check_res.role
        return Response(data={"isAdmin": user_role == "admin"}, status=200)


class RoleSetDEBUGAPIView(APIView):  #! This must be removed in production
    @response_handler
    def put(self, request) -> Response:
        nickname: str = request.data.get("nickname", "")
        new_role: str = request.data.get("role", "")
        check_not_none((nickname, "nickname"), (new_role, "role"))

        try:
            user: User = User.objects.get(nickname=encrypt(data=nickname))
            user.role = new_role
            user.save()
        except User.DoesNotExist:
            return Response(data={"message": "User not found"}, status=404)
        return Response(data={"message": "Success"}, status=201)
