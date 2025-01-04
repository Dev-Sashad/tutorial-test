from django.contrib import admin

from .model.post_model import Posts

# Register your models here.

@admin .register(Posts)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "date_created"]
    list_filter = ["date_created"]

# Register your models here.
