from fastapi import FastAPI, HTTPException
from datetime import datetime
import json
import uvicorn

app = FastAPI(title="Monitor-Consultor API", version="1.0.0")

# Variable global para almacenar el mensaje
global_data = {
    "content": None,
    "last_date": None
}

asking_state={
    "state":False
}


@app.get("/monitor_ask")
async def endpoint_monitor_ask():
    """
    Endpoint que recibe un mensaje, lo encripta y guarda globalmente
    """

    try:
        return asking_state
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando mensaje: {str(e)}")

@app.get("/monitor_send/{mensaje}")
async def endpoint_monitor_send(mensaje:str):
    """
    Endpoint que recibe un mensaje, lo encripta y guarda globalmente
    """

    try:
        global_data["content"]=mensaje
        global_data["last_date"]=datetime.now().strftime("%d-%m-%Y | %H:%M:%S")
        asking_state["state"]=False
        return {
            "status": "success",
            "message": global_data["content"],
            "timestamp": global_data["last_date"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando mensaje: {str(e)}")

@app.get("/consultor_request")
async def endpoint_consultor_request():
    try:
        asking_state["state"]=True
        return {"request":"sent"}
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error procesando mensaje: {str(e)}")

@app.get("/consultor_get")
async def endpoint_consultor_get():
    return global_data

@app.get("/")
async def root():
    return {
        "message": "API Monitor-Consultor funcionando",
        "endpoints": {
            "monitor": "POST /monitor - Recibe y guarda mensajes encriptados",
            "consultor": "GET /consultor - Consulta el último mensaje"
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)