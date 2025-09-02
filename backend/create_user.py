from app.core.hashing import get_password_hash
import sys

# Add the app directory to the path to allow imports
sys.path.append('.')

def main():
    """A simple script to generate a hashed password for manual user creation."""
    print("--- Create a new user for the database ---")
    email = input("Enter user's email: ")
    password = input("Enter user's password: ")

    if not email or not password:
        print("Email and password cannot be empty.")
        return

    hashed_password = get_password_hash(password)

    print("\n✅ User created successfully!")
    print("Copy the following details into your MongoDB 'users' collection:\n")
    print(f"  email: '{email}'")
    print(f"  hashed_password: '{hashed_password}'")
    print("  history: []")

if __name__ == "__main__":
    main()
