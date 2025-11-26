from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import models, schemas, crud
from database import engine, get_db
from vehicle_api import search_makes, search_models, get_all_makes, get_models_for_make

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rent-a-Car API")

# Add CORS middleware for Vue.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:8080"],  # Vue dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Rent-a-Car API"}

# Vehicles
@app.get("/api/vehicles", response_model=List[schemas.Vehicle])
def get_vehicles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_vehicles(db, skip=skip, limit=limit)

@app.get("/api/vehicles/{vehicle_id}", response_model=schemas.Vehicle)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = crud.get_vehicle(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@app.post("/api/vehicles", response_model=schemas.Vehicle)
def create_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    return crud.create_vehicle(db, vehicle)

# Customers
@app.get("/api/customers", response_model=List[schemas.Customer])
def get_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_customers(db, skip=skip, limit=limit)

@app.post("/api/customers", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)

# Reservations
@app.get("/api/reservations", response_model=List[schemas.ReservationDetail])
def get_reservations(db: Session = Depends(get_db)):
    reservations = crud.get_reservations(db)
    return reservations

@app.post("/api/reservations", response_model=schemas.Reservation)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    # Check category availability
    if not crud.check_category_availability(
        db, reservation.category, reservation.start_date, reservation.end_date, reservation.preferred_car_model
    ):
        raise HTTPException(status_code=400, detail="Nema dostupnih vozila u odabranoj kategoriji za odabrane datume")
    
    db_reservation = crud.create_reservation(db, reservation)
    if not db_reservation:
        raise HTTPException(status_code=400, detail="Greška pri kreiranju rezervacije")
    
    return db_reservation

@app.get("/api/categories/{category}/availability")
def check_category_availability(
    category: str,
    start_date: date,
    end_date: date,
    preferred_model: Optional[str] = None,
    db: Session = Depends(get_db)
):
    available = crud.check_category_availability(db, category, start_date, end_date, preferred_model)
    
    # Get available models in this category
    models_list = crud.get_available_models_in_category(db, category) if available else []
    
    return {
        "available": available,
        "category": category,
        "available_models": models_list
    }

@app.get("/api/categories/{category}/models")
def get_models_in_category(category: str, db: Session = Depends(get_db)):
    """Get all available car models in a specific category"""
    models_list = crud.get_available_models_in_category(db, category)
    return {
        "category": category,
        "count": len(models_list),
        "models": models_list
    }

@app.get("/api/vehicles/{vehicle_id}/availability")
def check_availability(
    vehicle_id: int,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):
    available = crud.check_vehicle_availability(db, vehicle_id, start_date, end_date)
    return {"available": available}

# Car Makes and Models Autocomplete Endpoints
@app.get("/api/car-makes")
def get_car_makes(q: Optional[str] = Query(None, description="Search query for filtering makes")):
    """
    Get all car makes or search by query
    - **q**: Optional search query (e.g., 'toy' returns Toyota, etc.)
    """
    if q:
        results = search_makes(q)
    else:
        results = get_all_makes()
    
    return {
        "count": len(results),
        "results": results
    }

@app.get("/api/car-makes/{make}/models")
def get_car_models(
    make: str,
    q: Optional[str] = Query(None, description="Search query for filtering models")
):
    """
    Get all models for a specific car make or search by query
    - **make**: Car make name (e.g., 'Toyota')
    - **q**: Optional search query (e.g., 'cor' returns Corolla, etc.)
    """
    if q:
        results = search_models(make, q)
    else:
        results = get_models_for_make(make)
    
    if not results:
        raise HTTPException(status_code=404, detail=f"No models found for make: {make}")
    
    return {
        "make": make,
        "count": len(results),
        "results": results
    }

# Damage Reports
@app.get("/api/damage-reports", response_model=List[schemas.DamageReport])
def get_damage_reports(vehicle_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_damage_reports(db, vehicle_id=vehicle_id)

@app.post("/api/damage-reports", response_model=schemas.DamageReport)
def create_damage_report(damage_report: schemas.DamageReportCreate, db: Session = Depends(get_db)):
    return crud.create_damage_report(db, damage_report)

@app.put("/api/damage-reports/{report_id}")
def update_damage_report(report_id: int, repaired: int, repair_date: Optional[date] = None, db: Session = Depends(get_db)):
    report = crud.update_damage_report(db, report_id, repaired, repair_date)
    if not report:
        raise HTTPException(status_code=404, detail="Damage report not found")
    return report

# Maintenance Records
@app.get("/api/maintenance-records", response_model=List[schemas.MaintenanceRecord])
def get_maintenance_records(vehicle_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_maintenance_records(db, vehicle_id=vehicle_id)

@app.post("/api/maintenance-records", response_model=schemas.MaintenanceRecord)
def create_maintenance_record(maintenance: schemas.MaintenanceRecordCreate, db: Session = Depends(get_db)):
    return crud.create_maintenance_record(db, maintenance)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
