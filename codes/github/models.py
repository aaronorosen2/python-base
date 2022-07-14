from django.db import models
from knox.auth import get_user_model


class Repo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=512, blank=True, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, blank=True,
                             default=None)
    class Meta:
        unique_together = ('user', 'name')



class RepoMember(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, blank=True,
                             default=None)
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE,
                             null=True, blank=True,
                             default=None)

class UserSshPubKey(models.Models):
    pub_key = models.TextField(null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, blank=True,
                             default=None)

