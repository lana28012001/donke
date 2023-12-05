from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# from django.contrib.auth.models import UserManager
# Create your models here.
class TimeStampedModelMixin(models.Model):
    """
    Abstract Mixin model to add timestamp
    """
    created_at = models.DateTimeField(u"Date created_at",auto_now_add=True)
    updated_at = models.DateTimeField(u"Date updated_at",auto_now=True, db_index=True)

    class Meta:
        abstract = True  

class UserAccount(AbstractUser):
    ''' Thông tin cá nhân '''
    gender_choices = [
        ['Nam', 'Nam'],
        ['Nam', 'Nam'],
        ['Khác/Không trả lời', 'Khác/Không trả lời']
    ]
   
    gender = models.CharField(max_length=255,choices=gender_choices,blank=True,null=True, verbose_name='Giới tính')
    address = models.CharField(max_length=255, default='',blank=True,null=True, verbose_name='Địa chỉ')
    phonenumber = models.CharField(max_length=15,blank=True,null=True, verbose_name='Số điện thoại')
    dateofbirth = models.CharField(max_length=10,default='',blank=True,null=True, verbose_name = 'Ngày sinh')
    email = models.CharField(max_length=255,blank=True,null=True,verbose_name='Email address')

    is_lock = models.BooleanField(default=False, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.is_superuser:
            self.is_superuser = False
        super(UserAccount, self).save(*args, **kwargs)

    def full_name(self):
        try:
            full_name = str(self.last_name) + \
                        " " + str(self.first_name)
        except:
            full_name = ""
        return full_name.strip()


    def __str__(self):
        return str(self.username)
   

    class Meta:
        verbose_name_plural = '01. Danh sách người dùng'


class FileProduct(models.Model):
    """
    Ảnh sản phẩm
    """
    images_product = models.FileField(upload_to='images product/',null=True, blank=True, verbose_name='Hình ảnh')
    file_product = models.ForeignKey(to="Product", on_delete=models.SET_NULL, blank=True, null=True,verbose_name='Hình ảnh sản phẩm' )
    
    class Meta:
        verbose_name_plural = '02. Ảnh sản phẩm '
    
    def __str__(self):
        return str(self.file_product)

class Product(TimeStampedModelMixin):
    """
    Sản phẩm
    """
    product = models.CharField(max_length=255,blank=False, null=False, verbose_name='Tên sản phẩm')
    price = models.IntegerField(blank=False, null=False, verbose_name='Giá')
    function = models.CharField(max_length=1024, blank=False, null=False, verbose_name='Công dụng')
    dosage = models.CharField(max_length=255, blank=False, null=False, verbose_name='Tần suất sử dụng')
    keyword = models.CharField(max_length=255, blank=False, null=False, verbose_name='Từ khóa Routine')
    estimate = models.CharField(max_length=255, blank=False, null=False, verbose_name='Ước lượng sử dụng')
    note = models.CharField(max_length=1024, blank=False, null=False, verbose_name='Lưu ý')
    
    class Meta:
        verbose_name_plural = '03. Sản phẩm'

    def __str__(self):
        return str(self.product)


class Service(TimeStampedModelMixin):
    """
    Dịch vụ
    """
    service = models.CharField(max_length=255,blank=False, null=False, verbose_name='Tên dịch vụ')
    function = models.CharField(max_length=1024, blank=True, null= True, verbose_name='Tác dụng')
    note = models.CharField(max_length=1024, blank=True, null=True, verbose_name='Lưu ý')

    class Meta:
        verbose_name_plural = '04. Dịch vụ'

    def __str__(self):
        return self.service

class TypeStatus(TimeStampedModelMixin):
    """
    Loại Tình trạng khách hàng
    """
    name = models.CharField(max_length=255,blank=False, null=False, verbose_name='Tên tình trạng')
    description = models.CharField(max_length=200,blank=True, null=True, verbose_name='Mô tả tình trạng')

    class Meta:
        verbose_name_plural = '05. Loại Tình trạng khách hàng'

    def __str__(self):
        return self.name
class TypeCustommer(TimeStampedModelMixin):
    """
    Nhóm khách hàng
    """
    name = models.CharField(max_length=255,blank=False, null=False, verbose_name='Tên Nhóm khách hàng')
    description = models.CharField(max_length=200,blank=True, null=True, verbose_name='Mô tả Nhóm khách hàng')

    class Meta:
        verbose_name_plural = '06. Nhóm khách hàng'

    def __str__(self):
        return self.name

class Customer(TimeStampedModelMixin):
    """
    Khách hàng
    """
    user = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, blank=True, null= True, verbose_name='user')
    full_name = models.CharField(max_length=255,blank=False, null=False, verbose_name='Tên khách hàng')
    numberphone = models.IntegerField(unique=True,blank=False, null=False, verbose_name='Số điện thoại')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    age = models.CharField(max_length=2,blank=True, null=True, verbose_name='Tuổi')
    profession = models.CharField(max_length=255, blank=True, null=True, verbose_name='Nghề nghiệp')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Địa chỉ')
    status = models.ForeignKey(TypeStatus,on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Tình trạng khách hàng')
    type = models.ForeignKey(TypeCustommer,on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Nhóm khách hàng')
    note = models.CharField(max_length=1024, blank=True, null=True, verbose_name='Ghi chú khách hàng')

    class Meta:
        verbose_name_plural = '07. Khách Hàng'

    def __str__(self):
        return self.full_name


class FileOrder(models.Model):
    """ File ảnh đơn kê """
    file_before = models.FileField(upload_to='images before/',null=True, blank=True, verbose_name='Hình ảnh trước điều trị')
    file_after = models.FileField(upload_to='images after/',null=True, blank=True, verbose_name='Hình ảnh sau điều trị')
    img_order = models.ForeignKey(to='Order', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Hình ảnh đơn kê')

    class Meta:
        verbose_name_plural = '08. Ảnh đơn kê'

    def __str__(self):
        return str(self.img_order)
        # return str(self.file_before) + " - " + str(self.file_after)

class Day(TimeStampedModelMixin):
    day = models.CharField(max_length=50, blank=True, null=True, verbose_name='Ngày')

    class Meta:
        verbose_name_plural = '09. Ngày'

    def __str__(self):
        return str(self.day)

class Buoi(TimeStampedModelMixin):
    buoi = models.CharField(max_length=50, blank=True, null=True, verbose_name='Ngày')

    class Meta:
        verbose_name_plural = '10. Buổi'

    def __str__(self):
        return str(self.buoi)

class DetailOrderProduct(TimeStampedModelMixin):
    """ Chi tiết danh sách kê thuốc nằm trong đơn kê """
    user = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='user')
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Thuốc')
    day = models.ForeignKey(Day, on_delete=models.SET_NULL,blank=True, null=True, verbose_name='Ngày')
    buoi = models.ForeignKey(Buoi, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Buổi')
    order = models.ForeignKey(to='Order', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Đơn kê')
    any_product = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural ='11. Chi tiết các sản phẩm trong Đơn kê'

    def __str__(self):
        return str(self.order)


class DetailOrderService(TimeStampedModelMixin):
    """ Chi tiết dịch vụ nằm trong đơn kê"""

    user = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='user')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Tên dịch vụ')
    time = models.CharField(max_length=8, null=True, blank=True, verbose_name='Thời gian')
    note = models.CharField(max_length=150, blank=True, null=True, verbose_name='Lưu ý')
    order = models.ForeignKey(to='Order', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Đơn kê')
    any_service = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = '12. Chi tiết các dịch vụ đi trong Đơn kê'

    def __str__(self):
        return str(self.order)


class Order(TimeStampedModelMixin):
    """ Đơn kê """
    user = models.ForeignKey(UserAccount, on_delete=models.SET_NULL,null=True, blank=True,verbose_name='user')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True, blank=True, verbose_name='Tên khách hàng')
    day_re_examination = models.DateField(null=True, blank=True,verbose_name='Ngày tái khám')
    use_to = models.TextField(null=True,blank=True, verbose_name='Cách dùng')
    detail_caleder_examination = models.TextField(null=True, blank=True, verbose_name='Chi tiết lịch khám')
    note_order = models.TextField(null=True, blank=True, verbose_name='Ghi chú đơn kê')
    pathological = models.TextField(null=True,blank=True, verbose_name='Bệnh lý')
    
    class Meta:
        verbose_name_plural = '13. Đơn kê'

    def __str__(self):
        return str(self.user)

class Notifications(TimeStampedModelMixin):
    """
    Thông báo
    """
    content = models.CharField(max_length=200,verbose_name="Nội dung thông báo")
    is_view = models.BooleanField(default=False,verbose_name="Đã xem")
    is_sent = models.BooleanField(default=False, verbose_name="Đã gửi")
    user = models.ForeignKey(UserAccount, on_delete=models.SET_NULL,null=True,blank=True, verbose_name="User")
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True,blank=True, verbose_name="Khách hàng")
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True,)

    class Meta:
        verbose_name_plural = _('14. Thông báo')