from django.contrib import admin
from .models import BlogPost, Task, CustomUser, Document, Comment



class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "thumbnail", "content", "published", )
    list_editable = ("published", )

class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title", "responsable", "description", "date_de_debut",
        "date_de_fin", "priorite", "statut",
        "avancement", "commentaires",
    )
    list_editable = ("priorite", )

class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "title", "book_file" , "level", "domain", "description",
    )
    list_editable = (
        "level", "domain",
    )

class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "username", "password", "is_staff", "is_admin",
        "is_agent", "is_student", "is_allowed", "level", "domain",
    )
    list_editable = (
        "is_staff", "is_admin",
        "is_agent", "is_student", "is_allowed", "level", "domain",
    )

class CommentAdmin(admin.ModelAdmin):
    list_display = ("content","blog","user", "anonymous", "created_at",)



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Document, DocumentAdmin)
