from django.db import models

from user.models import User


class Post(models.Model):
    uid = models.IntegerField()
    title = models.CharField(max_length=64)
    create = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    @property
    def auth(self):
        if not hasattr(self, '_auth'):
            # 数据库有数据分片时的操作
            # db_name = chose_db(self.uid)  # 根据数据分片规则选择 uid 所在的数据库
            # self._auth = User.objects.using(db_name).get(id=self.uid)

            self._auth = User.objects.get(id=self.uid)
        return self._auth

    def comments(self):
        return Comment.objects.filter(post_id=self.id).order_by('-create')

    def tags(self):
        '''当前帖子所具有的 Tag'''
        relations = PostTagRelation.objects.filter(post_id=self.id).only('tag_id')
        tag_id_list = [r.tag_id for r in relations]
        return Tag.objects.filter(id__in=tag_id_list)

    def update_tags(self, tag_names):
        '''更新当前帖子的标签'''
        tag_names = set(tag_names)
        current_tags = self.tags()
        current_tag_names = {t.name for t in current_tags}

        # 创建新的关系
        new_relation_tag_names = tag_names - current_tag_names
        PostTagRelation.add_post_tags(self.id, new_relation_tag_names)

        # 删除旧的关系
        old_relation_tag_names = current_tag_names - tag_names
        PostTagRelation.del_post_tags(self.id, old_relation_tag_names)


class Comment(models.Model):
    uid = models.IntegerField()
    post_id = models.IntegerField()
    create = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    @property
    def auth(self):
        if not hasattr(self, '_auth'):
            self._auth = User.objects.get(id=self.uid)
        return self._auth

    @property
    def post(self):
        if not hasattr(self, '_post'):
            self._post = Post.objects.get(id=self.post_id)
        return self._post


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def posts(self):
        relations = PostTagRelation.objects.filter(tag_id=self.id).only('post_id')
        post_id_list = [r.post_id for r in relations]
        return Post.objects.filter(id__in=post_id_list)

    @classmethod
    def ensure_tags(cls, tag_names):
        '''确保 tag 已存在'''
        # 先取出已存在的 tags
        old_tags = cls.objects.filter(name__in=tag_names)
        old_names = {t.name for t in old_tags}  # 已存在的 Tag.name

        # 筛选并创建新的 tags
        new_names = set(tag_names) - old_names
        new_tags = [Tag(name=n) for n in new_names]
        cls.objects.bulk_create(new_tags)

        # 返回全部的 tags
        return cls.objects.filter(name__in=tag_names)


class PostTagRelation(models.Model):
    '''
    帖子和标签的关系表

    post              tag
    ------------------------
    abc               python
    abc               django
    abc               linux
    HelloWorld        python
    HelloWorld        linux
    HelloWorld        develop
    '''
    post_id = models.IntegerField()
    tag_id = models.IntegerField()

    @classmethod
    def add_post_tags(cls, post_id, tag_names):
        '''为 post_id 添加新的 tag 的对应关系'''
        tags = Tag.ensure_tags(tag_names)
        new_relations = [PostTagRelation(post_id=post_id, tag_id=t.id) for t in tags]
        cls.objects.bulk_create(new_relations)

    @classmethod
    def del_post_tags(cls, post_id, tag_names):
        '''删除与 post_id 有关联的 tag 的关系'''
        tags = Tag.objects.filter(name__in=tag_names).only('id')
        tag_id_list = [t.id for t in tags]
        cls.objects.filter(post_id=post_id, tag_id__in=tag_id_list).delete()
