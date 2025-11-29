from fastapi import FastAPI, Request
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

SERVICE_MAP = {
    "equipos": "http://equipos-service:8001",
    "proveedores": "http://proveedores-service:8002",
    "mantenimientos": "http://mantenimiento-service:8003",
    "reportes": "http://reportes-service:8004",
    "agents": "http://agent-service:8005",
}

@app.get("/health")
def health():
    return {"status": "ok", "service": "api-gateway"}

@app.api_route("/api/{service}/{path:path}", methods=["GET","POST","PUT","DELETE"])
async def proxy(service: str, path: str, request: Request):
    if service not in SERVICE_MAP:
        return {"error": f"Service '{service}' not found"}
    url = f"{SERVICE_MAP[service]}/{path}"
    async with httpx.AsyncClient() as client:
        body=await request.body()
        headers=dict(request.headers)
        resp=await client.request(request.method,url,content=body,headers=headers)
        return resp.json()
