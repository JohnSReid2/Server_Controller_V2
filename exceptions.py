
class UserError(Exception):
    """Base class for user-related errors."""
    pass

class UserAlreadyExists(UserError):
    """Raised when trying to create a user that already exists."""
    pass

class UserNotFound(UserError):
    """Raised when user lookup fails."""
    pass

class AuthenticationError(UserError):
    """Raised when login credentials are invalid."""
    pass

class ServerCommandError(Exception):
    """Raised when a remote SSH command or control fails."""
    pass