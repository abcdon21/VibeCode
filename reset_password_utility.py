#!/usr/bin/env python3
"""
Password Reset Utility for FoodSaver App
Use this script to reset user passwords directly in the database
"""

import sqlite3
import hashlib
import getpass

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def reset_user_password():
    """Reset a user's password"""
    try:
        # Connect to database
        conn = sqlite3.connect('foodsaver.db')
        conn.row_factory = sqlite3.Row
        
        # Show all users
        users = conn.execute('SELECT id, first_name, last_name, email FROM users').fetchall()
        
        if not users:
            print("❌ No users found in database!")
            return
        
        print("\n📋 Current users in database:")
        print("-" * 50)
        for user in users:
            print(f"ID: {user['id']}, Name: {user['first_name']} {user['last_name']}, Email: {user['email']}")
        
        print("-" * 50)
        
        # Get user email
        email = input("\n✉️  Enter the email of the user to reset password: ").strip()
        
        # Check if user exists
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        if not user:
            print(f"❌ No user found with email: {email}")
            return
        
        print(f"\n👤 User found: {user['first_name']} {user['last_name']} ({user['email']})")
        
        # Get new password
        print("\n🔒 Enter new password:")
        password = getpass.getpass("New password (6+ characters): ")
        
        if len(password) < 6:
            print("❌ Password must be at least 6 characters long!")
            return
        
        confirm_password = getpass.getpass("Confirm password: ")
        
        if password != confirm_password:
            print("❌ Passwords don't match!")
            return
        
        # Update password
        hashed_password = hash_password(password)
        conn.execute(
            'UPDATE users SET password_hash = ? WHERE email = ?',
            (hashed_password, email)
        )
        conn.commit()
        conn.close()
        
        print(f"\n✅ Password successfully reset for {user['first_name']} {user['last_name']}!")
        print(f"📧 Email: {email}")
        print(f"🔑 New password: {password}")
        print("\nYou can now log in with the new password!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def create_new_user():
    """Create a new user account"""
    try:
        conn = sqlite3.connect('foodsaver.db')
        
        print("\n👥 Create New User Account")
        print("-" * 30)
        
        first_name = input("First name: ").strip()
        last_name = input("Last name: ").strip()
        email = input("Email: ").strip()
        
        if not all([first_name, last_name, email]):
            print("❌ All fields are required!")
            return
        
        # Check if user already exists
        existing = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        if existing:
            print(f"❌ User with email {email} already exists!")
            return
        
        # Get password
        password = getpass.getpass("Password (6+ characters): ")
        if len(password) < 6:
            print("❌ Password must be at least 6 characters long!")
            return
        
        confirm_password = getpass.getpass("Confirm password: ")
        if password != confirm_password:
            print("❌ Passwords don't match!")
            return
        
        # Create user
        hashed_password = hash_password(password)
        conn.execute(
            'INSERT INTO users (first_name, last_name, email, password_hash) VALUES (?, ?, ?, ?)',
            (first_name, last_name, email, hashed_password)
        )
        conn.commit()
        conn.close()
        
        print(f"\n✅ User account created successfully!")
        print(f"👤 Name: {first_name} {last_name}")
        print(f"📧 Email: {email}")
        print(f"🔑 Password: {password}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main menu"""
    print("🍎 FoodSaver Password Reset Utility")
    print("=" * 40)
    
    while True:
        print("\nChoose an option:")
        print("1. Reset existing user password")
        print("2. Create new user account")
        print("3. List all users")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            reset_user_password()
        elif choice == '2':
            create_new_user()
        elif choice == '3':
            try:
                conn = sqlite3.connect('foodsaver.db')
                users = conn.execute('SELECT id, first_name, last_name, email FROM users').fetchall()
                
                if not users:
                    print("\n❌ No users found in database!")
                else:
                    print(f"\n📋 Found {len(users)} user(s):")
                    print("-" * 50)
                    for user in users:
                        print(f"ID: {user[0]}, Name: {user[1]} {user[2]}, Email: {user[3]}")
                
                conn.close()
            except Exception as e:
                print(f"❌ Error: {e}")
                
        elif choice == '4':
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please enter 1-4.")

if __name__ == '__main__':
    main()
