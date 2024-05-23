from datetime import datetime, timedelta, timezone
from typing import Self
from icecream import ic

from django.conf import settings
from jwt import decode, encode

from ..models import Sessions, User
from ..serializers import SessionsSerializer
from .session_utils import session_update, session_delete
from .user_utils import authenticate_user

KEY = settings.JWT_KEY


class Token:
    @classmethod
    def __init__(self: Self, token_value: str) -> None:
        """
        Initializes a token with the provided value

        Parameters:
            token_value (str): The value of the token

        Returns:
            None

        Raises:
            None
        """
        self.value = token_value

    @classmethod
    def create(self: Self, user: User) -> None:
        """
        Creates a new token for the specified user

        Parameters:
            user (User): The user for whom the token is being created

        Returns:
            None

        Raises:
            None
        """
        creation_time = datetime.utcnow().replace(tzinfo=timezone.utc)
        expiration_time = self._set_expiration_time(
            token_type=self.__name__, creation_time=creation_time, user_id=user.id
        )
        payload = {
            "token_type": self.__name__,
            "user_id": user.id,
            "created": creation_time.isoformat(),
            "expired": expiration_time.isoformat(),
        }
        self.value = encode(payload=payload, key=KEY, algorithm="HS256")

    @classmethod
    def check(self: Self) -> User | int:
        """
        Checks the validity of the token and returns the associated user if valid

        Returns:
            User or int: The associated user if token is valid, otherwise an error code

        Raises:
            None
        """
        try:
            decoded_content = decode(jwt=self.value, key=KEY, algorithms=["HS256"])
            expiration_time_str = decoded_content.get("expired", None)
            expiration_time = datetime.fromisoformat(expiration_time_str[:-6]).replace(
                tzinfo=timezone.utc
            )
            current_time = datetime.utcnow().replace(tzinfo=timezone.utc)
            real_type = decoded_content.get("token_type", None)

            if expiration_time is not None and current_time > expiration_time:
                return -3  # Token expired

            real_type = decoded_content.get("token_type")
            if self.__name__ != real_type:
                return -1  # Token invalid

            user_id = decoded_content.get("user_id")
            creation_date_str = decoded_content.get("created")
            user = authenticate_user(user_id=user_id)
            if user:
                if self.__name__ == "RefreshToken":
                    return self._validate_refresh_token(
                        user=user, creation_date_str=creation_date_str
                    )
                elif self.__name__ == "AccessToken":
                    return user  # Token valid

            return -1  # Token invalid
        except Exception as e:
            ic(e)
            return -1  # Token invalid

    def _set_expiration_time(
        token_type: str, creation_time: datetime, user_id: int
    ) -> datetime:
        """
        Sets the expiration time for the token based on its type

        Parameters:
            token_type (str): The type of the token
            creation_time (datetime): The creation time of the token
            user_id (int): The ID of the user associated with the token

        Returns:
            datetime: The expiration time of the token

        Raises:
            Exception: If an invalid token type is given
        """
        if token_type.startswith("A"):  # ? Access token
            expiration_time = creation_time + timedelta(
                minutes=settings.ACCESS_TOKEN_PERIOD
            )
        elif token_type.startswith("R"):  # ? Refresh token
            expiration_time = creation_time + timedelta(
                days=settings.REFRESH_TOKEN_PERIOD
            )
            session_update(creation_time=creation_time, user_id=user_id)
        else:
            raise Exception("Invalid token_type given")
        return expiration_time

    def _validate_refresh_token(user: User, creation_date_str: str) -> User | Exception:
        """
        Validates the refresh token

        Parameters:
            user (User): The user associated with the refresh token
            creation_date_str (str): The creation date of the token in string format

        Returns:
            User or Exception: The associated user if token is valid, otherwise an error

        Raises:
            None
        """
        try:
            session = Sessions.objects.get(user=user.id)
            session_created = session.created_at
            creation_date = datetime.fromisoformat(creation_date_str[:-6]).replace(
                tzinfo=timezone.utc
            )

            # session_created = session_created.replace(microsecond=0)
            # creation_date = creation_date.replace(microsecond=0)
            # if session_created.tzinfo != creation_date.tzinfo:
            #     session_created = session_created.astimezone(timezone.utc)
            #     creation_date = creation_date.astimezone(timezone.utc)
            # session_created = session_created.replace(tzinfo=None)
            # creation_date = creation_date.replace(tzinfo=None)

            if session_created == creation_date:
                return user  # Token valid
            else:
                # return -2  # Token annulled
                return Exception()
        except Sessions.DoesNotExist:
            creation_date = datetime.strptime(creation_date_str, "%Y-%m-%dT%H:%M:%S.%f")
            data = {"user": user, "created_at": creation_date}
            serializer = SessionsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return user  # Token valid
            else:
                return -1  # Token invalid


class RefreshToken(Token):
    value = str

    @classmethod
    def delete(self: Self) -> None:
        """
        Deletes the refresh token and its associated session

        Returns:
            None

        Raises:
            None
        """
        check_res = self.check()
        if check_res.__class__ == int:
            return check_res
        user = check_res
        session_delete(user_id=user.id)


class AccessToken(Token):
    value = str

    @classmethod
    def refresh(self: Self, refresh_token: RefreshToken) -> None | int:
        """
        Refreshes the access token using the provided refresh token

        Parameters:
            refresh_token (RefreshToken): The refresh token to use for refreshing

        Returns:
            None or int: None if the operation is successful, otherwise an error code

        Raises:
            None
        """
        try:
            check_res = refresh_token.check()
            if check_res.__class__ != int:
                user = check_res
                access_token = AccessToken
                access_token.create(user=user)
                self.value = access_token.value
                return None
            else:
                return check_res
        except Exception as e:
            return -1


def to_message(result_code: int) -> str:
    """
    Converts the result code into an error message

    Parameters:
        result_code (int): The result code indicating the error

    Returns:
        str: The corresponding error message

    Raises:
        None
    """
    error_message = ""
    match result_code:
        case -3:
            error_message = "Token is expired"
        case -1:
            error_message = "Token is invalid"
        case -2:
            error_message = "Token was annulled"
    return error_message
