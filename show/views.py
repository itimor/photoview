# -*- coding: utf-8 -*-
# author: itimor

from django.views.generic.list import ListView
from models import Photo, PhotoGroup
from django.shortcuts import render
from django.http import HttpResponse
import json

from likes.models import Likes, LikesDetail
from django.contrib.contenttypes.models import ContentType


class PhotoListView(ListView):
    template_name = 'photo_list.html'
    context_object_name = 'photo_list'

    def get_queryset(self):
        groups = PhotoGroup.objects.all()
        photodata = {}
        for group in groups:
            article_list = Photo.objects.filter(img_group__name=group)
            photodata[group] = article_list
        return photodata


def likes_change(request):
    u"""处理改变点赞状态
        Method: GET
        params: 
            type  : object type
            id    : object id
            direct: -1 or 1 (add like or remove like)
        return: json
    """
    # 创建json对象需要的数据
    data = {}
    data['status'] = 200
    data['message'] = u'ok'
    data['nums'] = 0

    # 获取数据和对应的对象
    obj_type = request.GET.get('type')
    obj_id = request.GET.get('id')
    user = request.user

    direct = 1 if request.GET.get('direct') == '1' else -1
    c = ContentType.objects.get(model=obj_type)

    # 获取Likes对象
    try:
        l = Likes.objects.get(content_type=c, object_id=obj_id)
    except Exception, e:
        # 没有获取到对象，则新增一个Likes对象
        l = Likes(content_type=c, object_id=obj_id)
    data['nums'] = l.likes_num

    # 获取Likes明细对象
    try:
        detail = LikesDetail.objects.get(likes=l, user=user)
    except Exception, e:
        detail = LikesDetail(likes=l, user=user, is_like=False)
    liked = 1 if detail.is_like else -1

    # 判断是否赞过，或者取消赞
    if liked == direct:
        data['status'] = 403
        data['message'] = u'Invalid operation'
    else:
        # 更新记录
        l.likes_num += direct
        if l.likes_num < 0:
            l.likes_num = 0
        l.save()
        data['nums'] = l.likes_num

        # 修改明细
        detail.is_like = direct == 1
        detail.save()

    # 返回结果
    return HttpResponse(json.dumps(data), content_type="application/json")