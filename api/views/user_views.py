from rest_framework.response import Response
from rest_framework.views import APIView

from ..decorators.response import response_handler
from ..utils.request_utils import check_not_none
from ..utils.token_utils import AccessToken, check_res_to_error


class ProfileAPIView(APIView):
    @response_handler
    def get(self, request) -> Response:
        token_req = request.data.get("accessToken", "")
        check_not_none((token_req, "token"))
        token = AccessToken(token_value=token_req)
        check_res = token.check()
        if check_res.__class__ != int:
            user = check_res
            response_data = {
                "nickname": user.nickname,
                "profileImg": user.profile_img,
                "info": user.info,
            }
            return Response(response_data, status=201)  # Return profile info
        else:
            return Response(
                check_res_to_error(result_code=check_res), status=401
            )  # Return token error

