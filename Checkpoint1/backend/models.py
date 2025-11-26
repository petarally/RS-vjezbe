from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum, Boolean, Text
from sqlalchemy.orm import relationship
from database import Base
import enum

class VehicleStatus(str, enum.Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    RENTED = "rented"
    MAINTENANCE = "maintenance"

class ReservationStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    category = Column(String, nullable=False)  # economy, suv, luxury
    registration_number = Column(String, unique=True, nullable=False)
    daily_rate = Column(Float, nullable=False)
    mileage = Column(Integer, default=0)
    status = Column(Enum(VehicleStatus), default=VehicleStatus.AVAILABLE)
    fuel_type = Column(String, default="benzin")
    transmission = Column(String, default="manual")
    seats = Column(Integer, default=5)
    
    # Registration and compliance
    registration_expiry = Column(Date, nullable=True)
    last_inspection_date = Column(Date, nullable=True)
    next_inspection_due = Column(Date, nullable=True)
    
    # Insurance
    insurance_company = Column(String, nullable=True)
    insurance_policy_number = Column(String, nullable=True)
    insurance_expiry = Column(Date, nullable=True)
    insurance_premium = Column(Float, nullable=True)
    
    # Leasing/Ownership
    ownership_type = Column(String, default="owned")  # owned, leased, financed
    lease_company = Column(String, nullable=True)
    lease_start_date = Column(Date, nullable=True)
    lease_end_date = Column(Date, nullable=True)
    lease_monthly_payment = Column(Float, nullable=True)
    
    # Maintenance and condition
    last_service_date = Column(Date, nullable=True)
    next_service_due = Column(Date, nullable=True)
    service_interval_km = Column(Integer, default=15000)
    
    reservations = relationship("Reservation", back_populates="vehicle")
    damage_reports = relationship("DamageReport", back_populates="vehicle", cascade="all, delete-orphan")
    maintenance_records = relationship("MaintenanceRecord", back_populates="vehicle", cascade="all, delete-orphan")

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, nullable=False)
    oib = Column(String, unique=True, nullable=False)
    drivers_license = Column(String, nullable=False)
    city = Column(String)
    
    reservations = relationship("Reservation", back_populates="customer")

class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)  # Nullable - assigned later
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    category = Column(String, nullable=False)  # Required - customer reserves by category
    preferred_car_model = Column(String, nullable=True)  # Optional - preferred car model
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.PENDING)
    
    vehicle = relationship("Vehicle", back_populates="reservations")
    customer = relationship("Customer", back_populates="reservations")
    damage_reports = relationship("DamageReport", back_populates="reservation")

class DamageReport(Base):
    __tablename__ = "damage_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    reservation_id = Column(Integer, ForeignKey("reservations.id"), nullable=True)
    report_date = Column(Date, nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String, nullable=False)  # minor, moderate, major
    repair_cost = Column(Float, nullable=True)
    repaired = Column(Boolean, default=False)
    repair_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    
    vehicle = relationship("Vehicle", back_populates="damage_reports")
    reservation = relationship("Reservation", back_populates="damage_reports")

class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    service_date = Column(Date, nullable=False)
    service_type = Column(String, nullable=False)  # oil_change, tire_rotation, brake_service, general_service, inspection
    mileage_at_service = Column(Integer, nullable=True)
    cost = Column(Float, nullable=True)
    performed_by = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    next_service_km = Column(Integer, nullable=True)
    
    vehicle = relationship("Vehicle", back_populates="maintenance_records")
