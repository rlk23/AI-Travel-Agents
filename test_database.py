from database.config import SessionLocal, engine
from database.models import Base, User
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
import uuid

def create_tables():
    """Create all database tables"""
    print("\n=== Creating Database Tables ===")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
    except Exception as e:
        print("❌ Failed to create tables!")
        print(f"Error: {str(e)}")
        return False
    return True

def test_database_connection():
    """Test database connection"""
    print("\n=== Testing Database Connection ===")
    try:
        with SessionLocal() as session:
            result = session.execute(text("SELECT 1")).scalar()
            if result == 1:
                print("✅ Database connection successful!")
                return True
            else:
                print("❌ Database connection failed!")
                return False
    except Exception as e:
        print(f"❌ Database connection failed!")
        print(f"Error: {str(e)}")
        return False

def test_create_user():
    """Test creating a user in the database"""
    print("\n=== Testing User Creation ===")
    try:
        db = SessionLocal()
        # Create a test user
        test_user = User(
            user_id=uuid.uuid4(),
            email="test@example.com",
            password_hash="test_password_hash",
            first_name="Test",
            last_name="User"
        )
        db.add(test_user)
        db.commit()
        print("✅ User creation successful!")
        return test_user.user_id
    except SQLAlchemyError as e:
        db.rollback()
        print("❌ User creation failed!")
        print("Error:", str(e))
        return None
    finally:
        db.close()

def test_read_user(user_id):
    """Test reading a user from the database"""
    print("\n=== Testing User Read ===")
    try:
        db = SessionLocal()
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            print("✅ User read successful!")
            print(f"Found user: {user.first_name} {user.last_name} ({user.email})")
            return True
        else:
            print("❌ User not found!")
            return False
    except SQLAlchemyError as e:
        print("❌ User read failed!")
        print("Error:", str(e))
        return False
    finally:
        db.close()

def test_delete_user(user_id):
    """Test deleting a user from the database"""
    print("\n=== Testing User Deletion ===")
    try:
        db = SessionLocal()
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            print("✅ User deletion successful!")
            return True
        else:
            print("❌ User not found for deletion!")
            return False
    except SQLAlchemyError as e:
        db.rollback()
        print("❌ User deletion failed!")
        print("Error:", str(e))
        return False
    finally:
        db.close()

def main():
    """Run all database tests"""
    print("Starting Database Tests...")
    
    # Create tables
    if not create_tables():
        return
    
    # Test database connection
    if not test_database_connection():
        return
    
    # Test user operations
    user_id = test_create_user()
    if user_id:
        test_read_user(user_id)
        test_delete_user(user_id)

if __name__ == "__main__":
    main() 