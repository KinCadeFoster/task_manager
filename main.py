from fastapi import FastAPI


app = FastAPI()


@app.get("/task")
async def get_all_rask():
    return "staus: OK"