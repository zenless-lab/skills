class PublicClass:
    """A one-line summary of what the class instance represents.

    Longer class information detailing its purpose, state, and usage.
    Usage examples can be included here or in a separate module docstring.

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.

    Examples:
        >>> instance = PublicClass()
        >>> instance.eggs = 10
    """

    def __init__(self, likes_spam: bool = False):
        """Initializes the instance with the given spam preference.

        Args:
            likes_spam: Defines if the instance exhibits this preference.
        """
        self.likes_spam = likes_spam
        self.eggs = 0
