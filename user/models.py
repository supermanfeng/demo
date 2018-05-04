'''
    User

        UserRoleRelation

    Role

        RolePermRelation

    Permission
'''

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

    def has_perm(self, perm_name):
        return True


class Role(models.Model):
    '''角色表'''
    name = models.CharField(max_length=32, unique=True)


class UserRoleRelation(models.Model):
    '''用户和角色的对应关系'''
    user_id = models.IntegerField()
    role_id = models.IntegerField()

    @classmethod
    def add_role_for_user(cls, user_id, role_name):
        role = Role.objects.get(name=role_name).only('id')
        cls.objects.get_or_create(user_id=user_id, role_id=role.id)

    @classmethod
    def del_role_from_user(cls, user_id, role_name):
        role = Role.objects.get(name=role_name).only('id')
        cls.objects.get(user_id=user_id, role_id=role.id).delete()


class Permission(models.Model):
    '''权限表'''
    # create_post
    # modify_post
    # comment
    # delete_post
    name = models.CharField(max_length=32, unique=True)


class RolePermRelation(models.Model):
    '''角色和权限的关系表'''
    role_id = models.IntegerField()
    perm_id = models.IntegerField()

    @classmethod
    def add_perm_for_role(cls, role_id, perm_name):
        perm = Permission.objects.get(name=perm_name)
        cls.objects.get_or_create(role_id=role_id, perm_id=perm.id)

    @classmethod
    def del_perm_from_role(cls, role_id, perm_name):
        perm = Permission.objects.get(name=perm_name)
        cls.objects.get(role_id=role_id, perm_id=perm.id).delete()
