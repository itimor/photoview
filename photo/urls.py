# -*- coding: utf-8 -*-
# author: itimor

from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from show.views import PhotoListView

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^$', PhotoListView.as_view()),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
