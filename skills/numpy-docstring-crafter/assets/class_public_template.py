class PublicClass:
    """
    Short summary describing the class.

    Extended summary giving a few sentences about what the class does.

    Parameters
    ----------
    param_a : int
        Description of `param_a`.

    Attributes
    ----------
    attr_a : int
        Description of the attribute. Usually set by `param_a`.
    attr_b : float
        Another attribute description.

    Methods
    -------
    do_something()
        Description of what this specific method does.
    """

    def __init__(self, param_a):
        self.attr_a = param_a
        self.attr_b = 0.0

    def do_something(self):
        """
        Brief summary of the method.

        Returns
        -------
        int
            Description of the return value.
        """
        return self.attr_a
