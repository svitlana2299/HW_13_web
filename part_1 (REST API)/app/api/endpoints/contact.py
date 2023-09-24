from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user
from app.database import crud, schemas

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=schemas.Contact)
def create_contact(
    contact: schemas.ContactCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    # Перевіряємо, чи контакт не існує в базі даних
    existing_contact = crud.get_contact_by_name(db, name=contact.name)
    if existing_contact:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contact with this name already exists",
        )

    # Створюємо новий контакт
    new_contact = crud.create_contact(
        db, contact=contact, owner_id=current_user.id)

    return new_contact


@router.get("/", response_model=list[schemas.Contact])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Отримуємо список контактів
    contacts = crud.get_contacts(db, skip=skip, limit=limit)
    return contacts


@router.get("/{contact_id}", response_model=schemas.Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    # Отримуємо інформацію про конкретний контакт за його ID
    contact = crud.get_contact(db, contact_id=contact_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )
    return contact
