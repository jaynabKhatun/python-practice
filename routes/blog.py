from fastapi import APIRouter
from models.blog import BlogModel, UpdateBlogModel
from config.config import blog_collection
from serializes.blog import DecodeBlogs, DecodeBlog
from bson import ObjectId

import datetime

blog_root = APIRouter()


# post request to the server

@blog_root.post("/blog/new")
def NewBlog(doc: BlogModel):
    doc = dict(doc)
    current_date = datetime.date.today()
    doc["date"] = str(current_date)
    res = blog_collection.insert_one(doc)

    doc_id = str(res.inserted_id)

    return {
        "status": "ok",
        "message": "Blog created successfully",
        "id": doc_id

    }

# getting blogs


@blog_root.get("/all/blogs")
def allBlogs():
    res = blog_collection.find()
    decoded_data = DecodeBlogs(res)

    return {
        "status": "ok",
        "blogs": decoded_data
    }


# get single blog

@blog_root.get("/blog/{_id}")
def getBlog(_id):
    res = blog_collection.find_one({"_id": ObjectId(_id)})

    Decode_data = DecodeBlog(res)
    return {
        "status": "ok",
        "blog": Decode_data
    }


# update a single blog

@blog_root.patch("/update/{_id}")
def updateBlog(_id: str, doc: UpdateBlogModel):
    req = dict(doc.model_dump(exclude_unset=True))
    blog_collection.find_one_and_update(
        {"_id": ObjectId(_id)},
        {"$set": req}
    )

    return {
        "status": "ok",
        "message": "Blog updated successfully"
    }


# deleted a blog


@blog_root.delete("/delete/{_id}")
def deletedBlog(_id: str):
    blog_collection.find_one_and_delete(
        {"_id": ObjectId(_id)}

    )
    return {
        "status": "ok",
        "message": "Blog deleted successfully"
    }
