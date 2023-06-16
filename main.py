from fastapi import FastAPI, HTTPException, status
from config import settings

from auth.routers import router as auth_router
from provider.routers import router as provider_router

app = FastAPI(
    title="Test App",
    description="",
    version="0.1.0",
)

app.include_router(auth_router)
app.include_router(provider_router)


@app.get("/", include_in_schema=False)
def root_path():
    print(settings.database_url)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="You are in the wrong place :(",
    )


@app.get("/healthz", include_in_schema=False)
async def healthcheck():
    print(settings.database_url)
    return {"result": "OK - healthy"}
