def check_not_none(*args):
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
