from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src import crud, schemas
from src.db import get_db

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/", response_model=schemas.ContactResponse, status_code=201)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db, contact)


@router.get("/", response_model=List[schemas.ContactResponse])
def get_contacts(
    q: Optional[str] = Query(None, description="Search by name, surname or email"),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return crud.search_contacts(db, q=q, skip=skip, limit=limit)


@router.get("/{contact_id}", response_model=schemas.ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    obj = crud.get_contact(db, contact_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Contact not found")
    return obj


@router.put("/{contact_id}", response_model=schemas.ContactResponse)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    obj = crud.update_contact(db, contact_id, contact)
    if not obj:
        raise HTTPException(status_code=404, detail="Contact not found")
    return obj


@router.delete("/{contact_id}", status_code=204)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_contact(db, contact_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Contact not found")
    return None


@router.get("/upcoming-birthdays", response_model=List[schemas.ContactResponse])
def get_birthdays(days: int = 7, db: Session = Depends(get_db)):
    return crud.get_upcoming_birthdays(db, days=days)
