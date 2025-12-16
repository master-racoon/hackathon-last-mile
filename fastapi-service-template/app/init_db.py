"""
Database initialization script with seed data
Run this to populate initial vehicle types and customer orders from Excel
"""
from models import SessionLocal, Base, engine
from models.vehicle_type import VehicleType
from models.customer_order import CustomerOrder
import pandas as pd
from datetime import datetime, date
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_vehicle_types(db):
    """Seed vehicle types based on the dataset"""
    # Check if vehicle types already exist
    existing_count = db.query(VehicleType).count()
    if existing_count > 0:
        logger.info(f"Vehicle types already exist ({existing_count} records). Skipping vehicle type seed data.")
        return
    
    # Load from predefined data in data/vehicle_types.xlsx
    excel_path = "/data/vehicle_types.xlsx"
    if not Path(excel_path).exists():
        logger.warning(f"Vehicle types Excel file not found at {excel_path}. Skipping vehicle type seed data.")
        return
    
    try:
        # Try reading from different sheets
        excel_file = pd.ExcelFile(excel_path)
        logger.info(f"Available sheets: {excel_file.sheet_names}")
        
        # Try first sheet that has data
        df = None
        for sheet_name in excel_file.sheet_names:
            test_df = pd.read_excel(excel_path, sheet_name=sheet_name)
            if len(test_df) > 0:
                df = test_df
                logger.info(f"Using sheet: {sheet_name}")
                break
        
        if df is None or len(df) == 0:
            logger.warning("No data found in any sheet")
            return
            
        logger.info(f"Loaded {len(df)} vehicle types from Excel")
        logger.info(f"Columns found: {df.columns.tolist()}")
        
        vehicle_types = []
        for _, row in df.iterrows():
            vehicle_type = VehicleType(
                name=str(row['Vehicle']) if pd.notna(row['Vehicle']) else None,
                max_weight_kg=float(row['Payload_ton']) * 1000 if pd.notna(row['Payload_ton']) else None,
                payload_ton=float(row['Payload_ton']) if pd.notna(row['Payload_ton']) else None,
                max_volume_m3=float(row['Volume_m3']) if pd.notna(row['Volume_m3']) else None,
                volume_m3=float(row['Volume_m3']) if pd.notna(row['Volume_m3']) else None,
                length_m=float(row['Length_m']) if pd.notna(row['Length_m']) else None,
                width_m=float(row['Width_m']) if pd.notna(row['Width_m']) else None,
                height_m=float(row['Height_m']) if pd.notna(row['Height_m']) else None,
                diesel=bool(row['Diesel'] == 'yes') if pd.notna(row['Diesel']) else False,
                hybrid=bool(row['Hybrid'] == 'yes') if pd.notna(row['Hybrid']) else False,
                ev_van=bool(row['EV_van'] == 'yes') if pd.notna(row['EV_van']) else False,
                ev_charge_time=None,
                ev_range_km=float(str(row['EV_range_km']).split('–')[0]) if pd.notna(row['EV_range_km']) and row['EV_range_km'] != '—' else None,
                ev_energy_kwh_per_km=float(row['EV_energy_kWh_per_km']) if pd.notna(row['EV_energy_kWh_per_km']) and row['EV_energy_kWh_per_km'] != ' ' else None,
                average_speed_kmh=None,
                fuel_consumption_per_100km=None,
                diesel_l_per_km=float(row['Diesel_l_per_km']) if pd.notna(row['Diesel_l_per_km']) else None,
                cost_per_km=None,
                diesel_cost_zar_per_km=float(row['Diesel_cost_ZAR_per_km']) if pd.notna(row['Diesel_cost_ZAR_per_km']) else None,
                ev_cost_zar_per_km_ac=float(row['EV_cost_ZAR_per_km_AC']) if pd.notna(row['EV_cost_ZAR_per_km_AC']) and row['EV_cost_ZAR_per_km_AC'] != ' ' else None,
                ev_cost_zar_per_km_dc=float(row['EV_cost_ZAR_per_km_DC']) if pd.notna(row['EV_cost_ZAR_per_km_DC']) and row['EV_cost_ZAR_per_km_DC'] != ' ' else None,
                daily_rental_cost=None,
                is_active=True,
                description=None
            )
            vehicle_types.append(vehicle_type)
        
        db.add_all(vehicle_types)
        db.commit()
        logger.info(f"Successfully seeded {len(vehicle_types)} vehicle types")
        
    except Exception as e:
        logger.error(f"Error loading vehicle types from Excel: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()



def seed_orders_from_excel(db, excel_path="/data/open_orders.xlsx"):
    """Load customer orders from Excel file - aligned with Excel structure"""
    
    if not Path(excel_path).exists():
        logger.warning(f"Excel file not found at {excel_path}. Skipping order seed data.")
        logger.info("Ensure the data directory is mounted in docker-compose.yaml: ./data:/data")
        return
    
    # Check if orders already exist
    existing_count = db.query(CustomerOrder).count()
    if existing_count > 0:
        logger.info(f"Customer orders already exist ({existing_count} records). Skipping order seed data.")
        return
    
    try:
        df = pd.read_excel(excel_path)
        logger.info(f"Loaded {len(df)} rows from Excel")
        logger.info(f"Excel columns: {df.columns.tolist()}")
        
        # Group by order number to aggregate line items
        order_groups = df.groupby('Order number')
        
        orders_created = 0
        for order_num, group in order_groups:
            first_row = group.iloc[0]
            
            # Parse delivery date (format: YYYYMMDD)
            delivery_date_str = str(first_row['requested delivery date'])
            try:
                delivery_date = datetime.strptime(delivery_date_str, '%Y%m%d').date()
            except Exception as e:
                logger.warning(f"Could not parse date {delivery_date_str} for order {order_num}: {e}, using default")
                delivery_date = date(2026, 1, 1)
            
            # Aggregate weights and width from all line items
            total_gross_weight = group['gross weight'].sum()
            total_net_weight = group['net weight'].sum()
            total_width = group['width'].sum()
            
            # Get delivery method (assuming all line items have same delivery method)
            delivery_method = int(first_row['delivery method']) if pd.notna(first_row['delivery method']) else None
            
            # Lookup vehicle type - use weight to recommend appropriate vehicle
            vehicle_type = None
            if total_gross_weight > 0:
                # Recommend vehicle based on weight
                if total_gross_weight <= 1000:
                    vehicle_type = db.query(VehicleType).filter(VehicleType.name == "1 TONNER").first()
                elif total_gross_weight <= 4000:
                    vehicle_type = db.query(VehicleType).filter(VehicleType.name == "4 TONNER").first()
                elif total_gross_weight <= 8000:
                    vehicle_type = db.query(VehicleType).filter(VehicleType.name == "8 TONNER").first()
                elif total_gross_weight <= 12000:
                    vehicle_type = db.query(VehicleType).filter(VehicleType.name == "12 TONNER").first()
                elif total_gross_weight <= 15000:
                    vehicle_type = db.query(VehicleType).filter(VehicleType.name == "15 TONNER").first()
                else:
                    vehicle_type = db.query(VehicleType).filter(VehicleType.name == "20 TONNER").first()

            
            order = CustomerOrder(
                order_number=str(order_num),
                customer_name=str(first_row['Customer Name']) if pd.notna(first_row['Customer Name']) else None,
                requested_delivery_date=delivery_date,
                line_item_count=len(group),
                origin_country=str(first_row['From Country']) if pd.notna(first_row['From Country']) else None,
                origin_state=str(first_row['From stare']) if pd.notna(first_row['From stare']) else None,
                destination_country=str(first_row['To country']).strip() if pd.notna(first_row['To country']) else None,
                destination_state=str(first_row['To State']) if pd.notna(first_row['To State']) else None,
                gross_weight_kg=float(total_gross_weight) if pd.notna(total_gross_weight) else None,
                net_weight_kg=float(total_net_weight) if pd.notna(total_net_weight) else None,
                total_width=float(total_width) if pd.notna(total_width) else None,
                delivery_method=delivery_method,
                vehicle_type_id=vehicle_type.id if vehicle_type else None,
                status="pending",
                notes=f"Aggregated from {len(group)} line items from Excel"
            )
            
            db.add(order)
            orders_created += 1
        
        db.commit()
        logger.info(f"Successfully seeded {orders_created} customer orders from Excel")
        
    except Exception as e:
        logger.error(f"Error loading orders from Excel: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()


def init_db():
    """Initialize database with seed data"""
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")
    
    db = SessionLocal()
    
    try:
        seed_vehicle_types(db)
        seed_orders_from_excel(db)
        
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    logger.info("Database initialization complete")
