#!/usr/bin/env python3
"""
SessionExpAuth module for the API
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class"""

    def __init__(self):
        """Initialize SessionExpAuth"""
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except ValueError:
            self.session
