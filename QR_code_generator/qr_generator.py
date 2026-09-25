from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

from pathlib import Path
import qrcode, os, random

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def main(request: Request, url = None):
    
    random_version = random.randint(1, 10000)
    fullpath = Path.cwd()
    pathpng = f"{fullpath}/static/qrcode.png"
    
    if os.path.exists(pathpng):
        os.remove(pathpng)

    
    if url is not None:
        qr = qrcode.QRCode(
        version=1,  
        error_correction=qrcode.constants.ERROR_CORRECT_H,  
        box_size=10,  
        border=4
        )
    
        qr.add_data(url)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image.save(pathpng)

        
    urlrecieve = {"url": url, "v": random_version, "path": pathpng}
    
    return templates.TemplateResponse(
        request=request,
        name="qr_generator.html",
        context=urlrecieve
        )





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
