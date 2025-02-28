class AuthorAlreadyExistsError(Exception):
    """Exception raised when an auther already exists in the DB.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
