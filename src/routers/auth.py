from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..database import get_session
from ..models.auth import User


router = APIRouter(dependencies=[Depends(get_session)])


@router.get("/", response_model=list[User])
def authentication(db: Session = Depends(get_session)):
    ...


@router.post("/verify")
def verify_phone_number():
    ...
