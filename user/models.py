from django.db import models


class User(models.Model):
    SEX = (
        ('M', '男'),
        ('F', '女'),
        ('U', '保密'),
    )
    nickname = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=128)
    age = models.IntegerField()
    sex = models.CharField(choices=SEX, max_length=8)
    icon = models.ImageField()
    perm_id = models.IntegerField()

    @property
    def perm(self):
        if not hasattr(self, '_perm'):
            self._perm = Permission.objects.get(id=self.perm_id)
        return self._perm


class Permission(models.Model):
    name = models.CharField(max_length=32, unique=True)
    level = models.IntegerField()
