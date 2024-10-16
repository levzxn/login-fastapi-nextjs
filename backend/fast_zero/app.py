from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fast_zero.routers import docs
from fast_zero.middlewares import AuthMiddleware
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI, Request




app = FastAPI(docs_url="/documentation")
origins = ['http://localhost:3000']
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']

)
app.add_middleware(AuthMiddleware)
app.include_router(docs.router)

register_tortoise(
    app,
    db_url="postgres://postgres:Lucasfr420@localhost:5432/DOEM",
    modules={'models': ['fast_zero.models']},
    generate_schemas=True
)


@app.get('/')
async def root():
    return 'Rota Principal'