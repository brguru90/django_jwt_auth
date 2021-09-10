from django.db import models
class tokenBlackList(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=255, blank=False,null=False)
    block_until_date = models.DateTimeField(blank=True, null=True)   # block token if token_created_date < block_until_date
    block_token = models.CharField(unique=True, max_length=30, null=True)
    block_token_expire = models.DateTimeField(blank=True, null=True) # may be needed in case cleanup expired token from blacklist

