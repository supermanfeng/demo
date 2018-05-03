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
            # self._auth = User.objects.using(chose_db(self.uid)).get(id=self.uid)
            self._auth = User.objects.get(id=self.uid)
        return self._auth

    def comments(self):
        return Comment.objects.filter(post_id=self.id).order_by('-create')

    def tags(self):
        '''当前帖子所具有的 Tag'''
        pass

    def update_tags(self, tag_names):
        '''更新当前帖子的标签'''
        pass


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
        pass


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
