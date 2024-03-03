import firebase_admin
from firebase_admin import credentials, storage
from io import BytesIO

def store_image(image_id, data):
    data_blob = BytesIO(data)
    data_blob.seek(0)

    bucket = storage.bucket()

    blob = bucket.blob(str(image_id))
    
    blob.upload_from_file(data_blob, content_type='image/jpeg')

    blob.make_public()

    print("Your file URL:", blob.public_url)
    return blob.public_url
