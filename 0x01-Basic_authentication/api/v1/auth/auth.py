#!/usr/bin/env python3
"""Authentication module for the API.
"""
from flask import request
from typing import List, TypeVar
import re


class Auth:
    """Authentication class.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if authentication is required for the given path.
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        # Ensure path ends with '/' for consistent comparison
        path = path.rstrip('/') + '/'

        for excluded_path in excluded_paths:
            # Remove trailing slash and add it back with '*' for consistency
            excluded_path = excluded_path.rstrip('/') + '/*'
            if re.match(excluded_path.replace('*', '.*') + '$', path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Gets the authorization header field from the request.
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets the current user from the request.
        """
        return None
