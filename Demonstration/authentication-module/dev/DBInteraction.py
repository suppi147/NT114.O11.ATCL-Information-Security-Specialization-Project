from sqlalchemy import create_engine, Column, Integer, Text, CHAR, VARCHAR, text, exists
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import OperationalError
import os

Base = declarative_base()

class AuthTable(Base):
    __tablename__ = 'users'
    mysql_password = os.environ.get('MYSQL_PASSWORD')
    mysql_user = os.environ.get('MYSQL_USER')
    mysql_database = os.environ.get('MYSQL_DATABASE')
    db_url = f"mysql://{mysql_user}:{mysql_password}@authen-service-db-service:3306/{mysql_database}"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(CHAR(36), nullable=False, server_default=text("NULL"))
    username = Column(CHAR(80), nullable=False, server_default=text("NULL"))
    password = Column(CHAR(80), nullable=False, server_default=text("NULL"))
    fingerprint = Column(CHAR(40), nullable=False, server_default=text("NULL"))
    totpkey = Column(CHAR(100), nullable=False, server_default=text("NULL"))
    services = Column(Text, nullable=False, server_default=text("NULL"))

class AuthManager:        
    retries = 0
    max_retries = 1000
    def connect(self):
        engine = create_engine(AuthTable.db_url)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    def insert_user(self, uuid, username, password, totpkey, serviceSum):
        while AuthManager.retries < AuthManager.max_retries:
            try:
                session = self.connect()    
                new_user = AuthTable(uuid=uuid, username=username, password=password,fingerprint="NULL", totpkey=totpkey, services=serviceSum)
                session.add(new_user)
                session.commit()
                print(f"username '{new_user.username}' with UUID '{new_user.uuid}' with totpkey '{new_user.totpkey}' and service '{new_user.services}' is inserted into the db")
                session.close()
                break
            except OperationalError as e:
                    print(e)
                    AuthManager.retries += 1
    def username_exists(self, username):
        while AuthManager.retries < AuthManager.max_retries:
            try:
                try:
                    session = self.connect()
                    user = session.query(AuthTable).filter(AuthTable.username == username).one()
                    session.close()
                    return True
                except NoResultFound:
                    session.close()
                    return False
            except OperationalError as e:
                    print(e)
                    AuthManager.retries += 1
    def check_login(self, username, password):
        while AuthManager.retries < AuthManager.max_retries:
            try:
                session = self.connect()
                try:
                    user = session.query(AuthTable).filter(AuthTable.username == username, AuthTable.password == password).one()
                    session.close()
                    return True
                except NoResultFound:
                    session.close()
                    return False
            except OperationalError as e:
                print(e)
                AuthManager.retries += 1
    def get_totpkey_by_username(self, username):
        while AuthManager.retries < AuthManager.max_retries:
            try:
                session = self.connect()
                try:
                    user = session.query(AuthTable).filter(AuthTable.username == username).one()
                    totpkey = user.totpkey
                    session.close()
                    return totpkey
                except NoResultFound:
                    session.close()
                    return None
            except OperationalError as e:
                print(e)
                AuthManager.retries += 1
    def update_fingerprint_by_username(self, username, new_fingerprint):
        while AuthManager.retries < AuthManager.max_retries:
            try:
                session = self.connect()
                user = session.query(AuthTable).filter(AuthTable.username == username).one()
                user.fingerprint = new_fingerprint
                session.commit()
                print(f"Fingerprint for username '{user.username}' is updated in the db")
                session.close()
                break
            except OperationalError as e:
                print(e)
                AuthManager.retries += 1         
"""
    def update_token(self, uuid, new_token):
        while AuthManager.retries < AuthManager.max_retries:
            try:
                session = self.connect()    
                token_entry = session.query(AuthTable).filter_by(uuid=uuid).first()
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
                    AuthManager.retries += 1
    
    def get_token_by_uuid(self, uuid):
        while AuthManager.retries < AuthManager.max_retries:
            try:
                session = self.connect()    
                try:
                    token_entry = session.query(AuthTable).filter_by(uuid=uuid).first()
                    token = token_entry.token if token_entry else None
                except NoResultFound:
                    token = None
                finally:
                    session.close()
                return token
            except OperationalError as e:
                    print(e)
                    AuthManager.retries += 1

    def get_uuid_by_token(self, token):
        while AuthManager.retries < AuthManager.max_retries:
            try:
                session = self.connect()    
                try:
                    uuid_entry = session.query(AuthTable).filter_by(token=token).first()
                    uuid = uuid_entry.uuid if uuid_entry else None
                except NoResultFound:
                    uuid = None
                finally:
                    session.close()
                return uuid
            except OperationalError as e:
                    print(e)
                    AuthManager.retries += 1        

    def token_exists(self, token):
        while AuthManager.retries < AuthManager.max_retries:
            try:
                session = self.connect()
                exists_query = session.query(exists().where(AuthTable.token == token)).scalar()
                session.close()
                return exists_query
            except OperationalError as e:
                    print(e)
                    AuthManager.retries += 1 


    def uuid_exists(self, uuid):
        while AuthManager.retries < AuthManager.max_retries:
            try:
                try:
                    session = self.connect()
                    result = session.query(AuthTable).filter_by(uuid=uuid).first()
                    exists = (result is not None)
                except NoResultFound:
                    exists = False
                finally:
                    session.close()
                return exists
            except OperationalError as e:
                    print(e)
                    AuthManager.retries += 1 
"""