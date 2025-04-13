from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def home():  # noqa: ANN201
    return {"message": "Hello, FastAPI!"}
