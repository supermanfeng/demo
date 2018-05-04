'''
    User
       \
        UserRoleRelation
       /
    Role
       \
        RolePermRelation
       /
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

    def roles(self):
        '''用户所有的角色'''
        relations = UserRoleRelation.objects.filter(user_id=self.id).only('role_id')
        role_id_list = [r.role_id for r in relations]
        return Role.objects.filter(id__in=role_id_list)

    def has_perm(self, perm_name):
        '''检查用户是否具有该权限'''
        for role in self.roles():
            for perm in role.perms():
                if perm.name == perm_name:
                    return True
        return False


class Role(models.Model):
    '''角色表'''
    name = models.CharField(max_length=32, unique=True)

    def perms(self):
        '''角色所有的权限'''
        relations = RolePermRelation.objects.filter(role_id=self.id).only('perm_id')
        perm_id_list = [r.perm_id for r in relations]
        return Permission.objects.filter(id__in=perm_id_list)


class UserRoleRelation(models.Model):
    '''用户和角色的对应关系'''
    user_id = models.IntegerField()
    role_id = models.IntegerField()

    @classmethod
    def add_role_for_user(cls, user_id, role_name):
        role = Role.objects.get(name=role_name)
        cls.objects.get_or_create(user_id=user_id, role_id=role.id)

    @classmethod
    def del_role_from_user(cls, user_id, role_name):
        role = Role.objects.get(name=role_name)
        cls.objects.get(user_id=user_id, role_id=role.id).delete()


class Permission(models.Model):
    '''权限表'''
    # 权限名：
    #   create_post
    #   modify_post
    #   comment
    #   delete_post
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
