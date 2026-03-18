def perform_action(action_type: str) -> bool:
    """Execute a specific action based on the provided type.

    This multi-line docstring describes the behavior, parameters, return
    value, and potential exceptions.

    Args:
        action_type (str): The type of action to perform (e.g., 'start').

    Returns:
        bool: True if the action was successful, False otherwise.

    Raises:
        ValueError: If the `action_type` is not recognized.
    """
    if action_type not in ["start", "stop"]:
        raise ValueError(f"Unknown action: {action_type}")
    return True


def calculate_metric(identifier: int) -> int:
    """Calculate and return the basic metric."""
    return identifier * 2


def _private_helper(data: list) -> int:
    # Private APIs with simple logic can just use standard comments.
    # No docstring needed if it's self-explanatory.
    return len(data)


def get_name(user_id: int) -> str:
    # If a docstring would just be "Get name by user_id", omit it entirely.
    # The signature self-documents the intent.
    return "Name"
