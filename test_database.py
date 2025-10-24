import unittest
import sqlite3

class DatabaseConnectionTests(unittest.TestCase):
    def test_database_exists(self):
        try:
            conn = sqlite3.connect("projects.db")
            self.assertIsNotNone(conn)
            print("Database connected successfully")
        except Exception as e:
            self.fail(f"Database connection failed: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    unittest.main()
