# -*- coding: utf-8 -*-
# author: itimor

from django.db import models
from storage import ImageStorage, BackgroundStorage
from django.conf import settings


class Photo(models.Model):
    '''
    照片的数据模型
    '''
    img_upload = models.ImageField(u'图片上传路径', upload_to='img/%Y/%m/%d', storage=ImageStorage())
    img_title = models.CharField(max_length=100, unique=True, verbose_name=u'图片标题')
    img_context = models.TextField(max_length=100, null=True, blank=True, verbose_name=u'图片介绍')
    img_tags = models.ManyToManyField('Tag', blank=True)
    img_group = models.ForeignKey('PhotoGroup', blank=True)
    like_count = models.IntegerField(default=0, verbose_name=u'图片喜欢次数')
    img_create_time = models.DateTimeField(u'图片发布时间', auto_now_add=True)
    img_update_time = models.DateTimeField(u'图片更新时间', auto_now=True)

    def image_view(self):
        return u'<img src="%s" height="200px"/>' % (settings.MEDIA_URL + str(self.img_upload))

    image_view.short_description = 'Image'
    image_view.allow_tags = True


class Tag(models.Model):
    """
    标签的数据模型
    """
    name = models.CharField(max_length=20, null=True, blank=True, )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['id']


class PhotoGroup(models.Model):
    """
    标签的数据模型
    """
    name = models.CharField(max_length=20, verbose_name=u'相册名')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['id']


class IndexBackground(models.Model):
    """
    相册背景图片的数据模型
    """
    name = models.CharField(max_length=20, verbose_name=u'背景名')
    img_upload = models.ImageField(u'图片上传路径', upload_to='background', storage=BackgroundStorage())

    def image_view(self):
        return u'<img src="%s"/>' % (settings.MEDIA_URL + str(self.img_upload))

    image_view.short_description = 'Image'
    image_view.allow_tags = True