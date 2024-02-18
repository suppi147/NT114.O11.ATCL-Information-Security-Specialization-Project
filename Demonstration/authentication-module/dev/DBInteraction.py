from sqlalchemy import create_engine, Column, Integer, Text, CHAR, VARCHAR, text, exists
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import OperationalError
from log import Logger
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
        logger = Logger("authen_log.txt")
        while AuthManager.retries < AuthManager.max_retries:
            try:
                session = self.connect()    
                new_user = AuthTable(uuid=uuid, username=username, password=password,fingerprint="NULL", totpkey=totpkey, services=serviceSum)
                session.add(new_user)
                session.commit()
                logger.log(f"|authentication-module|DBInteraction.py|insert_user(uuid, username, password, totpkey, serviceSum)|connect to database: {AuthTable.mysql_database} success|")
                logger.log(f"|authentication-module|DBInteraction.py|insert_user(uuid, username, password, totpkey, serviceSum)|UUID: {new_user.uuid}, username: {new_user.username}, password: {new_user.password}, fingerprint: {new_user.fingerprint}, totpkey: {new_user.totpkey}, service: {new_user.services} is inserted into database: {AuthTable.mysql_database}|")
                session.close()
                break
            except OperationalError as e:
                    logger.log(f"|authentication-module|DBInteraction.py|insert_user(uuid, username, password, totpkey, serviceSum)|{e}|")
                    AuthManager.retries += 1
    def username_exists(self, username):
        logger = Logger("authen_log.txt")
        while AuthManager.retries < AuthManager.max_retries:
            try:
                try:
                    session = self.connect()
                    user = session.query(AuthTable).filter(AuthTable.username == username).one()
                    session.close()
                    logger.log(f"|authentication-module|DBInteraction.py|username_exists(username)|connect to database: {AuthTable.mysql_database} success|")
                    logger.log(f"|authentication-module|DBInteraction.py|username_exists(username)|username:{username} exist in database: {AuthTable.mysql_database}|")
                    return True
                except NoResultFound:
                    session.close()
                    logger.log(f"|authentication-module|DBInteraction.py|username_exists(username)|connect to database: {AuthTable.mysql_database} success|")
                    logger.log(f"|authentication-module|DBInteraction.py|username_exists(username)|username:{username} NOT exist in database: {AuthTable.mysql_database}|")
                    return False
            except OperationalError as e:
                    logger.log(f"|authentication-module|DBInteraction.py|username_exists(username)|{e}|")
                    AuthManager.retries += 1
    def check_login(self, username, password):
        logger = Logger("authen_log.txt")
        while AuthManager.retries < AuthManager.max_retries:
            try:
                session = self.connect()
                try:
                    user = session.query(AuthTable).filter(AuthTable.username == username, AuthTable.password == password).one()
                    session.close()
                    logger.log(f"|authentication-module|DBInteraction.py|check_login(self, username, password)|connect to database: {AuthTable.mysql_database} success|")
                    logger.log(f"|authentication-module|DBInteraction.py|check_login(self, username, password)|username:{username} and password:{password} login exist|")
                    return True
                except NoResultFound:
                    logger.log(f"|authentication-module|DBInteraction.py|check_login(self, username, password)|connect to database: {AuthTable.mysql_database} success|")
                    logger.log(f"|authentication-module|DBInteraction.py|check_login(self, username, password)|username:{username} and password:{password} NOT correct|")
                    session.close()
                    return False
            except OperationalError as e:
                logger.log(f"|authentication-module|DBInteraction.py|check_login(self, username, password)|{e}|")
                AuthManager.retries += 1
    def get_totpkey_by_username(self, username):
        logger = Logger("authen_log.txt")
        while AuthManager.retries < AuthManager.max_retries:
            try:
                session = self.connect()
                try:
                    user = session.query(AuthTable).filter(AuthTable.username == username).one()
                    totpkey = user.totpkey
                    session.close()
                    logger.log(f"|authentication-module|DBInteraction.py|get_totpkey_by_username(self, username)|connect to database: {AuthTable.mysql_database} success|")
                    logger.log(f"|authentication-module|DBInteraction.py|get_totpkey_by_username(self, username)|update totp: {user.totpkey} for username:{AuthTable.username}|")
                    return totpkey
                except NoResultFound:
                    logger.log(f"|authentication-module|DBInteraction.py|get_totpkey_by_username(self, username)|totp by username: {username} NOT found|")
                    session.close()
                    return None
            except OperationalError as e:
                logger.log(f"|authentication-module|DBInteraction.py|get_totpkey_by_username(self, username)|{e}|")
                AuthManager.retries += 1
    def update_fingerprint_by_username(self, username, new_fingerprint):
        logger = Logger("authen_log.txt")
        while AuthManager.retries < AuthManager.max_retries:
            try:
                session = self.connect()
                logger.log(f"|authentication-module|DBInteraction.py|update_fingerprint_by_username(self, username, new_fingerprint)|connect to database: {AuthTable.mysql_database} success|")
                user = session.query(AuthTable).filter(AuthTable.username == username).one()
                user.fingerprint = new_fingerprint
                session.commit()
                logger.log(f"|authentication-module|DBInteraction.py|update_fingerprint_by_username(self, username, new_fingerprint)|Fingerprint:{user.fingerprint} for username '{user.username}' is updated into database: {AuthTable.mysql_database}|")
                session.close()
                break
            except OperationalError as e:
                logger.log(f"|authentication-module|DBInteraction.py|update_fingerprint_by_username(self, username, new_fingerprint)|{e}|")
                AuthManager.retries += 1         
