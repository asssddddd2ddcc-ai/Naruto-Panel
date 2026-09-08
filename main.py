import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI(title="Uchiha Marzban Panel")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

USERS_DB = [
    {"username": "Sasuke_Uchiha", "protocol": "VLESS-XHTTP", "used": "45 GB", "total": "100 GB", "status": "active"},
    {"username": "Madara_Uchiha", "protocol": "Trojan-WS", "used": "890 GB", "total": "Unlimited", "status": "active"},
    {"username": "Shisui_Uchiha", "protocol": "VLESS-GRPC", "used": "50 GB", "total": "50 GB", "status": "expired"}
]

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "users": USERS_DB,
        "admin_user": os.getenv("ADMIN_USERNAME", "Itachi_Uchiha")
    })

@app.get("/sub/{username}", response_class=HTMLResponse)
async def subscription_page(request: Request, username: str):
    user = next((u for u in USERS_DB if u["username"].lower() == username.lower()), None)
    if not user:
        user = {"username": username, "protocol": "VLESS-WS", "used": "12 GB", "total": "50 GB", "status": "active"}
    
    sub_link = f"vless://uchiha-clan-secret-uuid@clean-ip.cloudflare.com:443?type=ws&security=tls&path=%2Fuchiha#{username}_Sharingan"
    
    return templates.TemplateResponse("subscription.html", {
        "request": request,
        "user": user,
        "sub_link": sub_link
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
