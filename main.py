import uvicorn
# import networkx as nx

from fastapi import FastAPI

from api_v1.routes.views import router as router


app = FastAPI(title="Shortest Path API", version="1.0.0")

app.include_router(router=router)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
