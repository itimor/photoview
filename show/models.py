# -*- coding: utf-8 -*-
# author: itimor

from django.db import models
from storage import ImageStorage, BackgroundStorage
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Likes(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        ct_field="content_type",
        fk_field="object_id"
    )

    # likes number
    likes_num = models.PositiveIntegerField('点赞数', default=0)

    def __unicode__(self):
        return u'%s:%s(%s)' % (self.content_type, self.object_id, self.likes_num)


class Photo(models.Model):
    '''
    照片的数据模型
    '''
    img_upload = models.ImageField(u'图片上传路径', upload_to='img/%Y/%m/%d', storage=ImageStorage())
    img_title = models.CharField(max_length=100, unique=True, verbose_name=u'图片标题')
    img_context = models.TextField(max_length=100, null=True, blank=True, verbose_name=u'图片介绍')
    img_tags = models.ManyToManyField('Tag', blank=True)
    img_group = models.ForeignKey('PhotoGroup', blank=True)
    like_count = models.ForeignKey('Likes')
    is_like = models.BooleanField(default=False)
    img_create_time = models.DateTimeField(u'图片发布时间', auto_now_add=True)
    img_update_time = models.DateTimeField(u'图片更新时间', auto_now=True)

    def image_view(self):
        return u'<img src="%s" height="200px"/>' % (settings.MEDIA_URL + str(self.img_upload))

    image_view.short_description = '图片展示'
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
        return u'<img src="%s" height="500px"/>' % (settings.MEDIA_URL + str(self.img_upload))

    image_view.short_description = '图片展示'
    image_view.allow_tags = True