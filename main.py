from re import M
from xmlrpc.client import boolean
from click import option
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()

class Post(BaseModel):
    title: str
    content:str
    published:bool = True
    rating: Optional[int]= None
 
my_posts= [{
    'title': 'Post 1',
    'content': 'Content of post 1', 
    "id":1,
},
{
    'title': 'Post 2',
    'content': 'Content of post 2', 
    "id":2,
}
]

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post
 
       
def find_index_post(id):
    for i, p in enumerate(my_posts):
       if p['id'] == id:    
        return i


@app.get('/posts')
async def root():
    return {'data':my_posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
        print(post)
        post_dict = post.dict()
        # creating an ID for us....
        post_dict['id'] = randrange(0, 1000000)
        my_posts.append(post_dict)
        return {"Data":post_dict}
 

@app.get('/posts/latest')
def get_latest_post():
    post = my_posts[(len(my_posts) - 1)]
    return {'data': post}


@app.get('/posts/{id}')
def posts_details(id: int, res:Response): 
    post = find_post(id) 
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with {id} was not found' )
    #     res.status_code = status.HTTP_404_NOT_FOUND
    #     return {'message': f'post with {id} was not found'}
    return {"post_details": post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT )
def post_delete(id:int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with {id} does not exist' )
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_posts(id: int, post:Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with {id} does not exist' )
     
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"message": post_dict}
    



# @app.post('/createpost')
# def create_posts(payload: dict=Body(...)):
#         return {'New post':f"title {payload['title']} \n content: {payload['content']}"}

  