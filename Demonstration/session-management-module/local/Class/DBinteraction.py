from sqlalchemy import create_engine, Column, Integer, Text, CHAR, BINARY, text, exists
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import OperationalError


Base = declarative_base()

class TokenTable(Base):
    __tablename__ = 'TokenTable'
    db_url = "mysql://root:123@localhost:3306/SessionManagementDB"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(CHAR(36), nullable=False, server_default=text("(UUID())"))
    token = Column(Text)
    counter = Column(BINARY(32),nullable=True)

class TokenManager:        
    retries = 0
    max_retries = 1000
    def connect(self):
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
                except NoResultFound:
                    token = None
                finally:
                    session.close()
                return token
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
                except NoResultFound:
                    exists = False
                finally:
                    session.close()
                return exists
            except OperationalError as e:
                    print(e)
                    TokenManager.retries += 1 
        

    def insert_counter(self, uuid, counter):
        while TokenManager.retries < TokenManager.max_retries:
            try:
                session = self.connect()
                token_entry = session.query(TokenTable).filter_by(uuid=uuid).first()
                if token_entry:
                    token_entry.counter = counter
                    session.commit()
                    print(f"Counter '{counter}' for Token with UUID '{uuid}' is inserted into the db")
                else:
                    print(f"Token with the UUID '{uuid}' not found. Insert failed.")
                session.close()
                break
            except OperationalError as e:
                print(e)
                TokenManager.retries += 1

    def update_counter_by_uuid(self, uuid, new_counter):
        while TokenManager.retries < TokenManager.max_retries:
            try:
                session = self.connect()
                token_entry = session.query(TokenTable).filter_by(uuid=uuid).first()
                if token_entry:
                    token_entry.counter = new_counter
                    session.commit()
                    print(f"Counter '{new_counter}' for Token with UUID '{uuid}' is updated into the db")
                else:
                    print(f"Token with the UUID '{uuid}' not found. Update failed.")
                session.close()
                break
            except OperationalError as e:
                print(e)
                TokenManager.retries += 1
    def get_counter_by_uuid(self, uuid):
        while TokenManager.retries < TokenManager.max_retries:
            try:
                session = self.connect()
                token_entry = session.query(TokenTable).filter_by(uuid=uuid).first()
                counter = token_entry.counter if token_entry else None
                session.close()
                return counter
            except OperationalError as e:
                print(e)
                TokenManager.retries += 1