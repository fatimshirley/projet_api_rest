from fastapi import FastAPI, HTTPException
from plat import plats

app = FastAPI()

@app.get("/plat")
def get_plats():
    return plats

@app.get("/plat/{plat_id}")
def get_plat_by_id(plat_id: int):
    for plat in plats:
        if plat["id"] == plat_id:
            return plat

    raise HTTPException(
        status_code=404,
        detail="Plat non trouvé"
    )

def somme(data:list[int])


