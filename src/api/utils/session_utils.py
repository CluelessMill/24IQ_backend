from datetime import datetime

from ..models import Sessions
from ..serializers import SessionsSerializer


def session_update(creation_time: datetime, user_id: int) -> None | str:
    """
    Updates or creates a session for the specified user

    Parameters:
        creation_time (datetime): The creation time of the session
        user_id (int): The ID of the user

    Returns:
        None or str: None if the operation is successful, otherwise an error message

    Raises:
        Exception: If serializer validation fails
    """
    existing_session = Sessions.objects.filter(user=user_id).first()

    if existing_session:
        existing_session.created_at = creation_time
        serializer = SessionsSerializer(
            instance=existing_session,
            data={"created_at": creation_time, "user": user_id},
        )
    else:
        session_data = {"created_at": creation_time, "user": user_id}
        serializer = SessionsSerializer(data=session_data)
    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)


def session_delete(user_id: int) -> None:
    """
    Deletes the session associated with the specified user

    Parameters:
        user_id (int): The ID of the user

    Returns:
        None

    Raises:
        None
    """
    existing_session = Sessions.objects.filter(user=user_id).first()
    if existing_session:
        existing_session.delete()
    return 0
