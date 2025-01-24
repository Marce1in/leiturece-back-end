from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.get("/authenticated")
def authenticated():
    pass

@router.post("/login")
def login():
    pass

@router.post("/register")
def register():
    pass

@router.post("/logout")
def logout():
    pass
