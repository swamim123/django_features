from django.contrib import admin
# from .models import Book, SuperAdminUser, SuperAdminUserActivity
from book.models import Employee, Book


# Register your models here.
# class SuperAdminUserActivityAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#     search_fields = ('id', 'name', 'mobile')
#
# for model_name, model in app.models.items():
#     if model_name in ['SuperAdminUserActivity']:
#         continue
#     admin.site.register(model)
#


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'emp_id', 'name', 'mobile', 'email', 'birth_date', 'image')
    search_fields = ('id', 'name', 'mobile')


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Book)

# admin.site.register(SuperAdminUser)
# admin.site.register(SuperAdminUserActivity)
