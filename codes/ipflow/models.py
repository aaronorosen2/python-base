from django.db import models
from knox.auth import get_user_model


class FlowLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    #user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
    #                         null=True, blank=True,
    #                         default=None)

    # we need to add the attributes for a flow log here.
    # https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html
