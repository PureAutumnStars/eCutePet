from django.contrib import admin

from api.forum.models import PostTag, PostInfo, PostComment, PostFavor


# Register your models here.

@admin.register(PostTag)
class PostTagAdmin(admin.ModelAdmin):
    # 默认按照name排序
    ordering = ['name']

    # 自定义后台展示的信息
    list_display = ["name", "description", "create_time", "modify_time"]


@admin.register(PostInfo)
class PostInfoAdmin(admin.ModelAdmin):
    # 默认按照create_time排序
    ordering = ['create_time']

    # 自定义后台展示的信息
    list_display = ["title", "tag", "front_image", "author", "click_num", "favor_num", "comment_num", "create_time"]


@admin.register(PostFavor)
class PostFavorAdmin(admin.ModelAdmin):
    # 默认按照user排序
    ordering = ['user']

    # 自定义后台展示的信息
    list_display = ["user", "post", "create_time"]


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    # 默认按照post排序
    ordering = ['post']

    # 自定义后台展示的信息
    list_display = ["id", "post", "user", "create_time", "modify_time"]
