from fastapi import APIRouter

from .auth import router as auth_router
from .employee import router as employee_router
from .employer import router as employer_router


router = APIRouter()

router.include_router(auth_router, tags=["Auth"])
router.include_router(employer_router, tags=["Employers"])
router.include_router(employee_router, tags=["Employees"])


