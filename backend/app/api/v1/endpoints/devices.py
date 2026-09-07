from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.device import Device
from app.schemas.device import DeviceOut, DeviceCreate, DeviceUpdate

router = APIRouter()


@router.get("/", response_model=List[DeviceOut])
def get_devices(db: Session = Depends(get_db)):
    devices = db.query(Device).all()
    return devices


@router.post("/", response_model=DeviceOut)
def create_device(device_in: DeviceCreate, db: Session = Depends(get_db)):
    existing = db.query(Device).filter(Device.device_id == device_in.device_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Device ID already registered")
    
    device = Device(**device_in.model_dump())
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


@router.get("/{device_id}", response_model=DeviceOut)
def get_device(device_id: str, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.put("/{device_id}", response_model=DeviceOut)
def update_device(device_id: str, device_in: DeviceUpdate, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    update_data = device_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(device, field, value)
        
    db.commit()
    db.refresh(device)
    return device
