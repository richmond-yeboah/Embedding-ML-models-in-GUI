import bcrypt

password = "statistics"
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
print(hashed_password)
