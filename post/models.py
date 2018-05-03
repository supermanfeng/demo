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
