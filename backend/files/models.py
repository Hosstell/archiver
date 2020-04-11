from django.db import models
import time


def file_path(instance, filename):
    filename = str(time.time()) + '_' + filename
    return 'files/{}/files/{}'.format(instance.hash, filename)


class Files(models.Model):
    file = models.FileField(upload_to=file_path)
    name = models.CharField(max_length=200)
    hash = models.CharField(max_length=30)


def archive_path(instance, filename):
    filename = str(time.time()) + '_' + filename
    return 'files/{}/archives/{}'.format(instance.hash, filename)


class Archive(models.Model):
    file = models.FileField(upload_to=archive_path)
    name = models.CharField(max_length=200)
    hash = models.CharField(max_length=30)
