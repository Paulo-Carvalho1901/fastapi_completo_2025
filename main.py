from fastapi import FastAPI, status

from schema import Message
from routers import auth, users


app = FastAPI(title='Curso de FastAPI')


app.include_router(auth.router)
app.include_router(users.router)



@app.get('/', status_code=status.HTTP_200_OK, response_model=Message)
def get_root():
    return {"message": "Olá mundo!"}



if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)