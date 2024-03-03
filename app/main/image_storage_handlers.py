import firebase_admin
from firebase_admin import credentials, storage
from io import BytesIO

if not firebase_admin._apps:
    cred = credentials.Certificate('path/to/your/serviceAccountKey.json')  # Replace with your JSON credentials file
    firebase_admin.initialize_app(cred, {'storageBucket': 'baggetters-38a7c.appspot.com'})  # Replace with your bucket name

def store_image(image_id, data):
    data_blob = BytesIO(data)
    data_blob.seek(0)

    bucket = storage.bucket()

    blob = bucket.blob(str(image_id))
    
    blob.upload_from_file(data_blob, content_type='image/jpeg')

    blob.make_public()

    print("Your file URL:", blob.public_url)
    return blob.public_url
