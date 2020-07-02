from django.contrib import admin

from . import models

admin.site.register(models.Role)
admin.site.register(models.UserInfo)
admin.site.register(models.UserGroup)
admin.site.register(models.Data)
admin.site.register(models.Book)
admin.site.register(models.Publish)
admin.site.register(models.Author)
admin.site.register(models.AuthorDetail)
admin.site.register(models.NewBook)
