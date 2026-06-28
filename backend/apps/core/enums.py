"""Enums for all static/choice values across the project.

Using Enums ensures no hard-coded string literals throughout the codebase.
"""

from enum import StrEnum


class PostStatus(StrEnum):
    """Possible states of a blog post."""

    DRAFT = "draft"
    PUBLISHED = "published"


class UserRole(StrEnum):
    """User role types defining access levels."""

    ADMIN = "admin"
    AUTHOR = "author"
    READER = "reader"
