from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password:str):
    #hash the password - password
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    print(plain_password, hashed_password,"inside verify")
    return pwd_context.verify(plain_password,hashed_password)