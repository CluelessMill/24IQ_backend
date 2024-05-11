def check_not_none(*args) -> None:
    """
    Checks if the provided variables are not None or empty strings

    Parameters:
        *args: Variable-length list of tuples containing the variable and its name

    Returns:
        None

    Raises:
        ValueError: If any of the provided variables are None or empty strings
    """
    empty_vars = []
    for arg, arg_name in args:
        if arg is None:
            empty_vars.append(arg_name)
        elif isinstance(arg, str) and not arg.strip():
            empty_vars.append(arg_name)
    if empty_vars:
        empty_vars_str = ", ".join(empty_vars)
        raise ValueError(
            f"The following variables cannot be None or empty: {empty_vars_str}"
        )
