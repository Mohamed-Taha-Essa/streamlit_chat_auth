#db desing  & operation 
# if for learing can uisng orm pewee but now will using sqlalchemy 


from sqlalchemy import create_engine , Column , Integer , String ,ForeignKey ,DateTime ,Text
from sqlalchemy.orm import sessionmaker ,declarative_base ,relationship
from datetime import datetime 

#Db design 
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversations = relationship(
        "Conversation",
        back_populates="user",
        cascade="all, delete-orphan"
    )

class Conversation(Base):
    __tablename__="conversations"
    id = Column(Integer ,primary_key = True)
    title= Column(String , nullable =False)
    created_at = Column(DateTime ,default=datetime.utcnow)

    #relation
    messages = relationship('Message' ,back_populates = 'conversation' ,cascade = 'all, delete-orphan')
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="conversations")
    

class Message(Base):
    __tablename__ = "messeges"
    id = Column(Integer ,primary_key = True)

    content= Column(Text , nullable =False)
    created_at = Column(DateTime ,default=datetime.utcnow)
    role = Column(String , nullable=False) #ai role [seystrm,human]

    #relations 
    conversation_id = Column(Integer ,ForeignKey('conversations.id'))
    conversation = relationship('Conversation' ,back_populates='messages')

#create db 
engine = create_engine('sqlite:///chat_history.db')
SessionLocal =sessionmaker(bind=engine)

#create all table 
Base.metadata.create_all(engine)

#db operation 
def get_session():
    'create new session'
    return SessionLocal()

def create_conversation(session,title ,user_id):
    "create new conversation"
    conv = Conversation(title=title ,user_id=user_id)
    session.add(conv)
    session.commit()
    return conv

def add_messege(session ,conversation_id ,role ,content):
    "add new message to existing conversation"
    msg = Message(conversation_id=conversation_id , role=role ,content =content)
    session.add(msg)
    session.commit()
    return msg 

def get_conversations(session ,user_id):
    "get all conversation" 
    return session.query(Conversation).filter_by(user_id=user_id).order_by(Conversation.created_at.desc()).all()

def get_messeges(session ,conversation_id):
    "return all messgs for selected convs" 
    return session.query(Message).filter_by(conversation_id=conversation_id).order_by(Message.created_at).all()

























