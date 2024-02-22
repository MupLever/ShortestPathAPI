import uvicorn

from fastapi import FastAPI

from api_v1.routes.views import router as router
from api_v1.users.views import router as users_router

app = FastAPI(title="Shortest Path API", version="1.0.0")

app.include_router(router=router)
app.include_router(router=users_router)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
