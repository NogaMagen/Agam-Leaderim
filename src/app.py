from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from data.scripts import PopulateDataBase
from routes import router

app = FastAPI()
populate = PopulateDataBase()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event("startup")
async def startup_event():
    populate.populate_employees()
    populate.populate_employers()