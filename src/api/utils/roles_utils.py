from ..models import User


def admin_check(user: User) -> bool:
    return user.role == "admin"
