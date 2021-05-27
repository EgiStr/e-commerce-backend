from firebase_admin import messaging,initialize_app,credentials
import os
import datetime 

# create firebase project in console.firebase and generated key for admin
cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), 'e-commerce-cd481-firebase-adminsdk-y3v6v-011fab9e1d.json'))

firebase = initialize_app(cred,name="e-commerce")


def send_notif_device(registration_token="",data={},title="Notification Order",body="hey you, you have some order"):
    if registration_token == "":
        return 
    message = messaging.Message(
        data=data,
        token=registration_token,
    
        # notification body
        notification=messaging.Notification(
            title=title,
            body=body
        ),

        # android notification
        android=messaging.AndroidConfig(
            ttl=datetime.timedelta(seconds=3600),
            notification=messaging.AndroidNotification(
                color='#f45342',
                title=title,
                body=body
            )
        ),
        
        # apns
        apns=messaging.APNSConfig(
        payload=messaging.APNSPayload(
            aps=messaging.Aps(badge=42),
        ),
    ),
    )

    response = messaging.send(message,app=firebase)
    
    return response

def send_notif_multiple(registration_tokens=[],data={},title="Notification Order",body="hey you, you have some order "):
    if len(registration_tokens) == 0:
        return 
    
    message = messaging.MulticastMessage(
        # for id user divice
        tokens=registration_tokens,
        # for data payload
        data=data,

        # notification body
        notification=messaging.Notification(
            title=title,
            body=body
        ),

        # android notification
        android=messaging.AndroidConfig(
            ttl=datetime.timedelta(seconds=3600),
            notification=messaging.AndroidNotification(
                title=title,
                body=body,
                color='#f45342'
            )
        ),

        # apns
        apns=messaging.APNSConfig(
        payload=messaging.APNSPayload(
            aps=messaging.Aps(badge=42),
        ),
    ),
    )
    response = messaging.send_multicast(message,app=firebase)
    # See the BatchResponse reference documentation
    # for the contents of response.
    return '{0} messages were sent successfully'.format(response.success_count)

registerToken = "eIYZeTUS0YncJVtrh0TF4C:APA91bHIQgQ6TKxHrhBoC3MXWSxMG3XjTTgNedrw5Iyhu13GE9uX_mf8eyb5KoX3XQvAChcZWMxj4s99otq6jxjB1OJjZu4vQ1_4-FLDhgdMm3aZQVPfHSWhKRuPRX8INpnCG7EphLZ-"