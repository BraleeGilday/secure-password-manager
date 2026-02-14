from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pwd_generator import pwd_gen_router

from user.user_router import router as user_router

from user.user_router import router as user_router
from credential.credential_router import router as credential_router

# https://fastapi.tiangolo.com/tutorial/cors/#use-corsmiddleware

app = FastAPI()

# backend address + port (change to https?)
# need to add frontend address (localhost:<different port>)
# will need to see how to redo for cloud deployment
# (as simple as containerize + nginx?)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(routers, tags[]) go here
app.include_router(credential_router, tags=["credential"])
app.include_router(user_router, tags=["User"])
app.include_router(pwd_gen_router.router, tags=["Password"])


# to be removed
@app.get("/")
async def main():
    return {"message": "Hello world!"}
