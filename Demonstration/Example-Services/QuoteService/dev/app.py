from flask import Flask, jsonify
from sqlalchemy import create_engine, Column, Integer, Text, func
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
import os


app = Flask(__name__)

Base = declarative_base()

class QuoteTable(Base):
    __tablename__ = 'QuoteTable'
    mysql_password = os.environ.get('MYSQL_PASSWORD')
    mysql_user = os.environ.get('MYSQL_USER')
    mysql_database = os.environ.get('MYSQL_DATABASE')
    db_url = f"mysql://{mysql_user}:{mysql_password}@quote-service-db-service:3306/{mysql_database}"
    id = Column(Integer, primary_key=True, autoincrement=True)
    quote = Column(Text, nullable=False)

class QuoteManager:
    retries = 0
    max_retries = 1000

    def connect(self):
        engine = create_engine(QuoteTable.db_url)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    def disconnect(self, session):
        session.close()

    def get_random_quote(self):
        while QuoteManager.retries < QuoteManager.max_retries:
            try:
                session = self.connect()
                random_quote = session.query(QuoteTable).order_by(func.rand()).first()
                self.disconnect(session)
                return random_quote
            except OperationalError as e:
                print(f"Error connecting to the database: {e}")
                QuoteManager.retries += 1

db_manager = QuoteManager()

@app.route('/random_quote', methods=['GET'])
def get_random_quote():
    random_quote = db_manager.get_random_quote()

    if random_quote:
        return jsonify({"quote": random_quote.quote})
    else:
        return jsonify({"message": "No quotes available"}), 404

if __name__ == '__main__':
    app.run(debug=True)