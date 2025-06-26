from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from router import endpoints

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://edwardmn.netlify.app"],  # You can restrict this to ["http://localhost:3000"] in production
    allow_credentials=True,
    allow_methods=["*"],  # or ["POST"] if you only use POST
    allow_headers=["*"],
)
app.include_router(endpoints.router)