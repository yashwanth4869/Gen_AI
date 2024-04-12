from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import queryRoute, ragRoute, sqlRoute, userRoute

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(userRoute.router, prefix = '/api/v1')
app.include_router(queryRoute.router, prefix = '/api/v1')
app.include_router(ragRoute.router,prefix='/api/v1')
app.include_router(sqlRoute.router,prefix='/api/v1')