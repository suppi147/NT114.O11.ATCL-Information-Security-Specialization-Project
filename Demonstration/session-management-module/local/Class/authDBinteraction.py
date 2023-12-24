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
    def connect(self):
        engine = create_engine(AuthTable.db_url)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

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