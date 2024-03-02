import requests

# Replace 'your_fastapi_server_url' with the actual URL of your FastAPI server
fastapi_url = 'http://localhost:8000'


# ## Push sample book data to firebase
# user_id = '1010'
# book_id = '101'
# book_data = {
#     "title": "Sample Book random Title 1",
#     "pages": [
#         {
#             "pageNum": 1,
#             "text": "Page 1 Content: Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
#             "images": [
#                 "The Steam Age Exhibit",
#                 "Coal-Powered Steam Train"
#             ]
#         },
#         {
#             "pageNum": 2,
#             "text": "Page 2 Content: Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
#             "images": [
#                 "The Steam Age Exhibit",
#                 "Coal-Powered Steam Train"
#             ]
#         }
#     ]
# }

# response_push_book = requests.post(fastapi_url + f"/api/set_book/{user_id}/{book_id}", json=book_data)
# print(response_push_book.json())



# ### Get book by user id and book id 
# user_id = 1010
# book_id = 101

# response_get_book = requests.get(fastapi_url + f'/api/get_book/{user_id}/{book_id}')
# print(response_get_book.json())


## Create a new user
user = {
    "email": "random@gmail.com",
    }

response_create_user = requests.post(fastapi_url + f'/api/create_user/{1234321}', json=user)
print(response_create_user.json())


# ### Get user id by email
# email = "random@gmail.com"
# response_get_user_id = requests.get(fastapi_url + f'/api/get_user_id/{email}')
# print(response_get_user_id.json())


