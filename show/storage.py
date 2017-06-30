# -*- coding: utf-8 -*-
# author: itimor

from django.core.files.storage import FileSystemStorage
from django.conf import settings


class ImageStorage(FileSystemStorage):
    def _save(self, name=settings.MEDIA_ROOT, content=settings.MEDIA_URL):
        import os, time, random
        # 文件扩展名
        fileext = os.path.splitext(name)[1]
        # 文件目录
        d = os.path.dirname(name)
        # 定义文件名，年月日时分秒随机数
        fntime = time.strftime('%Y%m%d%H%M%S') + '_%d' % random.randint(0, 100)
        # 重写合成文件名
        name = os.path.join(d, fntime + fileext)
        # 调用父类方法
        return super(ImageStorage, self)._save(name, content)
