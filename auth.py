import bcrypt
import csv

ALLOWED_DOMAINS = ["student.ie.edu", "oficinauniversal.com"]

# Load users from CSV file
def load_users(filename='users.csv'):
    users = {}
    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            users[row['username']] = row['password_hash']
    return users

# Hash a password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()

# Check a password against a stored hash
def check_password(provided_password, stored_password_hash):
    return bcrypt.checkpw(provided_password.encode(), stored_password_hash.encode())

# Validate email domain
def is_valid_email_domain(email):
    domain = email.split('@')[-1]
    return domain in ALLOWED_DOMAINS

# Register a new user
def register_user(username, password, filename='users.csv'):
    if not is_valid_email_domain(username):
        return False, "Invalid email domain"
    
    users = load_users(filename)
    if username in users:
        return False, "User already exists"

    hashed_password = hash_password(password)
    with open(filename, mode='a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([username, hashed_password])
    return True, "User registered successfully"

# Authenticate user
def authenticate_user(username, password, filename='users.csv'):
    if not is_valid_email_domain(username):
        return False, "Invalid email domain"
    
    users = load_users(filename)
    if username in users:
        stored_password_hash = users[username]
        if check_password(password, stored_password_hash):
            return True, "Authentication successful"
    return False, "Invalid username or password"
