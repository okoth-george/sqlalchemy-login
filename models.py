from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session

# Setup
Base = declarative_base()

# Define a model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

# Connect to the database
engine = create_engine("sqlite:///users.db")
Base.metadata.create_all(engine)



with Session(engine) as session:
    user=session.query(User).filter(User.name=="jijo").first()
    print(user.id,user.email)






