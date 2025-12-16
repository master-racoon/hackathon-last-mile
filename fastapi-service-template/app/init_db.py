"""
Database initialization script with seed data
Run this to populate initial vehicle types
"""
from models import SessionLocal, Base, engine
from models.vehicle_type import VehicleType
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db():
    """Initialize database with seed data"""
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")
    
    db = SessionLocal()
    
    try:
        # Check if vehicle types already exist
        existing_count = db.query(VehicleType).count()
        if existing_count > 0:
            logger.info(f"Vehicle types already exist ({existing_count} records). Skipping seed data.")
            return
        
        # Seed vehicle types
        vehicle_types = [
            VehicleType(
                name="20ft Container",
                code="20FT",
                description="Standard 20-foot shipping container",
                capacity_kg=28000,
                capacity_m3=33
            ),
            VehicleType(
                name="40ft Container",
                code="40FT",
                description="Standard 40-foot shipping container",
                capacity_kg=26500,
                capacity_m3=67
            ),
            VehicleType(
                name="40ft High Cube",
                code="40HC",
                description="40-foot high cube shipping container",
                capacity_kg=26400,
                capacity_m3=76
            ),
            VehicleType(
                name="Truck - Small",
                code="TRUCK_S",
                description="Small delivery truck",
                capacity_kg=3500,
                capacity_m3=15
            ),
            VehicleType(
                name="Truck - Medium",
                code="TRUCK_M",
                description="Medium delivery truck",
                capacity_kg=7500,
                capacity_m3=30
            ),
            VehicleType(
                name="Truck - Large",
                code="TRUCK_L",
                description="Large delivery truck / semi-trailer",
                capacity_kg=24000,
                capacity_m3=80
            ),
            VehicleType(
                name="Air Freight",
                code="AIR",
                description="Air cargo freight",
                capacity_kg=None,  # Varies by aircraft
                capacity_m3=None
            ),
            VehicleType(
                name="Rail Freight",
                code="RAIL",
                description="Railway freight car",
                capacity_kg=None,  # Varies
                capacity_m3=None
            ),
        ]
        
        db.add_all(vehicle_types)
        db.commit()
        logger.info(f"Successfully seeded {len(vehicle_types)} vehicle types")
        
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    logger.info("Database initialization complete")
