"""Core shared exceptions raised across all app layers.

All custom exceptions are caught explicitly in the API layer.
"""


class BlogAPIException(Exception):
    """Base exception for all blog API errors."""

    def __init__(self, message: str, status_code: int = 400) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundException(BlogAPIException):
    """Raised when a requested resource is not found."""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, status_code=404)


class PermissionDeniedException(BlogAPIException):
    """Raised when user lacks permission for the requested action."""

    def __init__(self, message: str = "Permission denied") -> None:
        super().__init__(message, status_code=403)


class ValidationException(BlogAPIException):
    """Raised when input validation fails in the service layer."""

    def __init__(self, message: str = "Validation error") -> None:
        super().__init__(message, status_code=400)


class ConflictException(BlogAPIException):
    """Raised when a resource conflict occurs (e.g. duplicate email)."""

    def __init__(self, message: str = "Resource conflict") -> None:
        super().__init__(message, status_code=409)
