from django.contrib import admin

from todo.tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "is_completed", "get_tags_display", "created_at", "updated_at")
    list_filter = ("is_completed", "created_at", "updated_at")

    readonly_fields = ("user", "created_at", "updated_at")
    search_fields = ("title", "user__username", "user__email", "user__first_name", "user__last_name")

    def get_fields(self, request, obj=None):
        fields = ("title", "tags")
        if obj is not None:
            fields += ("is_completed", "user", "created_at", "updated_at")
        return fields

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
