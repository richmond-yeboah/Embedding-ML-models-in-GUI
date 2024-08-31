import bcrypt

password = "statistics299"
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
print(hashed_password)