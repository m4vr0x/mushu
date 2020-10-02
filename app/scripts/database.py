import logging
import pymongo

def test_db_connection():
    db_client = pymongo.MongoClient("db", 27017, serverSelectionTimeoutMS=5000)

    logging.info("Testing database connection...")
    try:
        db_client.server_info()
        msg = "Succefully connected to MongoDB"
        logging.info(msg)
        return msg
    except pymongo.errors.ServerSelectionTimeoutError as e:
        msg = (f'Connection try timed out: {e}')
        logging.critical(msg)
        return msg
    except Exception:
        raise
