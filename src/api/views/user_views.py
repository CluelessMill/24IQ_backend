from rest_framework.response import Response
from rest_framework.views import APIView

from ..decorators.response import response_handler
from ..models import User
from ..utils.request_utils import check_not_none
from ..utils.token_utils import AccessToken, to_message


class ProfileAPIView(APIView):
    @response_handler
    def get(self, request) -> Response:
        token_req: str = request.data.get("accessToken", "")
        check_not_none((token_req, "token"))
        token = AccessToken(token_value=token_req)
        check_res: int | User = token.check()
        if check_res.__class__ != int:
            user: User = check_res
            response_data = {
                "nickname": user.nickname,
                "profileImg": user.profile_img,
                "info": user.info,
            }
            return Response(data=response_data, status=201)
        else:
            return Response(data=to_message(result_code=check_res), status=401)
