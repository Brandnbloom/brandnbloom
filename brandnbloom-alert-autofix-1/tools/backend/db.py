from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import os
from datetime import datetime

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///data/bloominsight.db')
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, index=True)
    handle = Column(String, unique=True, index=True, nullable=False)
    display_name = Column(String)
    bio = Column(Text)
    followers = Column(Integer)
    following = Column(Integer)
    profile_pic_url = Column(String)
    last_pull = Column(DateTime, default=datetime.utcnow)

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), index=True)
    post_id = Column(String, index=True)
    timestamp = Column(DateTime)
    caption = Column(Text)
    like_count = Column(Integer)
    comment_count = Column(Integer)
    impressions = Column(Integer)
    reach = Column(Integer)
    hashtags = Column(Text)
    media_type = Column(String)
    raw = Column(Text)
    account = relationship('Account')

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    create_tables()
    print('Tables created.')
