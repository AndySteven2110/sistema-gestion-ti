from fastapi import FastAPI
from pydantic import BaseModel
import asyncpg

app = FastAPI(title="Mantenimiento Service", version="1.0")
DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/ti_management"

class MantenimientoIn(BaseModel):
    equipo_id: int
    tipo: str
    descripcion: str
    fecha_programada: str = None
    fecha_realizada: str = None
    costo: float = 0.0
    tecnico_id: int = None
    prioridad: str = None

@app.get("/health")
def health():
    return {"status":"ok","service":"mantenimiento-service"}

@app.post("/mantenimientos")
async def crear_mantenimiento(data: MantenimientoIn):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        async with conn.transaction():
            q1 = '''INSERT INTO mantenimientos (
                equipo_id, tipo, descripcion, fecha_programada,
                fecha_realizada, costo, tecnico_id, prioridad
            ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8)
            RETURNING id;'''
            mid = await conn.fetchval(q1, data.equipo_id,data.tipo,data.descripcion,
                data.fecha_programada,data.fecha_realizada,data.costo,
                data.tecnico_id,data.prioridad)

            await conn.execute(
                "UPDATE equipos SET estado_operativo='En reparación' WHERE id=$1",
                data.equipo_id)

            await conn.execute(
                "INSERT INTO notificaciones (equipo_id,tipo,mensaje) VALUES ($1,'mantenimiento','Nuevo mantenimiento registrado')",
                data.equipo_id)

        return {"status":"created","mantenimiento_id": mid}
    except Exception as e:
        return {"error": str(e)}
    finally:
        await conn.close()

@app.get("/mantenimientos")
async def listar():
    conn = await asyncpg.connect(DATABASE_URL)
    rows = await conn.fetch("SELECT * FROM mantenimientos ORDER BY id DESC")
    await conn.close()
    return rows
