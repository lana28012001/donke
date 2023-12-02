from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from core.models import Customer, DetailOrderProduct, DetailOrderService, Notifications, Order, Product, Service, TypeCustommer, TypeStatus, UserAccount
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import re
from django.contrib.auth.hashers import make_password

class UserView(View):
    def get(self, request):
        if request.user.is_superuser:
            list_user = UserAccount.objects.all().order_by('-id')
            # paginator = Paginator(customer_list, 10)
            # page = request.GET.get('page')
            # try:
            #     customers = paginator.page(page)
            # except PageNotAnInteger:
            #     customers = paginator.page(1)
            # except EmptyPage:
            #     customers = paginator.page(paginator.num_pages)

            context = {
                'list_user':list_user
            }
            return render(request, 'user.html', context)
        
        return HttpResponse("Bạn không có quyền truy cập vào đây.")
        
    def post(self,request):
        if request.user.is_superuser:
            username = str(request.POST['username']).strip()
            password1 = str(request.POST['password1']).strip()
            password2 = str(request.POST['password2']).strip()
            phonenumber = str(request.POST['phonenumber']).strip() 
            email = str(request.POST['email']).strip()
            address = str(request.POST['address']).strip()

            if (username == '') or (phonenumber == '') or (password1 == '')  or (password2 == ''):
                return JsonResponse(
                    {
                        'type': 'error',
                        'message': 'Lỗi thiếu thông tin bắt buộc: Username, Password, SĐT',
                        }, safe=True)

            elif (username != "") and (UserAccount.objects.filter(username=username).exists() == True):
                return JsonResponse(
                {
                    'type': 'error',
                    'message': 'Username này đã tồn tại.',
                    }, safe=True)
            elif (password1 != "") and (password2 != "") and (password1 != password2):
                return JsonResponse(
                {
                    'type': 'error',
                    'message': 'Mật khẩu không trùng khớp.',
                    }, safe=True)

            elif ((password1 != '') and (password2 != "")) and  ((re.match(r'(?=.{8})(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[!@#$%^&*])', password1)) == None):
                    return JsonResponse(
                    {
                        'type': 'error',
                        'message': 'Mật khẩu phải có 8 kí tự gồm chữ hoa, thường, số, kí tự đặc biệt!',
                        }, safe=True)
            elif (phonenumber != "") and (not re.search('^[0-9]{10,13}$', phonenumber)):
                return JsonResponse(
                {
                    'type': 'error',
                    'message': 'SĐT phải gồm 10 - 13 số',
                    }, safe=True)

            elif (phonenumber != "") and (UserAccount.objects.filter(phonenumber=phonenumber).exists() == True):
                return JsonResponse(
                {
                    'type': 'error',
                    'message': 'SĐT này đã tồn tại.',
                    }, safe=True)

            elif (email != "") and (not re.search(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email)):
                return JsonResponse(
                {
                    'type': 'error',
                    'message': 'Email này không đúng định dạng'
                    }, safe=True)
            elif (email != "") and (UserAccount.objects.filter(email=email).exists() == True):
                return JsonResponse(
                {
                    'type': 'error',
                    'message': 'Email này đã tồn tại.',
                    }, safe=True)
            else:
                try:
                    
                    if address == '':
                        address = None
                    create_ser = UserAccount.objects.create(username=username,password=make_password(password1),email=email,phonenumber=phonenumber,address=address)
                    return JsonResponse(
                        {
                            'type': 'success',
                            'message': 'Thêm mới người dùng thành công'
                            }, safe=True)
                except Exception as e:
                    return JsonResponse(
                            {
                            'type': 'error',
                            'message': 'Lỗi ' + str(e)
                            },safe=True)

        return HttpResponse("Bạn không có quyền truy cập vào đây.")
        
class UpdateUserView(View):
    def get(self,request,id):
        if request.user.is_superuser:
            data = get_object_or_404(UserAccount, pk=id)
            
            data_user = {
                'id':data.id,
                'username': data.username,
                'phonenumber': data.phonenumber,
                'email': data.email,
                'address': data.address,

            }
            return JsonResponse(
                    {
                    'type': 'success',
                    'data_user':data_user
                    },safe=True)
        return HttpResponse("Bạn không có quyền truy cập vào đây.")
            
    def post(self,request,id):
        if request.user.is_superuser:
            data_u = get_object_or_404(UserAccount, pk=id)
            phonenumber = str(request.POST['phonenumber']).strip()
            email = str(request.POST['email']).strip() 
            address = str(request.POST['address']).strip()

            if (phonenumber == '') :
                    return JsonResponse(
                        {
                            'type': 'error',
                            'message': 'Lỗi thiếu thông tin bắt buộc: SĐT',
                            }, safe=True)
            
            elif (phonenumber != "") and (not re.search('^[0-9]{10,13}$', phonenumber)):
                return JsonResponse(
                {
                    'type': 'error',
                    'message': 'SĐT phải gồm 10 - 13 số',
                    }, safe=True)

            elif (email != "") and (not re.search(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email)):
                return JsonResponse(
                {
                    'type': 'error',
                    'message': 'Email này không đúng định dạng'
                    }, safe=True)

            else:
                try:
                    # id_user = request.user.id
                    if address == '':
                        address = None
                    update = UserAccount.objects.filter(id=id).update(email=email,phonenumber=phonenumber,address=address)
                    return JsonResponse(
                        {
                            'type': 'success',
                            'message': 'Cập nhập User thành công'
                            }, safe=True)
                except Exception as e:
                    return JsonResponse(
                        {
                        'type': 'error',
                        'message': 'Lỗi ' + str(e)
                        },safe=True)
        return HttpResponse("Bạn không có quyền truy cập vào đây.")


class DeleteUserView(View):
    def get(self,request,id):
        if request.user.is_superuser:
            # id_user_get =  request.user.id
            data_user = get_object_or_404(UserAccount, pk=id)
            # list_orders = Order.objects.filter(user_id=data_user.id)
            list_customer = Customer.objects.filter(user_id=data_user.id)
            list_user = UserAccount.objects.all()
            context = {
                # 'list_orders':list_orders,
                'list_customer':list_customer,
                'list_user':list_user,
                'data_user':data_user
            }
            return render(request, 'delete_user.html', context)
        return HttpResponse("Bạn không có quyền truy cập vào đây.")

    def post(self,request,id):
        if request.user.is_superuser:
            try:
                user_delete = get_object_or_404(UserAccount, pk=id)
                
                id_user_new = request.POST['usernew']
                if id == id_user_new:
                    return JsonResponse(
                    {
                        'type': 'error',
                        'message': 'Không thể chọn User mới trùng với User cần xóa'
                        }, safe=True)
                elif user_delete.username =='admin':
                    return JsonResponse(
                    {
                        'type': 'error',
                        'message': 'Không được phép xóa user admin này'
                        }, safe=True)

                list_customer = Customer.objects.filter(user_id=user_delete.id)
                # print(len(list_customer))
                for i_customer in list_customer:
                    update_customer = Customer.objects.filter(id=i_customer.id).update(user_id=id_user_new)

                list_order = Order.objects.filter(user_id=user_delete.id)
                # print(len(list_order))
                for i_order in list_order:
                    update_or = Order.objects.filter(id=i_order.id).update(user_id=id_user_new)
                    
                list_detail_product = DetailOrderProduct.objects.filter(user_id=user_delete.id)
                # print(len(list_detail_product))
                for i_detail_product in list_detail_product:
                    update_cu_product = DetailOrderProduct.objects.filter(id=i_detail_product.id).update(user_id=id_user_new)

                list_detail_service = DetailOrderService.objects.filter(user_id=user_delete.id)
                # print(len(list_detail_service))
                for i_detail_service in list_detail_service:
                    update_cu_service = DetailOrderService.objects.filter(id=i_detail_service.id).update(user_id=id_user_new)

                list_notification = Notifications.objects.filter(user_id=user_delete.id)
                # print(len(list_notification))
                for i_notification in list_notification:
                    update_notification = Notifications.objects.filter(id=i_notification.id).update(user_id=id_user_new)
                    
                user_delete.delete()
                   
                return JsonResponse(
                    {
                        'type': 'success',
                        'message': 'Xóa User thành công'
                        }, safe=True)
            except Exception as e:
                return JsonResponse(
                    {
                        'type': 'error',
                        'message': 'Lỗi ' + str(e)
                        }, safe=True)
        
        return HttpResponse("Bạn không có quyền truy cập vào đây.")

