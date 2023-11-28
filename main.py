from fastapi import FastAPI, HTTPException
from starlette import status

from config import lifespan, RequestContextMiddleware
from app.routers import root_router

app = FastAPI(lifespan=lifespan)

# Application Middlewares
app.add_middleware(RequestContextMiddleware)

# include application root router
app.include_router(root_router)


@app.get("/healthz", include_in_schema=False)
async def healthcheck():
    return {"result": "OK - healthy"}


@app.get("/", include_in_schema=False)
async def root_path():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="You are in the wrong place :(",
    )
