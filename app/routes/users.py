from fastapi import APIRouter, Depends
from app.models.user import User
from app.core.dependencies import get_current_user
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserRead)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
