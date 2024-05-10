from ..models import User
from ..utils.token_utils import AccessToken
from ..utils.user_utils import authenticate_user


def admin_check(token: AccessToken) -> bool | int:
    # ! No need now, replaced by token.check() returned value to optimize process
    pass
