from fastapi import FastAPI, HTTPException
import asyncio

app = FastAPI(title="Sistema de Citas Médicas")

# Base de datos simulada en memoria
citas = []

@app.get("/")
async def home():
    return {"mensaje": "Bienvenido al Sistema de Citas Médicas"}

# 1. CREAR CITA (con delay de 2 segundos y validación)
@app.post("/citas")
async def crear_cita(paciente: str, especialidad: str):
    # Validación básica
    if not paciente or paciente.strip() == "":
        raise HTTPException(status_code=400, detail="El nombre del paciente es obligatorio")

    # Simulación de delay de 2 segundos (Requisito)
    await asyncio.sleep(2)

    nueva_cita = {
        "id": len(citas) + 1,
        "paciente": paciente,
        "especialidad": especialidad,
        "estado": "Programada"
    }
    citas.append(nueva_cita)
    return nueva_cita

# 2. LISTAR CITAS
@app.get("/citas")
async def listar_citas():
    return citas

# 3. BUSCAR CITA POR PACIENTE
@app.get("/citas/buscar/{nombre_paciente}")
async def buscar_cita(nombre_paciente: str):
    resultados = [c for c in citas if nombre_paciente.lower() in c["paciente"].lower()]
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron citas para ese paciente")
    return resultados

# 4. CANCELAR CITA (DELETE)
@app.delete("/citas/{cita_id}")
async def cancelar_cita(cita_id: int):
    for i, cita in enumerate(citas):
        if cita["id"] == cita_id:
            cita_cancelada = citas.pop(i)
            return {"mensaje": "Cita cancelada con éxito", "cita": cita_cancelada}
    
    raise HTTPException(status_code=404, detail="ID de cita no encontrado")