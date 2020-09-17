from django.contrib import admin
from blog.models import Post, Category, Profile,Comment

#class PostAdmin(admin.ModelAdmin):
#    prepopulated_fields = {'slug': ('title',)}

#admin.site.register(Post,PostAdmin)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Comment)
