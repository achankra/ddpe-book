# Simple Repository Pattern demonstrating DDPE layer separation

# WRONG: Service coupled to datastore ❌
class BadPaymentService:
    def get_payment(self, id):
        import psycopg2  # Direct datastore dependency!
        conn = psycopg2.connect("...")
        cursor = conn.execute("SELECT * FROM payments WHERE id = %s", (id,))
        return cursor.fetchone()

# RIGHT: Service uses repository abstraction ✓
class PaymentRepository:
    """Abstraction layer - can swap PostgreSQL for DynamoDB without changing service."""
    
    def find_by_id(self, payment_id: str) -> dict:
        # Datastore details hidden here
        pass

class PaymentService:
    """Business logic layer - speaks domain language, not SQL."""
    
    def __init__(self, repo: PaymentRepository):
        self._repo = repo  # Injected dependency
    
    def get_payment(self, payment_id: str) -> dict:
        return self._repo.find_by_id(payment_id)  # No datastore knowledge




    
