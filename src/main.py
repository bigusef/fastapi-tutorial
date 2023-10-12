from fastapi import FastAPI, HTTPException, status

from .routers import auth
from .settings import get_settings


settings = get_settings()

app = FastAPI()


# region App Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# endregion


@app.get("/healthz", include_in_schema=False)
async def healthcheck():
    return {"result": "OK - healthy"}


@app.get("/", include_in_schema=False)
def root_path():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="You are in the wrong place :(",
    )
