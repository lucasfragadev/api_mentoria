from fastapi import FastAPI

app = FastAPI()

@app.get("/health") # O @app.get e o decorator // O que ta entre parenteses e o path // path = url = "/"
def health():
   return {"status": "OK"} 