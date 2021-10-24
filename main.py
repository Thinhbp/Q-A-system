import json

import uvicorn
from fastapi import FastAPI,Request,Form,Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import utils


app=FastAPI()

templates=Jinja2Templates(directory='templates')
@app.get('/',response_class=HTMLResponse)

async def index(request: Request):
    return templates.TemplateResponse('index.html',context={'request':request})

@app.post('/',response_class=HTMLResponse)
async def implement(request:Request,question:str=Form(...),paragraph:str=Form(...)):

    result=utils.processing(question,paragraph)
    context={'request':request,"result": result,'question':question,'paragraph':paragraph}
    return templates.TemplateResponse('index.html',context)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=1234)

