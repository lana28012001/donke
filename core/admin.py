from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin

from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from .models import *
from django.contrib.admin import DateFieldListFilter

# Register your models here.

class UserAccountAdmin(UserAdmin):
    list_display = ['id','username','email','phonenumber','address','dateofbirth','gender','is_active', 'is_lock']
    search_fields = ('id', 'username','email','phonenumber','address','dateofbirth','gender')
    model = UserAccount
admin.site.register(UserAccount, UserAccountAdmin)

class TypeStatusAdmin(admin.ModelAdmin):
    list_display = ['id','name','description',]
    search_fields = ('id','name','description')
admin.site.register(TypeStatus,TypeStatusAdmin)

class TypeCustomerAdmin(admin.ModelAdmin):
    list_display = ['id','name','description',]
    search_fields = ('id','name','description')
admin.site.register(TypeCustommer,TypeCustomerAdmin)

class DayAdmin(admin.ModelAdmin):
    list_display = ['id','day',]
    search_fields = ('id','day')
admin.site.register(Day,DayAdmin)

class BuoiAdmin(admin.ModelAdmin):
    list_display = ['id','buoi',]
    search_fields = ('id','buoi')
admin.site.register(Buoi,BuoiAdmin)


class FileProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'images_product',"file_product_id"]
    search_fields = ('id', 'images_product')
admin.site.register(FileProduct, FileProductAdmin)

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('id','product','price','function', 'dosage','keyword','estimate','note')
        import_order = ('id','product','price','function', 'dosage','keyword','estimate','note')
        export_order = ('id','product','price','function', 'dosage','keyword','estimate','note')
        clean_model_instances = True
class ProductAdmin(ImportExportModelAdmin):
    list_display = ['id','product','price','function', 'dosage','keyword','estimate','note']
    search_fields = ('id','product','price','function', 'dosage','keyword','estimate','note')
    resource_class = ProductResource
admin.site.register(Product, ProductAdmin)


class ServiceResource(resources.ModelResource):
    class Meta:
        model = Service
        fields = ('id', 'service', 'function', 'note')
        import_order = ('id', 'service', 'function', 'note')
        export_order = ('id', 'service', 'function', 'note')
        clean_model_instances = True
class ServiceAdmin(ImportExportModelAdmin):
    list_display = ['id', 'service', 'function', 'note']
    search_fields = ('id', 'service')
    resource_class = ServiceResource

admin.site.register(Service, ServiceAdmin)


class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer
        fields = ('id', 'user','full_name', 'numberphone', 'age', 'profession', 'address', 'status', 'type','note')
        import_order = ('id', 'user','full_name', 'numberphone', 'age', 'profession', 'address', 'status', 'type','note')
        export_order = ('id', 'user','full_name', 'numberphone', 'age', 'profession', 'address', 'status', 'type','note')
        clean_model_instances = True
class CustomerAdmin(ImportExportModelAdmin):
    list_display = ['id', 'user','full_name', 'numberphone', 'age', 'profession', 'address', 'status', 'type','note']
    search_fields = ('id', 'full_name', 'numberphone')
    resource_class = CustomerResource

admin.site.register(Customer, CustomerAdmin)


class FileOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'file_before', 'file_after','img_order','img_order_id']
    # search_fields = ('id', 'file_before', 'file_after','img_order')
    
admin.site.register(FileOrder, FileOrderAdmin)


class DetailOrderProductAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','day','buoi', 'order','order_id']
    # search_fields = ('id','user','product','day','buoi', 'order')
admin.site.register(DetailOrderProduct, DetailOrderProductAdmin)


class DetailOrderServiceAdmin(admin.ModelAdmin):
    list_display = ['id','user','service','time','note', 'order','order_id']
    # search_fields = ('id','user','service','time','note', 'order')
admin.site.register(DetailOrderService, DetailOrderServiceAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'customer', 'day_re_examination', 'use_to', 'detail_caleder_examination','note_order','pathological','created_at','updated_at']
    # search_fields = ('id', 'customer',)
    
admin.site.register(Order, OrderAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id','user','order','customer','content','is_view','is_sent','created_at','updated_at']
    # search_fields = ('id','user','order','customer','content','is_view','is_sent',)
admin.site.register(Notifications, NotificationAdmin)