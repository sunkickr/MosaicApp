from io import BytesIO
from django.core.files import File
from PIL import Image
from mosaic_api.mosaicbuilder.mosaicalgo import create_mosaic
from mosaic_api.mosaicbuilder.mosaicalgo2 import create_new_mosaic

def invert(image):
    """Invert images colors."""
    im = Image.open(image)
    out =im.convert("RGB",(
        2.3706743, -0.9000405, -0.4706338, 0,
        -0.5138850,  1.4253036,  0.0885814, 0,
        0.0052982, -0.0146949,  1.0093968, 0))
    thumb_io = BytesIO()
    out.save(thumb_io, 'JPEG', quality=85)
    return File(thumb_io, name=image.name)

def mosaic(image):
    """Creates a mosaic in the model."""
    im = Image.open(image)
    ratio = round(image.width/image.height, 1)
    size = (int(1800*ratio), int(1800))
    mosaic = create_mosaic(im, 25, 50, 'mosaic_api/mosaicbuilder/crop_source')
    mosaic = mosaic.resize(size)
    thumb_io = BytesIO()
    mosaic.save(thumb_io, 'JPEG', quality=85)
    return File(thumb_io, name=image.name)

def newmosaic(image):
    """Creates a mosaic in the model."""
    im = Image.open(image)
    ratio = round(image.width/image.height, 1)
    size = (int(1800*ratio), int(1800))
    mosaic = create_new_mosaic(im, 25, 50, 'build/media/new/sourceimages')
    mosaic = mosaic.resize(size)
    thumb_io = BytesIO()
    mosaic.save(thumb_io, 'JPEG', quality=85)
    return File(thumb_io, name=image.name)

def thumb(image, pix):
    """Makes viewable mosaic for webpage."""
    try:
        im = Image.open(image)
    except:
        print('error')

    if im.width > im.height:
        im = im.crop(((im.width-im.height)/2 , 0 , im.width-(im.width-im.height)/2 , im.height))
    elif im.width < im.height:
        im = im.crop((0, (im.height-im.width)/2, im.width, im.height - (im.height-im.width)/2))
    im = im.resize((pix,pix))
    print(im.size)

    thumb_io = BytesIO()
    im.save(thumb_io, 'JPEG', quality=85)
    return File(thumb_io, name=image.name)
