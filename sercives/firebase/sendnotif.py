from .firebase import firebase
import datetime
from firebase_admin import messaging

# create firebase project in console.firebase and generated key for admin


def send_notif_device(
    registration_token="",
    data={},
    title="Notification Order",
    body="hey you, you have some order",
):
    if registration_token == "":
        return
    message = messaging.Message(
        data=data,
        token=registration_token,
        # notification body
        notification=messaging.Notification(title=title, body=body),
        # android notification
        android=messaging.AndroidConfig(
            ttl=datetime.timedelta(seconds=3600),
            notification=messaging.AndroidNotification(
                color="#f45342", title=title, body=body
            ),
        ),
        # apns
        apns=messaging.APNSConfig(
            payload=messaging.APNSPayload(
                aps=messaging.Aps(badge=42),
            ),
        ),
    )

    response = messaging.send(message, app=firebase)

    return response


def send_notif_multiple(
    registration_tokens=[],
    data={},
    title="Notification Order",
    body="hey you, you have some order ",
):
    if len(registration_tokens) == 0:
        return

    message = messaging.MulticastMessage(
        # for id user divice
        tokens=registration_tokens,
        # for data payload
        data=data,
        # notification body
        notification=messaging.Notification(title=title, body=body),
        # android notification
        android=messaging.AndroidConfig(
            ttl=datetime.timedelta(seconds=3600),
            notification=messaging.AndroidNotification(
                title=title, body=body, color="#f45342"
            ),
        ),
        # apns
        apns=messaging.APNSConfig(
            payload=messaging.APNSPayload(
                aps=messaging.Aps(badge=42),
            ),
        ),
    )
    response = messaging.send_multicast(message, app=firebase)
    # See the BatchResponse reference documentation
    # for the contents of response.
    return "{0} messages were sent successfully".format(response.success_count)


registerToken = ["e6fbXG_-83l0y5_9ou66Z4:APA91bF91P4A_DtD-ARJP9K71q0VV4kTfS6sCEovI0IOtvmb4i7p9RRXBnAqA6jt6cIXdyvek4-4xdhOGSDwFfGh6NR5asGpRyT4wh7mjPdD0LYcPXDxNDbLovqr2xIzooShI9DXIJQE"]

