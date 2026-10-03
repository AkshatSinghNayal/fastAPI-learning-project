from fastapi import FastAPI, Depends,HTTPException
from sqlalchemy.orm import Session
from database import engine, sessionFactory
import models,schemas
from auth import create_token,verify

app = FastAPI()


def get_db():
    db = sessionFactory()
    try:
        yield db
    finally:
        db.close()


models.Base.metadata.create_all(bind=engine)

#loginapi
@app.post("/login")
def login():
    return{
        "access_token" : create_token({"user" : "admin"}),
        "token_type" : "bearer"
    }


#create blog
@app.post("/blogs", response_model=schemas.BlogResponse)
def create_post(blog:schemas.BlogCreate, db:Session = Depends(get_db), user = Depends(verify)):
    newBlod = models.Blog(
        title = blog.title,
        content = blog.content
    )
    db.add(newBlod)
    db.commit()
    db.refresh(newBlod)

    return newBlod


#read all blog
@app.get("/getBlogs", response_model=list[schemas.BlogResponse])
def get_posts(db : Session = Depends(get_db)):
    return db.query(models.Blog).all()


#get by id
@app.get("/blog/{id}", response_model=schemas.BlogResponse)
def getByID(id : int , db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id ).first()

    if not blog:
        raise HTTPException(status_code=404 , detail="post related to id not found")

    return blog


#deletion

@app.delete("/delete/{id}")
def delete_by_id(id:int , db : Session = Depends(get_db)):
    post = db.query(models.Blog).filter(models.Blog.id == id ).first()
    db.delete(post)
    db.commit()




#update by id
@app.put("/update/{id}", response_model=schemas.BlogResponse)
def update_by_id( id : int , temp: schemas.BlogCreate, db : Session  = Depends(get_db)):
    post = db.query(models.Blog).filter(models.Blog.id == id ).first()
    post.title = temp.title
    post.content = temp.content
    db.commit()
    db.refresh(post)

    return post











# Your exact execution flow
# Suppose the user sends:
# POST /blogs
# Authorization: Bearer HELLO123

# and body:
# {
#     "title": "My Blog",
#     "content": "Hello"
# }

# FastAPI first looks at:
# @app.post("/blogs")def create_post(    blog: schemas.BlogCreate,    db: Session = Depends(get_db),    user = Depends(verify)):


# It says:
# I need 3 things:

# blog
# db
# user

# Getting blog
# FastAPI reads body:
# {
#     "title": "My Blog",
#     "content": "Hello"
# }

# and creates:
# blog


# Getting db
# It sees:
# Depends(get_db)


# So roughly:
# db = get_db()


# Getting user
# It sees:
# Depends(verify)


# So it wants to do:
# user = verify(...)


# But FastAPI looks at verify:
# def verify(token: str = Depends(oauth2_schema)):


# It realizes:
# Wait.

# verify() itself needs `token`.

# Where do I get token?

# Answer:
# Depends(oauth2_schema)


# So FastAPI executes the dependency:
# token = oauth2_schema(request)


# oauth2_schema checks:
# Authorization: Bearer HELLO123

# and returns:
# token = "HELLO123"


# Then FastAPI can finally call:
# user = verify("HELLO123")


# Now inside:
# def verify(token):    try:        payload = jwt.decode(            token,            SECRECT_KEY,            algorithms=ALGO        )        return payload    except JWTError:        raise HTTPException(...)


# Imagine "HELLO123" is actually a valid JWT.
# Then:
# payload = {    "user": "admin",    "exp": ...}


# So:
# return payload


# means:
# user = {    "user": "admin",    "exp": ...}


# Now FastAPI finally executes:
# create_post(    blog=blog,    db=db,    user={        "user": "admin",        "exp": ...    })


# That's the entire chain.