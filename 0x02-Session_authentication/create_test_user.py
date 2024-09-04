#!/usr/bin/env python3
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from models.user import User

def create_test_user():
    try:
        test_user = User()
        test_user.email = "bob@hbtn.io"
        test_user.password = "H0lbertonSchool98!"
        test_user.first_name = "Bob"
        test_user.last_name = "Dylan"
        test_user.save()
        print("Test user created successfully")
        
        # Print all users
        all_users = User.all()
        print(f"Total users: {len(all_users)}")
        for user in all_users:
            print(f"User: {user.id}, Email: {user.email}")
    except Exception as e:
        print(f"Error creating test user: {e}")

if __name__ == "__main__":
    create_test_user()
