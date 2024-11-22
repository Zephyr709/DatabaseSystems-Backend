from sqlalchemy import create_engine, Column, Integer, String, Text, Numeric, BigInteger, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

# Subscription Model
class Subscription(Base):
    __tablename__ = 'subscription'

    subscriptionid = Column(BigInteger, primary_key=True, autoincrement=True)
    subscriptiontype = Column(Text, nullable=False)
    billingcycle = Column(Text, nullable=False)
    startdate = Column(DateTime(timezone=True), nullable=False)
    renewaldate = Column(DateTime(timezone=True), nullable=False)
    paymentstatus = Column(Text, nullable=False)

    # Relationship with Professional and User
    professionals = relationship("Professional", back_populates="subscription")
    users = relationship("User", back_populates="subscription")

    def __repr__(self):
        return f"<Subscription(subscriptionid={self.subscriptionid}, subscriptiontype={self.subscriptiontype})>"

# Professional Model
class Professional(Base):
    __tablename__ = 'professional'

    professionalid = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    maxseats = Column(Integer, nullable=False)
    currentseats = Column(Integer, nullable=False, default=0)
    subscriptionid = Column(BigInteger, ForeignKey('subscription.subscriptionid'))

    # Relationship with Subscription and User
    subscription = relationship("Subscription", back_populates="professionals")
    users = relationship("User", back_populates="professional")

    def __repr__(self):
        return f"<Professional(professionalid={self.professionalid}, name={self.name})>"

# User Model
class User(Base):
    __tablename__ = 'users'

    userid = Column(BigInteger, primary_key=True, autoincrement=True)
    country = Column(Text, nullable=False)
    city = Column(Text, nullable=False)
    height = Column(Numeric(5, 2), nullable=False)
    gender = Column(Text, nullable=False)
    weight = Column(Numeric(5, 2), nullable=False)
    birthdate = Column(DateTime(timezone=True), nullable=False)
    email = Column(Text, unique=True, nullable=False)
    name = Column(Text, nullable=False)
    nutritiongoal = Column(Text, nullable=False)
    macrosplit = Column(Text, nullable=False)
    totallogins = Column(Integer, default=0, nullable=False)
    lastlogin = Column(DateTime(timezone=True))
    createdat = Column(DateTime, default=datetime.utcnow, nullable=False)
    subscriptionid = Column(BigInteger, ForeignKey('subscription.subscriptionid'), nullable=True)
    professionalid = Column(BigInteger, ForeignKey('professional.professionalid'), nullable=True)

    # Relationships
    subscription = relationship("Subscription", back_populates="users")
    professional = relationship("Professional", back_populates="users")

    def __repr__(self):
        return f"<User(userid={self.userid}, name={self.name})>"