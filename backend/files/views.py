# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import mimetypes
import time

from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from os.path import basename

import hashlib
import json
import zipfile

from backend import settings
from files.models import Files, Archive
from urllib.parse import quote


class MyView(View):
    def get(self, request, *args, **kwargs):
        cookie = "Hello Man!"
        http_response = HttpResponse("Hello world")
        http_response.set_cookie('cookie', cookie)
        return http_response

    def post(self, request):

        device_name = request.META['SESSION_MANAGER']
        hash_obj = hashlib.md5(device_name.encode('utf8'))
        hash = hash_obj.hexdigest()

        loaded_files = []
        for file in dict(request.FILES).values():
            new_file = Files.objects.create(
                hash=hash,
                name=file[0].name
            )
            new_file.file = file[0]
            new_file.save()
            loaded_files.append({
                'id': new_file.id,
                'name': new_file.name,
                'size': new_file.file.size
            })

        return HttpResponse(json.dumps(loaded_files))


class MakeArchiveView(View):
    def post(self, request):

        device_name = request.META['SESSION_MANAGER']
        hash_obj = hashlib.md5(device_name.encode('utf8'))
        hash = hash_obj.hexdigest()

        archive_name = request.POST['fileName']
        archive_type = request.POST['typeName']
        squeeze_flag = request.POST['squeezeFlag'] == 'true'

        ids = json.loads(dict(request.POST)['ids'][0])
        files = Files.objects.filter(id__in=ids)

        path = './archive.zip'

        if squeeze_flag:
            print('Сжатие')
            jungle_zip = zipfile.ZipFile('./archive.zip', 'w', zipfile.ZIP_DEFLATED)
        else:
            print('Сжатие нет')
            jungle_zip = zipfile.ZipFile('./archive.zip', 'w')

        for file in files:
            path = str(file.file.file)
            print(path)
            jungle_zip.write(path, basename(file.name))
        jungle_zip.close()

        file = open('./archive.zip', 'rb')

        name_file = '{file_name}{file_type_name}'.format(file_name=archive_name, file_type_name=archive_type)
        new_file = Archive.objects.create(
            hash=hash,
            name=name_file
        )
        new_file.file.save('archive.zip', File(file))
        new_file.save()

        return HttpResponse(json.dumps({
            "id": new_file.id,
            "size": new_file.file.size,
            "name": new_file.name
        }))


class CheckTryCount(View):
    try_count = 35

    def get(self, request, *args, **kwargs):
        print("Chekc")
        device_name = request.META['SESSION_MANAGER']
        hash_obj = hashlib.md5(device_name.encode('utf8'))
        hash = hash_obj.hexdigest()

        done_try = Archive.objects.filter(hash=hash).count()

        return HttpResponse(json.dumps({
            "try_count": self.try_count,
            "done_try": done_try
        }))


class DownloadFileView(View):
    def get(self, request, *args, **kwargs):

        id = request.GET.get('id')
        document_file = Files.objects.get(id=id)

        file = document_file.file
        name = document_file.name
        content_type = mimetypes.guess_type(name)[0]
        response = HttpResponse(file.read(), content_type=content_type)
        # 'attachment; filename="filename"' - Сразу скачивает файл без открытия
        # 'filename="filename"' - Открывает файл в отдельной вкладке
        response['Content-Disposition'] = "filename*=UTF-8\'\'{}".format(quote(name, encoding='utf-8'))
        return response


class DownloadArchiveView(View):
    def get(self, request, *args, **kwargs):

        id = request.GET.get('id')
        document_file = Archive.objects.get(id=id)

        file = document_file.file
        name = document_file.name
        content_type = mimetypes.guess_type(name)[0]
        response = HttpResponse(file.read(), content_type=content_type)
        # 'attachment; filename="filename"' - Сразу скачивает файл без открытия
        # 'filename="filename"' - Открывает файл в отдельной вкладке
        response['Content-Disposition'] = "filename*=UTF-8\'\'{}".format(quote(name, encoding='utf-8'))
        return response

