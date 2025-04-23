from fastapi import APIRouter, Depends
from app.models.user import User
from app.core.dependencies import get_current_user
from app.core.permissions import require_role
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserRead)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/restricted")
async def admin_area(user: User = Depends(require_role("admin"))):
    return {"msg": f"Acesso liberado, usuário: {user.name}"}
