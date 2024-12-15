from django.db import models

class Posts(models.Model):
    title = models.CharField(max_length =100)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now = True)
    
    def __str__(self) -> str:
        return self.title