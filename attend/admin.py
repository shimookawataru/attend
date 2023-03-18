from django.contrib import admin
from .models import SubmitAttendance, OverWorkTime, SubmitForget
from django.db.models import Q

#フィルター
class StaffFieldListFilter(admin.RelatedFieldListFilter):
    def field_choices(self, field, request, model_admin):
        staff_id = request.GET.get('staff__staff_id')
        limit_choices_to = Q(staff__exact = staff_id) if staff_id else None
        return field.get_choices(include_blank=False, limit_choices_to=limit_choices_to)

#勤怠管理リスト
class SubmitAttendanceAdmin(admin.ModelAdmin,):
    list_display = ("staff", "in_out", "date", "time")
    list_filter = (
        'in_out',
        ('staff', StaffFieldListFilter),
        "date"
    )

#働きすぎリスト
class OverWorkTimeAdmin(admin.ModelAdmin,):
    list_display = ("staff", "date_time_in", "date_time_out", "worktime")
    list_filter = (
        "worktime",
        'date_time_in',
        'date_time_out',
        ('staff', StaffFieldListFilter)
    )

#打刻忘れリスト
class SubmitForgetAdmin(admin.ModelAdmin,):
    list_display = ("staff", "in_out", "date_time_forget")
    list_filter = (
        "in_out",
        'date_time_forget',
        ('staff', StaffFieldListFilter)
    )

# Register your models here.
admin.site.register(SubmitAttendance, SubmitAttendanceAdmin)
admin.site.register(OverWorkTime, OverWorkTimeAdmin)
admin.site.register(SubmitForget, SubmitForgetAdmin)