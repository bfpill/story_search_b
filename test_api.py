import requests

from app.main.types import Book

# Replace 'your_fastapi_server_url' with the actual URL of your FastAPI server
fastapi_url = 'http://localhost:8000'


### Push sample book data to firebase
user_id = '101'
book_data = {
    "title": "Sample Book 3 Title",
    "pages": [
        {
            "pageNum": 1,
            "text": "Page 1 Content: Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "images": [
                { "src": "image1.jpg", "position": { "x": 100, "y": 100 } },
                { "src": "image2.jpg", "position": { "x": 200, "y": 200 } }
            ]
        },
        {
            "pageNum": 2,
            "text": "Page 2 Content: Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "images": [
                { "src": "image3.jpg", "position": { "x": 50, "y": 50 } }
            ]
        }
    ]
}

data_to_store = {"user_id": user_id, "book": book_data}
response_push_book = requests.post(fastapi_url + '/api/save_book', json=data_to_store)
print(response_push_book.json())


# ### Get all book ids of user
# user_id = '101'
# response_get_books = requests.get(fastapi_url + f'/api/get_books/{user_id}')
# print(fastapi_url + f'/api/get_user_book_ids/{user_id}')
# print(response_get_books.json())
