import uvicorn
from fastapi import FastAPI
from app.routers import post, user, auth, vote

######################################
# Creates the database automatically
######################################

from . import models
from .database import engine
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World"}

# if __name__ == '__main__':
#    app = FastAPI()
#    app.include_router(post.router)
#    app.include_router(user.router)
#    app.include_router(auth.router)
#    app.include_router(vote.router)

#    uvicorn.run(app, host="0.0.0.0", port="9090")


#    @app.get("/")
#    def root():
#        return {"message": "Hello World"}


#    @app.get("/posts")
#    def get_post():
#        return {"message": "Get all posts"}
