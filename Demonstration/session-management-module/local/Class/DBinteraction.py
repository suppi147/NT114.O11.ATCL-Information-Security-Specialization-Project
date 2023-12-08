from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class TokenTable(Base):
    __tablename__ = 'TokenTable'
    db_url = "mysql://root:123@localhost:3306/SessionManagementDB"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(Text)

class TokenManager:
    def __init__(self):
        self.engine = create_engine(TokenTable.db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def connect(self):
        return self.Session()

    def insert_token(self, token):
        session = self.connect()
        new_token = TokenTable(token=token)
        session.add(new_token)
        session.commit()
        session.close()

    def update_token(self, old_token, new_token):
        session = self.connect()
        token_entry = session.query(TokenTable).filter_by(token=old_token).first()
        if token_entry:
            token_entry.token = new_token
            session.commit()
        session.close()

# Example usage:
if __name__ == "__main__":
    token_manager = TokenManager()
    token_manager.insert_token("new_token")
    token_manager.update_token("new_token", "newbwww_token")
