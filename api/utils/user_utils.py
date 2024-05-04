from hashlib import sha256

from ..models import User
from .cript_utils import check_password, decrypt, encrypt


def authenticate_user(
    nickname: str = None, user_id: int = None, password: str = None, email: str = None
) -> User | None:
    try:
        user = None
        if nickname is not None and password is not None:
            user = User.objects.get(nickname=encrypt(data=nickname))
            if not check_password(
                input_password=password, stored_password=user.password.tobytes()
            ):
                user = None
        elif email is not None and password is not None:
            user = User.objects.get(email=encrypt(data=email))
            if not check_password(
                input_password=password, stored_password=user.password.tobytes()
            ):
                user = None
        elif nickname is None and email is None:
            user = User.objects.get(id=user_id)

        if not user:
            return None
        user.nickname = decrypt(data=user.nickname.tobytes())
        user.email = decrypt(data=user.email.tobytes())
        return user
    except User.DoesNotExist:
        return None


def check_user(nickname: str, password: str) -> bool:
    try:
        user = User.objects.get(nickname=encrypt(data=nickname))
        return check_password(input_password=password, stored_password=user["password"])
    except User.DoesNotExist:
        return False


def check_is_unique(nickname: str = None, email: str = None) -> bool:
    if email is not None:
        try:
            User.objects.get(email=encrypt(data=email))
            return False
        except User.DoesNotExist:
            return True
    else:
        try:
            User.objects.get(nickname=encrypt(nickname))
            return False
        except User.DoesNotExist:
            return True


def generate_nickname(email: str) -> str:
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"
    hashed_email = sha256(string=email.encode()).hexdigest()
    hashed_email = [(chr(int(i) + 97) if i.isdigit() else i) for i in hashed_email]
    nickname = ""
    for char in hashed_email:
        if len(nickname) >= 15:
            break
        if char in consonants:
            nickname += char
            if len(nickname) < 15:
                nickname += vowels[int(ord(char)) % len(vowels)]
        elif char in vowels:
            nickname += consonants[int(ord(char)) % len(consonants)]
    while len(nickname) < 15:
        nickname += consonants[int(hashed_email[0], base=16) % len(consonants)]

    return nickname
