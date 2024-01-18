from sqlalchemy import create_engine, Column, Integer, Text, CHAR, text, exists
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import OperationalError
import os

Base = declarative_base()

class TokenTable(Base):
    __tablename__ = 'TokenTable'
    mysql_password = os.environ.get('MYSQL_PASSWORD')
    mysql_user = os.environ.get('MYSQL_USER')
    mysql_database = os.environ.get('MYSQL_DATABASE')
    db_url = f"mysql://{mysql_user}:{mysql_password}@authorization-db-service:3306/{mysql_database}"


    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(CHAR(36), nullable=False)
    token = Column(Text)

class TokenManager:        
    retries = 0
    max_retries = 1000
    def connect(self, max_retries=1000):
        engine = create_engine(TokenTable.db_url)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    def insert_token(self, token, uuid):
        while TokenManager.retries < TokenManager.max_retries:
            try:
                session = self.connect()    
                new_token = TokenTable(token=token, uuid=uuid)
                session.add(new_token)
                session.commit()
                print(f"Token '{new_token.token}' with UUID '{new_token.uuid}' is inserted into the db")
                session.close()
                break
            except OperationalError as e:
                    print(e)
                    TokenManager.retries += 1

    def update_token(self, uuid, new_token):
        while TokenManager.retries < TokenManager.max_retries:
            try:
                session = self.connect()    
                token_entry = session.query(TokenTable).filter_by(uuid=uuid).first()
                if token_entry:
                    token_entry.token = new_token
                    session.commit()
                    print(f"Token '{token_entry.token}' with UUID '{token_entry.uuid}' is updated into the db")
                else:
                    print(f"Token with the UUID '{uuid}' not found. Update failed.")
                session.close()
                break
            except OperationalError as e:
                    print(e)
                    TokenManager.retries += 1
    
    def get_token_by_uuid(self, uuid):
        while TokenManager.retries < TokenManager.max_retries:
            try:
                session = self.connect()    
                try:
                    token_entry = session.query(TokenTable).filter_by(uuid=uuid).first()
                    token = token_entry.token if token_entry else None
                    session.close()
                except NoResultFound:
                    token = None
                return token
            except OperationalError as e:
                    print(e)
                    TokenManager.retries += 1        
    def get_uuid_by_token(self, token):
        while TokenManager.retries < TokenManager.max_retries:
            try:
                session = self.connect()    
                try:
                    uuid_entry = session.query(TokenTable).filter_by(token=token).first()
                    uuid = uuid_entry.uuid if uuid_entry else None
                except NoResultFound:
                    uuid = None
                finally:
                    session.close()
                return uuid
            except OperationalError as e:
                    print(e)
                    TokenManager.retries += 1    
    def token_exists(self, token):
        while TokenManager.retries < TokenManager.max_retries:
            try:
                session = self.connect()
                exists_query = session.query(exists().where(TokenTable.token == token)).scalar()
                session.close()
                return exists_query
            except OperationalError as e:
                    print(e)
                    TokenManager.retries += 1 


    def uuid_exists(self, uuid):
        while TokenManager.retries < TokenManager.max_retries:
            try:
                try:
                    session = self.connect()
                    result = session.query(TokenTable).filter_by(uuid=uuid).first()
                    exists = (result is not None)
                    session.close()
                except NoResultFound:
                    exists = False
                return exists
            except OperationalError as e:
                    print(e)
                    TokenManager.retries += 1 