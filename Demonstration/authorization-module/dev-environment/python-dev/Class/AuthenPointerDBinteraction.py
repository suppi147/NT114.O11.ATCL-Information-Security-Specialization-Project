from sqlalchemy import create_engine, Column, Integer, Text, CHAR, text, exists
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import OperationalError
import os

Base = declarative_base()

class AuthPointerTable(Base):
    __tablename__ = 'users'
    mysql_password = os.environ.get('MYSQL_PASSWORD')
    mysql_user = os.environ.get('AUTHEN_MYSQL_USER')
    mysql_database = os.environ.get('AUTHEN_MYSQL_DATABASE')
    db_url = f"mysql://{mysql_user}:{mysql_password}@authen-service-db-service:3306/{mysql_database}"


    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(CHAR(80), nullable=False, server_default=text("NULL"))
    uuid = Column(CHAR(36), nullable=False, server_default=text("NULL"))
    fingerprint = Column(CHAR(40), nullable=False, server_default=text("NULL"))
    services = Column(Text, nullable=False, server_default=text("NULL"))

class AuthPointerManager:        
    retries = 0
    max_retries = 1000
    def connect(self, max_retries=1000):
        engine = create_engine(AuthPointerTable.db_url)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    def get_fingerprint_by_uuid(self, uuid):
        while AuthPointerManager.retries < AuthPointerManager.max_retries:
            try:
                session = self.connect()
                try:
                    user = session.query(AuthPointerTable).filter(AuthPointerTable.uuid == uuid).first()
                    fingerprint = user.fingerprint if user else None
                    session.close()
                    return fingerprint
                except NoResultFound:
                    session.close()
                    return None
            except OperationalError as e:
                print(e)
                AuthPointerManager.retries += 1

    def get_services_by_uuid(self, uuid):
        while AuthPointerManager.retries < AuthPointerManager.max_retries:
            try:
                session = self.connect()
                try:
                    user = session.query(AuthPointerTable).filter(AuthPointerTable.uuid == uuid).first()
                    services = user.services if user else None
                    session.close()
                    return services
                except NoResultFound:
                    session.close()
                    return None
            except OperationalError as e:
                print(e)
                AuthPointerManager.retries += 1

    def get_uuid_by_username(self, username):
        while AuthPointerManager.retries < AuthPointerManager.max_retries:
            try:
                session = self.connect()
                try:
                    user = session.query(AuthPointerTable).filter(AuthPointerTable.username == username).first()
                    uuid = user.uuid if user else None
                    session.close()
                    return uuid
                except NoResultFound:
                    session.close()
                    return None
            except OperationalError as e:
                print(e)
                AuthPointerManager.retries += 1

    def get_username_by_uuid(self, uuid):
        while AuthPointerManager.retries < AuthPointerManager.max_retries:
            try:
                session = self.connect()
                try:
                    user = session.query(AuthPointerTable).filter(AuthPointerTable.uuid == uuid).first()
                    username = user.username if user else None
                    session.close()
                    return username
                except NoResultFound:
                    session.close()
                    return None
            except OperationalError as e:
                print(e)
                AuthPointerManager.retries += 1