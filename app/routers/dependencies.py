from sql.database import SessionMaker

# Dependency
def get_db():
    db = SessionMaker()
    try:
        yield db
    finally:
        db.close()