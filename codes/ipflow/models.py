from django.db import models
from knox.auth import get_user_model


class FlowLog(models.Model):
    account_id = models.CharField(max_length=255, null=True, blank=True)
    interface_id = models.CharField(max_length=255, null=True, blank=True)
    srcaddr = models.CharField(max_length=255, null=True, blank=True)
    dstaddr = models.CharField(max_length=255, null=True, blank=True)
    srcport = models.CharField(max_length=255, null=True, blank=True)
    dstport = models.CharField(max_length=255, null=True, blank=True)
    protocol = models.CharField(max_length=255, null=True, blank=True)
    # keep going...
    #user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
    #                         null=True, blank=True,
    #                         default=None)

    # we need to add the attributes for a flow log here.
    # https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html
