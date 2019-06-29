from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import User,Building, College, Department, Role, Section, Homework, Field, Course, Document, Message, Solution, Video


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('content_type')


admin.site.register(User)
admin.site.register(College)
admin.site.register(Department)
admin.site.register(Role)
admin.site.register(Section)
admin.site.register(Homework)
admin.site.register(Field)
admin.site.register(Course)
admin.site.register(Document)
admin.site.register(Message)
admin.site.register(Solution)
admin.site.register(Video)
admin.site.register(Building)

