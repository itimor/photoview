# -*- coding: utf-8 -*-
# author: itimor

from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from show.views import PhotoListView

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^$', PhotoListView.as_view()),
                  url(r"^likes/", include("pinax.likes.urls", namespace="pinax_likes")),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
