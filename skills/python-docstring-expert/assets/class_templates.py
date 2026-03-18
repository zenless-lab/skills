class PublicEntity:
    """Represents a public entity handling specific domain logic.

    This class provides methods to interact with the entity. Note that constructor
    parameters are documented here in the class docstring, not in `__init__`.

    Args:
        name (str): The name of the entity.
        identifier (int): A unique identifier for the entity.

    Attributes:
        is_active (bool): Indicates if the entity is currently active.
    """

    def __init__(self, name: str, identifier: int):
        self.name = name
        self.identifier = identifier
        self.is_active = True


class SimpleDataContainer:
    """A simple container for generic data payloads."""
    # Simple classes don't need extensive multi-line docstrings if their
    # attributes are obvious or well-typed.
    pass
