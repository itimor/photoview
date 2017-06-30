# -*- coding: utf-8 -*-
# author: itimor

from django.contrib import admin
from models import Photo, Tag, PhotoGroup, IndexBackground
import os
from django.dispatch import receiver
from django.db import models


# 图片自动删除
@receiver(models.signals.post_delete, sender=Photo)
@receiver(models.signals.post_delete, sender=IndexBackground)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Photo` object is deleted.
    """
    if instance.img_upload:
        if os.path.isfile(instance.img_upload.path):
            os.remove(instance.img_upload.path)

# 图片自动更新
@receiver(models.signals.pre_save, sender=Photo)
@receiver(models.signals.pre_save, sender=IndexBackground)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Photo` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).img_upload
    except sender.DoesNotExist:
        return False

    new_file = instance.img_upload
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class PhotoAdmin(admin.ModelAdmin):
    search_fields = ('img_title', 'img_time')
    list_filter = ('img_create_time', 'img_update_time', 'like_count', 'img_group',)
    list_display = (
    'img_title', 'img_context', 'img_upload', 'img_group', 'like_count', 'img_create_time', 'img_update_time')
    fields = ('img_title', 'img_context', 'img_tags', 'img_upload', 'img_group', 'image_view')
    readonly_fields = ('image_view', 'like_count', 'img_update_time')


class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('name',)
    list_display = ('name',)
    fields = ('name',)


class PhotoGroupAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('name',)
    list_display = ('name',)
    fields = ('name',)


class IndexBackgroundAdmin(admin.ModelAdmin):
    list_display = ('name', 'img_upload',)
    fields = ('name', 'img_upload', 'image_view')
    readonly_fields = ('image_view',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoGroup, PhotoGroupAdmin)
admin.site.register(IndexBackground, IndexBackgroundAdmin)