from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from routers import database, metrics, professionals, subscriptions, users, dailyMealLogs
app = FastAPI()


app.add_middleware(CORSMiddleware, 
                   allow_origins=["*"], 
                   allow_methods=["*"], 
                   allow_headers=["*"],
                   allow_credentials=True)

app.include_router(database.router)
app.include_router(metrics.router)
app.include_router(professionals.router)
app.include_router(subscriptions.router)
app.include_router(users.router)
app.include_router(dailyMealLogs.router)


@app.get("/")
def root():
    return {"message": "Hello World"}

