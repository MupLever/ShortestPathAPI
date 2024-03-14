import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api_v1.routes.views import router as router
from api_v1.auth.views import router as auth_router
from api_v1.users.views import router as users_router
from api_v1.addresses.views import router as addresses_router

app = FastAPI(title="Shortest Path API", version="1.0.0")

app.include_router(router=router)
app.include_router(router=users_router)
app.include_router(router=auth_router)
app.include_router(router=addresses_router)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PUT"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, log_config="log_conf.yaml")
