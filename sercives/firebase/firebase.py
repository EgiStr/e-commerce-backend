from firebase_admin import initialize_app, credentials
import os

cred = credentials.Certificate(
    os.path.join(
        os.path.dirname(__file__),
        "firebaseSdk.json",
    )
)

firebase = initialize_app(cred, name="e-commerce")