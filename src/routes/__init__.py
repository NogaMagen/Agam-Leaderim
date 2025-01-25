from fastapi import APIRouter

from .auth import router as auth_router
from .employee import router as employee_router
from .employer import router as employer_router

# from .populate_database import router as populate_database


router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(employee_router, prefix="/employees", tags=["Employees"])
router.include_router(employer_router, prefix="/employers", tags=["Employers"])
# router.include_router(populate_database, prefix="/populate_database", tags=["Populate"])
