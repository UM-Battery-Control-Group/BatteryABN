from batteryabn.models import db


class BaseRepository:

    def __init__(self):
        self.session = db.session

    def add(self, instance):
        """Add a new instance to the session."""
        self.session.add(instance)

    def delete(self, instance):
        """Delete an instance from the session."""
        self.session.delete(instance)

    def commit(self):
        """Commit the current transaction."""
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

    def rollback(self):
        """Rollback the current transaction."""
        self.session.rollback()