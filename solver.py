from database import signup_user, login_user

print(signup_user("test@example.com", "password123"))  # Should return True or False
print(login_user("test@example.com", "password123"))   # Should return True or False
