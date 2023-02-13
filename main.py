from fastapi import FastAPI
import scraper_ciudad as _scraper_ciudad
import scraper_todas_ciudades as _scraper_todas_las_ciudades

app  = FastAPI()

@app.get("/")
async def root():
    return {"Descarga de datos por ciudad y/o categoria"}

@app.get("/Consulta de datos por ciudad especifica") 
async def datos_por_ciudad(numero: int):
    return _scraper_ciudad._ciudad_individual(numero)

@app.get("/Consulta de datos de todas las ciudades") 
async def todos_los_datos_por_ciudades():
    return _scraper_todas_las_ciudades._todas_las_ciudades()