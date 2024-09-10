#!/usr/bin/env python3
"""End-to-end integration test"""
import requests

BASE_URL = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """Test user registration"""
    response = requests.post(
        f"{BASE_URL}/users",
        data={'email': email, 'password': password}
    )
    assert response.status_code == 200, (
        f"Failed to register user. Status code: {response.status_code}"
    )
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test login with wrong password"""
    response = requests.post(
        f"{BASE_URL}/sessions",
        data={'email': email, 'password': password}
    )
    assert response.status_code == 401, (
        "Login with wrong password should fail. "
        f"Status: {response.status_code}"
    )


def log_in(email: str, password: str) -> str:
    """Test user login"""
    response = requests.post(
        f"{BASE_URL}/sessions",
        data={'email': email, 'password': password}
    )
    assert response.status_code == 200, (
        f"Failed to log in. Status code: {response.status_code}"
    )
    assert "session_id" in response.cookies, "Session ID not found in cookies"
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """Test profile access without logging in"""
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403, (
        "Unlogged profile access should be forbidden. "
        f"Status: {response.status_code}"
    )


def profile_logged(session_id: str) -> None:
    """Test profile access when logged in"""
    response = requests.get(
        f"{BASE_URL}/profile",
        cookies={"session_id": session_id}
    )
    assert response.status_code == 200, (
        f"Failed to access profile. Status code: {response.status_code}"
    )
    assert "email" in response.json(), "Email not found in profile response"


def log_out(session_id: str) -> None:
    """Test user logout"""
    response = requests.delete(
        f"{BASE_URL}/sessions",
        cookies={"session_id": session_id}
    )
    assert response.status_code == 200, (
        f"Failed to log out. Status code: {response.status_code}"
    )


def reset_password_token(email: str) -> str:
    """Test password reset token generation"""
    response = requests.post(
        f"{BASE_URL}/reset_password",
        data={'email': email}
    )
    assert response.status_code == 200, (
        f"Failed to get reset token. Status code: {response.status_code}"
    )
    assert "reset_token" in response.json(), (
        "Reset token not found in response"
    )
    return response.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test password update"""
    response = requests.put(
        f"{BASE_URL}/reset_password",
        data={
            'email': email,
            'reset_token': reset_token,
            'new_password': new_password
        }
    )
    assert response.status_code == 200, (
        f"Failed to update password. Status code: {response.status_code}"
    )
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
