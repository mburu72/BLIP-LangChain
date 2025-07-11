from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from router import endpoints

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(endpoints.router)
