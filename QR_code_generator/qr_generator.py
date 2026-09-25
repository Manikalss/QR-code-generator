from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import uvicorn

import qrcode, os
import io, base64

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def main(request: Request, url = None):
    
    qr64 = ""
    
    if url and len(url) < 901:
        qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,  
        box_size=10,  
        border=4
        )
    
        qr.add_data(url)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        bt = io.BytesIO()
        qr_image.save(bt, format="PNG")
        qr64 = base64.b64encode(bt.getvalue()).decode("utf-8")
        
    urlrecieve = {"url": url, "qr64": qr64}
    
    return templates.TemplateResponse(
        request=request,
        name="qr_generator.html",
        context=urlrecieve
        )





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
