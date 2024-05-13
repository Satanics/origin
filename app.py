from fastapi import FastAPI, Depends
from sqlalchemy import Connection
import yaml
from Repositories import MemoryRepository, Repository, PostgresRepository
from Connection import conn


with open('config.yaml') as f:
    config = yaml.safe_load(f)

if config['Repositorytype'] == 'PostgresRepository':
    state = PostgresRepository()
elif config['Repositorytype'] == 'MemoryRepository':
    state = MemoryRepository()

app = FastAPI()

def Repository_factory() -> dict:
    return state

def Connection_factory() -> Connection:
    return conn


@app.get("/")
def select_all_users(state:Repository = Depends(Repository_factory), conn: Connection = Depends(Connection_factory)) -> list:
    return(state.select_all_users())


@app.post('/create/{fio}')
def create_user(fio: str, state:Repository = Depends(Repository_factory), conn: Connection = Depends(Connection_factory)) -> str:
    state.create_user(fio)
    return(fio)


@app.get('/select/{id}')
def select_user(id: int, state:Repository = Depends(Repository_factory), conn: Connection = Depends(Connection_factory)) -> str:
    return state.select_user(id)


@app.delete('/{id}')
def delete_user(id: int, state:Repository = Depends(Repository_factory), conn: Connection = Depends(Connection_factory)) -> str:
    state.delete_user(id)
    return('deleted')

@app.get('/update/{id}/{fio}')
def update_user(id: int, fio: str, state:Repository = Depends(Repository_factory), conn: Connection = Depends(Connection_factory)) -> str:
    state.update_user(id,fio)
    return('updated')