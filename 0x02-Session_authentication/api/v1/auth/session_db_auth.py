#!/usr/bin/env python3
"""SessionDBAuth module for the API"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from models.user import User
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class for handling session authentication with database"""

    def __init__(self):
        """Initialize SessionDBAuth instance"""
        super().__init__()
        User.load_from_file()
        UserSession.load_from_file()

    def create_session(self, user_id=None):
        """
        Create and store a new UserSession and return the Session ID
        Args:
            user_id (str): The user ID
        Returns:
            str: The session ID or None if creation fails
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        kwargs = {
            'user_id': user_id,
            'session_id': session_id,
        }
        user_session = UserSession(**kwargs)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the User ID by requesting UserSession in the database
        Args:
            session_id (str): The session ID
        Returns:
            str: The user ID or None if not found or expired
        """
        if session_id is None:
            return None
        try:
            user_sessions = UserSession.search({'session_id': session_id})
            if not user_sessions:
                return None
            user_session = user_sessions[0]
            expired_time = user_session.created_at + \
                timedelta(seconds=self.session_duration)
            if expired_time < datetime.utcnow():
                return None
            return user_session.user_id
        except Exception as e:
            print(f"Error in user_id_for_session_id: {e}")
            return None

    def destroy_session(self, request=None):
        """
        Destroys the UserSession based on the Session ID
        from the request cookie
        Args:
            request: The Flask request object
        Returns:
            bool: True if the session was destroyed, False otherwise
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        try:
            user_sessions = UserSession.search({'session_id': session_id})
            if not user_sessions:
                return False
            user_session = user_sessions[0]
            user_session.remove()
            return True
        except Exception as e:
            print(f"Error in destroy_session: {e}")
            return False
