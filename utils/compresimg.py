import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


def CompressPost(f):
    try:
        image = Image.open(f)
        myHeight, myWidht = image.size
        image = image.convert("RGB")
        image.thumbnail((myHeight, myWidht), Image.ANTIALIAS)
        thumbnail = BytesIO()
        # Default quality is quality=75
        image.save(thumbnail, format="JPEG", quality=25, optimize=True)

        thumbnail.seek(0)

        newImage = InMemoryUploadedFile(
            thumbnail, None, f.name, "image/jpeg", sys.getsizeof(thumbnail), None
        )
        return newImage

    except Exception as e:
        return e


def Compressprofil(f):
    try:
        image = Image.open(f)

        image = image.convert("RGB")
        image.thumbnail((400, 400), Image.ANTIALIAS)
        thumbnail = BytesIO()
        # Default quality is quality=75
        image.save(thumbnail, format="JPEG", quality=15, optimize=True)

        thumbnail.seek(0)

        newImage = InMemoryUploadedFile(
            thumbnail, None, f.name, "image/jpeg", sys.getsizeof(thumbnail), None
        )
        return newImage
    except Exception as e:
        return 
