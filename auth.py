#authentication desing & operation login ,register ,logout

#import library to hash password
from passlib.context import CryptContext
from db import User 

#initialize password context
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password):
    """hash a password"""
    return pwd_context.hash(password)


def verify_password(password, hashed_password):
    """check if password is correct"""
    return pwd_context.verify(password, hashed_password)


def register_user(session ,email, password):
    """register a new user"""
    new_user = User(email=email, password_hash=hash_password(password))
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


def authenticate_user(session ,email ,password):
    user = session.query(User).filter_by(email=email).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


