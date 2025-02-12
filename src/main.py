from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from loguru import logger

from api.router import api_router
from services.db import pool


@asynccontextmanager
async def lifespan(instance: FastAPI):
    logger.info("Opening connection pool")
    await pool.open()

    yield

    logger.info("Closing connection pool")
    await pool.close()


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
