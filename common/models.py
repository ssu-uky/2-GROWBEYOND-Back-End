from django.db import models

class CommonModel(models.Model):
    
    # auto_now_add == 객체가 생성되는 시간을 기준
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True