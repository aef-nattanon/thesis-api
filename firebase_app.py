from firebase_admin import credentials, firestore, initialize_app, storage


def initialize_firestore():
  # Initialize Firestore DB
  cred = credentials.Certificate('./serviceAccountKey.json')
  default_app = initialize_app(cred, {
      'storageBucket': 'aef-nattanon-thesis.appspot.com'
  })
  db = firestore.client()
  result_images_ref = db.collection('result_images')
  bucket = storage.bucket()

  return cred, default_app, db, result_images_ref, bucket

def firebase_upload_image(image_path, bucket):
    blob = bucket.blob(image_path[2:])
    blob.upload_from_filename(image_path)

    # Opt : if you want to make public access from the URL
    blob.make_public()
    return blob.public_url
