from fastapi import FastAPI, HTTPException
from src.scrapper.router import router as scrapper_router
from src.cluster.router import router as cluster_router
from src.prisma import prisma

from fastapi.middleware.cors import CORSMiddleware

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"


origins = ["*"]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with the domains you want to allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(scrapper_router, prefix="/scrapper", tags=["scrapper"])
app.include_router(cluster_router, prefix="/cluster", tags=["collections"])



@app.on_event("startup")
async def startup():
    await prisma.connect()

@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI project!"}
