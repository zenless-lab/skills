def public_function(param1: int, param2: str = "default") -> dict[str, int]:
    """Summary line explaining what the function does (max 80 chars).

    A more detailed description of the function's behavior, its side effects,
    and any important details about its implementation that the caller should
    know. This can span multiple paragraphs.

    Args:
        param1: Describe what param1 represents. If the description spans
            multiple lines, indent the continuation lines by 4 spaces.
        param2: Describe param2. The type is expected to be handled by
            type annotations.

    Returns:
        A dictionary mapping strings to integers, representing the result.
        Do not describe the type again if it is already in the type hint,
        unless explaining internal structure.

    Raises:
        ValueError: If param1 is negative.

    Examples:
        >>> public_function(42, param2="test")
        {'result': 42}
    """
    pass
