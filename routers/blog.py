from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import DateTime
from utils.oauth2 import get_current_user
from utils import oauth2
from datetime import datetime


import schemas
import models
import database
import uuid

getdb = database.getdb
router = APIRouter(tags=["the blog-section ;)"])


def format_blog_date(date_published):
    return date_published.isoformat() if date_published else None


@router.get("/images/{filename}")
def get_image(filename: str):
    if not filename:
        raise HTTPException(
            status_code=404, detail="image not found, try again :)")
    return FileResponse(f"images/{filename}")


@router.get("/blog", response_model=list[schemas.ShowBlog], description="BLOGS BLOGS BLOGGSSSS")
def BLOGS(db: Session = Depends(getdb)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get("/blog/{id}", response_model=schemas.ShowBlog, description="I SEE YOU'RE LOOKING FOR A POST... PUT THE ID THEN?")
def find_your_blog_by_id(id: int, db: Session = Depends(getdb)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=404, detail="sorry, blog post not found. try creating one instead :)")

    return blog.first()


@router.get("/blog_categories", description="DIFFERENT THINGS WE HAVE BUT WE'RE GLAD TO HAVE YOU :)")
def get_our_blog_categories():
    return schemas.CATEGORY


@router.get("/blog_category-by-id//{category_id}", description="LOOKING FOR SOMEWHERE TO READ FROM? INPUT THE ID ;)")
def get_any_category_of_blogs_available_by_id(category_id: int):
    if category_id not in schemas.CATEGORY:
        return {"no such blog category, try another"}
    return schemas.CATEGORY[category_id]


@router.post("/create-blog", description="TRYING TO CREATE? TAKE YOUR TIME BUT DON'T WASTE TIME - ONE KEY TO SUCCESS")
async def create_a_blog(name: str = Form(...), body: str = Form(...), owner_id: int = Form(...), file: UploadFile = File(...), db: Session = Depends(getdb), current_user=Depends(oauth2.get_current_user)):

    content = await file.read()
    filename = f"images/{uuid.uuid4()}.jpg"

    with open(filename, "wb") as f:
        f.write(content)
    date_published = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_blog = models.Blog(name=name, body=body, owner_id=owner_id,
                           url=f"https://blog-1-k4272118.deta.app/{filename}")

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return {new_blog, date_published}


# @router.post("/create-blog-in-category", response_model=schemas.BlogCategory, description="NEW POST? YOU GOT THIS!")
# async def create_a_post_in_a_category(id: int, name: str = Form(...), body: str = Form(...), owner: int = Form(...), file: UploadFile = File(...), db: Session = Depends(getdb), current_user=Depends(oauth2.get_current_user)):

#     content = await file.read()
#     filename = f"images/{uuid.uuid4()}.jpg"

#     with open(filename, "wb") as f:
#         f.write(content)
#     date_published = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     new_blog = schemas.CATEGORY
#     if id not in schemas.CATEGORY:
#         return "category not found"
#     schemas.CATEGORY[new_blog]

#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)

#     return {new_blog, date_published}

@router.post("/create-blog-in-category", description="NEW POST? YOU GOT THIS!")
async def create_a_post_in_a_category(id: int, name: str, body: str, db: Session = Depends(getdb), current_user=Depends(oauth2.get_current_user)):

    # content = await file.read()
    # filename = f"images/{uuid.uuid4()}.jpg"

    # with open(filename, "wb") as f:
    #     f.write(content)

    date_published = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_blog = schemas.BlogCategory(
        name=name, body=body, date_published=date_published)

    category = db.query(models.Category).filter(
        models.Category.id == id).first()
    if not category:
        return "Category not found"

    new_blog.category = category

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@router.put("/blog/{username}{id}", response_model=schemas.ShowBlog, description="HMM, UNSATISFIED WITH YOUR WORK? NO WAHALAS. GO AHEAD, DO AT WILL")
def update_your_blog_post(req: schemas.UpdateBlog, username: str, id: int, db: Session = Depends(getdb), current_user=Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=404, detail="login to update your blog post:)")

    if not blog.first():
        raise HTTPException(
            status_code=404, detail="blog not found :(")

    blog.update(req.dict())

    db.commit()

    return blog.first()


@router.delete("/blog/", description="TIRED OF YOUR MASTER-PIECE? OH BUMMERRR")
def delete_your_blog_post(id: int, db: Session = Depends(getdb), current_user=Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        return {"couldn't find blog :("}

    blog.delete()
    db.commit()

    return {"blog deleted successfully :)"}
