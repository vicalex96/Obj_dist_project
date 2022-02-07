from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import router as blog_router
# genera la instancia que nos va a devolver la aplicacion
def get_application():
    #instanciamos al FastAPI junto con metadata
    app = FastAPI(title='APlicacion Distribuida', version="1.0.0")
    
    #agregamos un middleware, que nos habilite el CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    
    app.include_router(blog_router, prefix="/api")
    return app
app = get_application()
     