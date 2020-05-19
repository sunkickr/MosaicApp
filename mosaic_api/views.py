from django.shortcuts import render
from .models import Mosaic, Image, NewMosaic
from .serializers import MosaicSerializer, ImageSerializer, NewMosaicSerializer
from rest_framework import generics, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from django.views.generic import View
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import logging
import urllib.request
import os


# Create your views here.

class MosaicListCreate(generics.ListCreateAPIView):
    queryset = Mosaic.objects.all()
    serializer_class = MosaicSerializer


class ImageViewSet(generics.ListCreateAPIView):
    queryset=Image.objects.all()
    serializer_class = ImageSerializer


class NewMosaicListCreate(generics.ListCreateAPIView):
    queryset = NewMosaic.objects.all()
    serializer_class = NewMosaicSerializer

@csrf_exempt
def check_url(request):
    try:
        url_status = urllib.request.urlopen(request.body.decode("utf-8") ).getcode()
    except:
        return HttpResponse(":( Url is Not Working")
    if (url_status == 200):
        return HttpResponse("Yey! URL is Working")
    return HttpResponse(":( Url is Not Working")

class FrontendAppView(View):
    """
    Serves the compiled frontend entry point (only works if you have run `yarn
    run build`).
    """
    def get(self, request):
            print (os.path.join(settings.REACT_APP_DIR, 'build', 'index.html'))
            try:
                with open(os.path.join(settings.REACT_APP_DIR, 'build', 'index.html')) as f:
                    return HttpResponse(f.read())
            except FileNotFoundError:
                logging.exception('Production build of app not found')
                return HttpResponse(
                    """
                    This URL is only used when you have built the production
                    version of the app. Visit http://localhost:3000/ instead, or
                    run `yarn run build` to test the production version.
                    """,
                    status=501,
                )