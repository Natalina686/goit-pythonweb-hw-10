from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, extract, and_
from datetime import date, timedelta, date

from . import models, schemas


def create_contact(db: Session, contact_in: schemas.ContactCreate) -> models.Contact:
    db_obj = models.Contact(**contact_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_contact(db: Session, contact_id: int) -> Optional[models.Contact]:
    return db.get(models.Contact, contact_id)


def search_contacts(
    db: Session,
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[models.Contact]:
    query = db.query(models.Contact)
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                models.Contact.first_name.ilike(like),
                models.Contact.last_name.ilike(like),
                models.Contact.email.ilike(like),
            )
        )
    return query.offset(skip).limit(limit).all()


def update_contact(db: Session, contact_id: int, contact_in: schemas.ContactUpdate) -> Optional[models.Contact]:
    db_obj = db.get(models.Contact, contact_id)
    if not db_obj:
        return None
    for key, value in contact_in.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_contact(db: Session, contact_id: int) -> bool:
    db_obj = db.get(models.Contact, contact_id)
    if not db_obj:
        return False
    db.delete(db_obj)
    db.commit()
    return True


def get_upcoming_birthdays(db: Session, days: int = 7) -> List[models.Contact]:
    today = date.today()
    dates = [( (today + timedelta(days=i)).month, (today + timedelta(days=i)).day ) for i in range(days + 1)]
    
    conds = [and_(extract('month', models.Contact.birthday) == m, extract('day', models.Contact.birthday) == d)
             for m, d in dates]
    query = db.query(models.Contact).filter(or_(*conds))
    return query.all()
