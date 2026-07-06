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



if __name__ == "__main__":
    print("=" * 62)
    print("  Repository Pattern — Layer Separation Demo")
    print("=" * 62)

    # --- BAD approach ---
    print("\n--- WRONG: Tightly-Coupled Service ---")
    print("  BadPaymentService.get_payment() imports psycopg2 directly.")
    print("  Problems:")
    print("    - Cannot swap PostgreSQL for DynamoDB without rewriting")
    print("    - Cannot unit-test without a live database")
    print("    - Business logic mixed with infrastructure details")

    # --- GOOD approach ---
    print("\n--- RIGHT: Repository-Abstracted Service ---")

    class InMemoryPaymentRepo(PaymentRepository):
        """Test double — swappable without touching the service."""
        def __init__(self):
            self._store = {
                "PAY-001": {"id": "PAY-001", "amount": 99.99, "status": "completed"},
                "PAY-002": {"id": "PAY-002", "amount": 250.00, "status": "pending"},
            }
        def find_by_id(self, payment_id: str) -> dict:
            return self._store.get(payment_id, {"error": "not found"})

    repo = InMemoryPaymentRepo()
    service = PaymentService(repo)

    for pid in ["PAY-001", "PAY-002", "PAY-999"]:
        result = service.get_payment(pid)
        print(f"  service.get_payment('{pid}') -> {result}")

    print("\n  Benefits:")
    print("    - Service has zero knowledge of the datastore")
    print("    - Swap InMemoryRepo -> PostgresRepo -> DynamoRepo freely")
    print("    - Unit tests run in milliseconds with in-memory doubles")
    print("=" * 62)
