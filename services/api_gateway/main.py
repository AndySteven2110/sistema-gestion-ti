from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(title="API Gateway", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MAPA DE MICROSERVICIOS
SERVICE_MAP = {
    "equipos": "http://equipos-service:8001",
    "proveedores": "http://proveedores-service:8002",
    "mantenimientos": "http://mantenimiento-service:8003",
    "reportes": "http://reportes-service:8004",
    "agents": "http://agent-service:8005",
}

@app.get("/health")
async def health():
    return {"status": "ok", "service": "api-gateway"}


# -------------------------------
# FUNCION CENTRAL DE PROXY
# -------------------------------
async def forward(service: str, path: str, request: Request):
    if service not in SERVICE_MAP:
        raise HTTPException(404, f"Servicio '{service}' no existe")

    url = f"{SERVICE_MAP[service]}/{path}"

    async with httpx.AsyncClient() as client:
        body = await request.body()
        resp = await client.request(
            request.method,
            url,
            content=body,
            headers=dict(request.headers)
        )

    # Si la respuesta no es JSON, devolver raw
    try:
        return resp.json()
    except:
        return {"raw": resp.text}


# -------------------------------
# RUTA PRINCIPAL QUE USA EL FRONTEND
# /api/<service>/<path>
# -------------------------------
@app.api_route("/api/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def api_proxy(service: str, path: str, request: Request):
    return await forward(service, path, request)
