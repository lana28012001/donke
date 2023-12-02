from django.urls import include, path, re_path

from django.conf import settings
from django.conf.urls.static import static


# from core.views.admin import view_admin, view_organization, view_role
from core.views import view_customer, view_order, view_product, view_service, views, view_auth, view_home, view_user, view_api

from django.contrib.auth.decorators import login_required


urlpatterns = [
    # 
    path('', view_home.HomeView.as_view(), name='home'),
    path('login', view_auth.LoginView.as_view() , name ='login'),
    re_path('logout', login_required(view_auth.LogoutView.as_view()) , name ='logout'),
    re_path('changepassword', login_required(view_auth.ChangePasswordView) , name ='changepassword'),

    # admin
    # # User: Nguoi dung
    re_path('manage/user', login_required(view_user.UserView.as_view()), name='manage_user'),
    re_path(r'manage/update/user/(?P<id>\d+)$', login_required(view_user.UpdateUserView.as_view()), name='manage_update_user' ),
    re_path(r'manage/delete/user/(?P<id>\d+)$', login_required(view_user.DeleteUserView.as_view()), name='manage_delete_user' ),
    
    # # Customer: Khach hang
    re_path('manage/customer', login_required(view_customer.CustomerView.as_view()), name='manage_customer'),
    re_path(r'manage/update/customer/(?P<id>\d+)$', login_required(view_customer.UpdateCustomerView.as_view()), name='manage_update_customer' ),
    re_path(r'manage/delete/customer/(?P<id>\d+)$', login_required(view_customer.DeleteCustomerView.as_view()), name='manage_delete_customer' ),
    re_path(r'customer/order/(?P<id>\d+)$', login_required(view_customer.CustomerOrderView.as_view()), name='manage_customer_order'),

    # Product: Sảm phẩm/Thuốc
    # re_path('manage/product', login_required(view_product_bk.ProductView.as_view()), name='manage_product'),
    # re_path(r'manage/update/product/(?P<id>\d+)$', login_required(view_product_bk.UpdateProductView.as_view()), name='manage_update_product' ),
    # re_path(r'manage/delete/product/(?P<id>\d+)$', login_required(view_product_bk.DeleteProductView.as_view()), name='manage_delete_product' ),

    re_path('manage/product', login_required(view_product.ListProduct), name='manage_product'),
    re_path('manage/add/product', login_required(view_product.AddProduct), name='manage_add_product'),
    re_path(r'manage/update/product/(?P<id>\d+)$', login_required(view_product.UpdateProduct), name='manage_update_product' ),
    re_path(r'manage/delete/product/(?P<id>\d+)$', login_required(view_product.DeleteProductView.as_view()), name='manage_delete_product' ),

    # Service: Dich vu
    re_path('manage/service', login_required(view_service.ServiceView.as_view()), name='manage_service'),
    re_path(r'manage/update/service/(?P<id>\d+)$', login_required(view_service.UpdateServiceView.as_view()), name='manage_update_service' ),
    re_path(r'manage/delete/service/(?P<id>\d+)$', login_required(view_service.DeleteServiceView.as_view()), name='manage_delete_service' ),

    # Order: Đơn kê
    re_path('manage/order', login_required(view_order.ListOrder), name='manage_order'),
    re_path('manage/add/order', login_required(view_order.AddOrder), name='manage_add_order'),
    re_path(r'manage/update/order/(?P<id>\d+)$', login_required(view_order.UpdateOrder), name='manage_update_order'),
    re_path(r'manage/delete/order/(?P<id>\d+)$', login_required(view_order.DeleteOrderView.as_view()), name='manage_delete_order'),
    re_path(r'manage/view/order/(?P<id>\d+)$', login_required(view_order.ViewOrder), name='manage_view_order'),

    re_path(r'^exportExcelHome$', login_required(view_order.Home_Export_Excel1), name='home_export_excel'), 

    # api notification
    path('manager/notification', view_api.ManageNotification,name='manager_notification'),
    path('list/notification', view_api.List_Notification.as_view(), name='list_notification'),
    re_path(r'notification/is/sent/(?P<id>\d+)$', login_required(view_api.Notification_is_sent), name='notification_is_sent'),
    re_path(r'notification/is/view/(?P<id>\d+)$', login_required(view_api.Notification_is_view), name='notification_is_view'),
    # path('notification_read_all/', view_api.Notification_read_add.as_view(), name='notification_is_sent'),

    # xem nhiều thông báo
    path('view/more/notification', view_api.View_More_Notification, name='view_more_notification'),
    
]

urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
            
urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




