from hashlib import sha256
from PIL import Image

from ..models import User
from .cript_utils import check_password, decrypt, encrypt
from .functions.generate_image import encode_text_to_image

def authenticate_user(
    nickname: str = None, user_id: int = None, password: str = None, email: str = None
) -> User | None:
    """
    Authenticates a user based on provided credentials

    Parameters:
        nickname (str, optional): The nickname of the user
        user_id (int, optional): The ID of the user
        password (str, optional): The password of the user
        email (str, optional): The email of the user

    Returns:
        User or None: The authenticated user if successful, otherwise None

    Raises:
        None
    """
    try:
        user = None
        if password is not None:
            if nickname is not None:
                encrypted_nickname = encrypt(data=nickname)
                user = User.objects.get(nickname=encrypted_nickname)
            elif email is not None:
                encrypted_email = encrypt(data=email)
                user = User.objects.get(email=encrypted_email)

            if user and not check_password(
                input_password=password, stored_password=user.password.tobytes()
            ):
                return None
        elif user_id is not None:
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
    """
    Checks if the provided nickname or email is unique in the database

    Parameters:
        nickname (str, optional): The nickname to be checked
        email (str, optional): The email to be checked

    Returns:
        bool: True if the nickname or email is unique, otherwise False

    Raises:
        None
    """
    try:
        if email is not None:
            User.objects.get(email=encrypt(data=email))
        else:
            User.objects.get(nickname=encrypt(data=nickname))
        return False
    except User.DoesNotExist:
        return True


def generate_nickname(email: str) -> str:
    """
    Generates a nickname from the provided email

    Parameters:
        email (str): The email used to generate the nickname

    Returns:
        str: The generated nickname

    Raises:
        None
    """
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"
    hashed_email = sha256(string=email.encode()).hexdigest()
    nickname = ""
    is_consonant_turn = True
    for char in hashed_email:
        if len(nickname) >= 15:
            break
        if char.isdigit():
            index = int(char)
        else:
            index = ord(char) % 16
        if is_consonant_turn:
            nickname += consonants[index % len(consonants)]
        else:
            nickname += vowels[index % len(vowels)]
        is_consonant_turn = not is_consonant_turn
    while len(nickname) < 15:
        nickname += consonants[
            int(sha256(string=nickname.encode()).hexdigest()[0], base=16)
            % len(consonants)
        ]
    return nickname

def generate_profile_picture(prompt: str) -> Image.Image:
    image_size = 400
    encoded_image = encode_text_to_image(text=prompt, image_size=image_size)
    return encoded_image
