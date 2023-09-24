from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user
from app.database import crud, schemas

router = APIRouter(prefix="/birthdays", tags=["birthdays"])


@router.post("/", response_model=schemas.Birthday)
def create_birthday(
    birthday: schemas.BirthdayCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    # Перевіряємо, чи день народження не існує в базі даних
    existing_birthday = crud.get_birthday_by_date(db, date=birthday.date)
    if existing_birthday:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Birthday for this date already exists",
        )

    # Створюємо новий день народження
    new_birthday = crud.create_birthday(
        db, birthday=birthday, owner_id=current_user.id)

    return new_birthday


@router.get("/", response_model=list[schemas.Birthday])
def read_birthdays(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Отримуємо список днів народження
    birthdays = crud.get_birthdays(db, skip=skip, limit=limit)
    return birthdays


@router.get("/{birthday_id}", response_model=schemas.Birthday)
def read_birthday(birthday_id: int, db: Session = Depends(get_db)):
    # Отримуємо інформацію про конкретний день народження за його ID
    birthday = crud.get_birthday(db, birthday_id=birthday_id)
    if birthday is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Birthday not found",
        )
    return birthday
