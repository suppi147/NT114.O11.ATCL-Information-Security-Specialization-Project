from sqlalchemy import create_engine, Column, Integer, Text, CHAR, VARCHAR, text, exists
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import OperationalError


Base = declarative_base()

class AuthTable(Base):
    __tablename__ = 'AuthTable'
    db_url = "mysql://root:123@localhost:3306/SessionManagementDB"

    uuid = Column(CHAR(36), nullable=False, server_default=text("(UUID())"))
    browserFingerprint = Column(VARCHAR(64),nullable=True)

class AuthManager:        
    retries = 0
    max_retries = 1000
    def update_fingerprint_by_uuid(self, uuid, new_fingerprint):
        while AuthManager.retries < AuthManager.max_retries:
            try:
                session = self.connect()
                token_entry = session.query(AuthManager).filter_by(uuid=uuid).first()
                if token_entry:
                    token_entry.browserFingerprint = new_fingerprint
                    session.commit()
                    print(f"fingerprint '{new_fingerprint}' for Token with UUID '{uuid}' is updated into the db")
                else:
                    print(f"Token with the UUID '{uuid}' not found. Update failed.")
                session.close()
                break
            except OperationalError as e:
                print(e)
                AuthManager.retries += 1


    def get_fingerprint_by_uuid(self, uuid):
        while AuthManager.retries < AuthManager.max_retries:
            try:
                session = self.connect()
                token_entry = session.query(AuthTable).filter_by(uuid=uuid).first()
                fingerprint = token_entry.browserFingerprint if token_entry else None
                session.close()
                return fingerprint
            except OperationalError as e:
                print(e)
                AuthManager.retries += 1