class EmptyDirectoryException(Exception):
    """
    An Empty Directory Exception.
    """

    def __init__(self, message):
        super().__init__(message)