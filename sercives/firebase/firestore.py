from firebase_admin.firestore import firestore
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
    os.path.dirname(__file__),
    "firebaseSdk.json",
)

def get_db():
    # [START firestore_setup_client_create_async]
    # The `project` parameter is optional and represents which project the client
    # will act on behalf of. If not supplied, the client falls back to the default
    # project inferred from the environment.
    db = firestore.Client()
    # [END firestore_setup_client_create_async]
    return db


def sendMessage(user,data_raw: dict):
    db = get_db()
    data = {**data_raw, "timestamp": firestore.SERVER_TIMESTAMP,"username":user.username}
    db.collection('message').add(data)


async def cursor_paginate():
    db = get_db()
    # [START firestore_query_cursor_pagination_async]
    cities_ref = db.collection("cities")
    first_query = cities_ref.order_by("population").limit(3)

    # Get the last document from the results
    docs = [d async for d in first_query.stream()]
    last_doc = list(docs)[-1]

    # Construct a new query starting at this document
    # Note: this will not have the desired effect if
    # multiple cities have the exact same population value
    last_pop = last_doc.to_dict()["population"]

    next_query = (
        cities_ref.order_by("population").start_after({"population": last_pop}).limit(3)
    )
    # Use the query for pagination
    # ...
    # [END firestore_query_cursor_pagination_async]

    return next_query
