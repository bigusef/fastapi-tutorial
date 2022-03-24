from fastapi import FastAPI, HTTPException, status

from .routers import auth
from .settings import get_settings


settings = get_settings()

app = FastAPI(
    title="Wasla Mobile App",
    description="""this application is a hub between online/offline stores from one side and delivery Individuals/companies from the other side. this platform helps a store to find various delivery options based on its location and find the best delivery deals. as a delivery entity, I search for the most attractive requests and try to finalize deals.""",
    version="0.1.0",
    terms_of_service="/legals",
    license_info={"name": "Proprietary license"},
    contact={
        "name": "Appzone Technology",
        "url": "https://appzone-technology.com",
        "email": "info@appzone-technology.com",
    },
    openapi_url="/docs-files/v1.json",
    # docs_url=None,
    # redoc_url="/docs" if settings.is_debugging else None,
)


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
