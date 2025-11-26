from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from models import VehicleStatus, ReservationStatus

class VehicleBase(BaseModel):
    brand: str
    model: str
    year: int
    category: str
    registration_number: str
    daily_rate: float
    fuel_type: str = "benzin"
    transmission: str = "manual"
    seats: int = 5
    
    # Registration and compliance
    registration_expiry: Optional[date] = None
    last_inspection_date: Optional[date] = None
    next_inspection_due: Optional[date] = None
    
    # Insurance
    insurance_company: Optional[str] = None
    insurance_policy_number: Optional[str] = None
    insurance_expiry: Optional[date] = None
    insurance_premium: Optional[float] = None
    
    # Leasing/Ownership
    ownership_type: str = "owned"
    lease_company: Optional[str] = None
    lease_start_date: Optional[date] = None
    lease_end_date: Optional[date] = None
    lease_monthly_payment: Optional[float] = None
    
    # Maintenance
    last_service_date: Optional[date] = None
    next_service_due: Optional[date] = None
    service_interval_km: int = 15000

class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: int
    mileage: int
    status: VehicleStatus
    
    class Config:
        from_attributes = True

class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    oib: str
    drivers_license: str
    city: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    
    class Config:
        from_attributes = True

class ReservationBase(BaseModel):
    customer_id: int
    category: str
    preferred_car_model: Optional[str] = None
    start_date: date
    end_date: date

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int
    vehicle_id: Optional[int] = None
    total_price: float
    status: ReservationStatus
    
    class Config:
        from_attributes = True

class DamageReportBase(BaseModel):
    vehicle_id: int
    reservation_id: Optional[int] = None
    report_date: date
    description: str
    severity: str = "minor"
    repair_cost: Optional[float] = None
    repaired: int = 0
    repair_date: Optional[date] = None
    notes: Optional[str] = None

class DamageReportCreate(DamageReportBase):
    pass

class DamageReport(DamageReportBase):
    id: int
    
    class Config:
        from_attributes = True

class MaintenanceRecordBase(BaseModel):
    vehicle_id: int
    service_date: date
    service_type: str
    mileage_at_service: int
    cost: float
    performed_by: Optional[str] = None
    description: Optional[str] = None
    next_service_km: Optional[int] = None

class MaintenanceRecordCreate(MaintenanceRecordBase):
    pass

class MaintenanceRecord(MaintenanceRecordBase):
    id: int
    
    class Config:
        from_attributes = True

class ReservationDetail(Reservation):
    vehicle: Vehicle
    customer: Customer
    
    class Config:
        from_attributes = True