from fastapi import APIRouter
from models.blog import BlogModel
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


# single blog

@blog_root.get("/blog/{_id}")
def getBlog(_id):
    res = blog_collection.find_one({"_id": ObjectId(_id)})

    Decode_data = DecodeBlog(res)
    return {
        "status": "ok",
        "blog": Decode_data
    }
