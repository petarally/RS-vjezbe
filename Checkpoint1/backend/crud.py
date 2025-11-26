from sqlalchemy.orm import Session
from sqlalchemy import and_
import models, schemas
from datetime import date

def get_vehicles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vehicle).offset(skip).limit(limit).all()

def get_vehicle(db: Session, vehicle_id: int):
    return db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()

def create_vehicle(db: Session, vehicle: schemas.VehicleCreate):
    db_vehicle = models.Vehicle(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_reservations(db: Session):
    return db.query(models.Reservation).all()

def create_reservation(db: Session, reservation: schemas.ReservationCreate):
    # Find available vehicle in the requested category
    available_vehicle = find_available_vehicle_in_category(
        db, 
        reservation.category, 
        reservation.start_date, 
        reservation.end_date,
        reservation.preferred_car_model
    )
    
    if not available_vehicle:
        return None  # No vehicle available
    
    # Calculate total price
    days = (reservation.end_date - reservation.start_date).days
    if days == 0:
        days = 1
    total_price = days * available_vehicle.daily_rate
    
    db_reservation = models.Reservation(
        vehicle_id=available_vehicle.id,
        customer_id=reservation.customer_id,
        category=reservation.category,
        preferred_car_model=reservation.preferred_car_model,
        start_date=reservation.start_date,
        end_date=reservation.end_date,
        total_price=total_price
    )
    
    # Update vehicle status
    available_vehicle.status = models.VehicleStatus.RESERVED
    
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def check_vehicle_availability(db: Session, vehicle_id: int, start_date: date, end_date: date):
    """Check if vehicle is available for given dates"""
    overlapping = db.query(models.Reservation).filter(
        and_(
            models.Reservation.vehicle_id == vehicle_id,
            models.Reservation.status.in_([
                models.ReservationStatus.PENDING,
                models.ReservationStatus.CONFIRMED,
                models.ReservationStatus.ACTIVE
            ]),
            models.Reservation.start_date <= end_date,
            models.Reservation.end_date >= start_date
        )
    ).first()
    
    return overlapping is None

def check_category_availability(db: Session, category: str, start_date: date, end_date: date, preferred_model: str = None):
    """Check if any vehicle in the category is available for given dates"""
    vehicle = find_available_vehicle_in_category(db, category, start_date, end_date, preferred_model)
    return vehicle is not None

def find_available_vehicle_in_category(db: Session, category: str, start_date: date, end_date: date, preferred_model: str = None):
    """Find an available vehicle in the specified category for the given dates"""
    # Get all vehicles in the category (not in maintenance)
    vehicles_query = db.query(models.Vehicle).filter(
        and_(
            models.Vehicle.category == category,
            models.Vehicle.status != models.VehicleStatus.MAINTENANCE
        )
    )
    
    # If preferred model is specified, prioritize it
    if preferred_model:
        preferred_vehicles = vehicles_query.filter(models.Vehicle.model == preferred_model).all()
        for vehicle in preferred_vehicles:
            if check_vehicle_availability(db, vehicle.id, start_date, end_date):
                return vehicle
    
    # If no preferred model match, check all vehicles in category
    all_vehicles = vehicles_query.all()
    for vehicle in all_vehicles:
        if check_vehicle_availability(db, vehicle.id, start_date, end_date):
            return vehicle
    
    return None

def get_available_models_in_category(db: Session, category: str):
    """Get all unique car models available in a category"""
    vehicles = db.query(models.Vehicle).filter(
        and_(
            models.Vehicle.category == category,
            models.Vehicle.status != models.VehicleStatus.MAINTENANCE
        )
    ).all()
    
    # Get unique models with brand
    models_list = []
    seen = set()
    for vehicle in vehicles:
        key = f"{vehicle.brand} {vehicle.model}"
        if key not in seen:
            seen.add(key)
            models_list.append({
                "brand": vehicle.brand,
                "model": vehicle.model,
                "display": key,
                "daily_rate": vehicle.daily_rate
            })
    
    return models_list
# Damage Reports CRUD
def get_damage_reports(db: Session, vehicle_id: int = None):
    query = db.query(models.DamageReport)
    if vehicle_id:
        query = query.filter(models.DamageReport.vehicle_id == vehicle_id)
    return query.order_by(models.DamageReport.report_date.desc()).all()

def create_damage_report(db: Session, damage_report: schemas.DamageReportCreate):
    db_report = models.DamageReport(**damage_report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def update_damage_report(db: Session, report_id: int, repaired: int, repair_date: date = None):
    db_report = db.query(models.DamageReport).filter(models.DamageReport.id == report_id).first()
    if db_report:
        db_report.repaired = repaired
        if repair_date:
            db_report.repair_date = repair_date
        db.commit()
        db.refresh(db_report)
    return db_report

# Maintenance Records CRUD
def get_maintenance_records(db: Session, vehicle_id: int = None):
    query = db.query(models.MaintenanceRecord)
    if vehicle_id:
        query = query.filter(models.MaintenanceRecord.vehicle_id == vehicle_id)
    return query.order_by(models.MaintenanceRecord.service_date.desc()).all()

def create_maintenance_record(db: Session, maintenance: schemas.MaintenanceRecordCreate):
    db_maintenance = models.MaintenanceRecord(**maintenance.dict())
    db.add(db_maintenance)
    db.commit()
    db.refresh(db_maintenance)
    return db_maintenance
