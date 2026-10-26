from sqlalchemy import Column, Integer, String, Boolean
from src.utils.db import Base


class UserModel(Base):
    __tablename__ = "user_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)





#the difference in argon2 and bcrypt is that argon2 is more secure and resistant to attacks. Argon2 is the winner of the Password Hashing Competition (PHC) and is designed to be memory-hard, which means it requires a significant amount of memory to compute the hash, making it more resistant to brute-force attacks. Bcrypt, on the other hand, is an older hashing algorithm that is still widely used but is not as secure as Argon2.


