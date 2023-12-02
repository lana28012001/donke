
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from core.models import Customer, Order, TypeCustommer, TypeStatus, UserAccount
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import re

class CustomerView(View):
    def get(self, request):
        if request.user.is_superuser:
            list_customer = Customer.objects.all().order_by('-id')
            list_status = TypeStatus.objects.all()
            list_type = TypeCustommer.objects.all()
            # paginator = Paginator(customer_list, 10)
            # page = request.GET.get('page')
            # try:
            #     customers = paginator.page(page)
            # except PageNotAnInteger:
            #     customers = paginator.page(1)
            # except EmptyPage:
            #     customers = paginator.page(paginator.num_pages)

            context = {
                'list_customer':list_customer,
                'list_type':list_type,
                'list_status':list_status
            }
            return render(request, 'customer.html', context)
        else:
            data_id =  request.user.id
            list_customer = Customer.objects.filter(user_id=data_id).all().order_by('-id')
            list_type = TypeStatus.objects.all()
            list_status = TypeStatus.objects.all()
            context = {
                'list_customer':list_customer,
                'list_type':list_type,
                'list_status':list_status
            }
            return render(request, 'customer.html', context)

    def post(self,request):
        data_user = request.POST['user']
        fullname = str(request.POST['full_name']).strip()
        numberphone = str(request.POST['numberphone']).strip()
        email = str(request.POST['email']).strip()
        age = str(request.POST['age']).strip()
        address = str(request.POST['address']).strip()
        profession = str(request.POST['profession']).strip()
        status = request.POST['status']
        type = request.POST['type']
        note = request.POST['note']

        if (fullname == '') or (numberphone == ''):
            return JsonResponse(
                {
                    'type': 'error',
                    'message': 'Lỗi thiếu thông tin bắt buộc: Tên khách hàng, SĐT',
                    }, safe=True)
        elif ((numberphone != "") and (numberphone).isnumeric() == False) or((age != "") and (age).isnumeric() == False):
            return JsonResponse(
            {
                'type': 'error',
                'message': 'SĐT, Tuổi chỉ chứa kí tự số',
                }, safe=True)

        elif (numberphone != "") and (not re.search(r'^[0-9]{10,13}$', numberphone)):
            return JsonResponse(
                {
                    'type': 'error',
                    'message': 'SĐT không đúng định dạng(10 - 13 số)',
                    }, safe=True)
        elif (email != "") and (not re.search(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email)):
                return JsonResponse(
                {
                    'type': 'error',
                    'message': 'Email này không đúng định dạng'
                    }, safe=True)
        else:
            if (numberphone != '') and (Customer.objects.filter(numberphone=numberphone).exists() == True):
                return JsonResponse(
                    {
                        'type': 'error',
                        'message': 'SĐT này đã tồn tại trên hệ thống',
                        }, safe=True)
            else:
                try:
                    # id_user = request.user.id
                    if numberphone == '':
                        numberphone = None
                    if email == '':
                        email = None
                    if age == '':
                        age = None
                    if address == '':
                        address = None
                    if profession == '':
                        profession = None
                    if note == '':
                        note = None
                    createcustomer = Customer.objects.create(user_id=data_user,full_name=fullname,numberphone=numberphone,email=email,age=age,address=address,profession=profession, status_id=status, type_id=type,note=note)
                    return JsonResponse(
                            {
                                'type': 'success',
                                'message': 'Thêm mới khách hàng thành công'
                                }, safe=True)
                except Exception as e:
                    return JsonResponse(
                            {
                            'type': 'error',
                            'message': 'Lỗi ' + str(e)
                            },safe=True)
        

class CustomerOrderView(View):
     def get(self, request,id):
        data_id =  request.user.id
        data_customer = get_object_or_404(Customer, pk=id)
        list_order = Order.objects.filter(customer_id=data_customer.id).all().order_by('-id')
        context = {
            'list_order':list_order,
            'data_customer':data_customer,
        }
        return render(request, 'customer_order.html', context)   


class UpdateCustomerView(View):
    def get(self,request,id):
        data = get_object_or_404(Customer, pk=id)
        if data.status != None:
            id_status = data.status.id
            name_status = data.status.name
        if data.status == None:
            id_status = None
            name_status = None
        if data.type != None:
            id_type = data.type.id
            name_type = data.type.name
        if data.type == None:
            id_type = None
            name_type = None
        customer = {
            'id':data.id,
            'full_name': data.full_name,
            'numberphone': data.numberphone,
            'age': data.age,
            'email': data.email,
            'address': data.address,
            'profession': data.profession,
            'id_type': id_type,
            'name_type':name_type,
            'id_status':id_status,
            'name_status':name_status,
            'note':data.note,
        }
        return JsonResponse(
                {
                'type': 'success',
                'data_customer':customer
                },safe=True)
        
    def post(self,request,id):
        data_cu = get_object_or_404(Customer, pk=id)
        fullname = str(request.POST['full_name']).strip()
        numberphone = str(request.POST['numberphone']).strip()
        email = str(request.POST['email']).strip()
        age = str(request.POST['age']).strip()
        profession = str(request.POST['profession']).strip()
        address = str(request.POST['address']).strip()
        status = request.POST['status']
        type = request.POST['type']
        note = request.POST['note']

        if (fullname == ''):
            return JsonResponse(
                {
                    'type': 'error',
                    'message': 'Lỗi thiếu thông tin bắt buộc: Tên khách hàng',
                    }, safe=True)
        elif  ((numberphone != "") and (numberphone).isnumeric() == False) or((age != "") and (age).isnumeric() == False):
            return JsonResponse(
            {
                'type': 'error',
                'message': 'CCCD/CMND, SĐT, Tuổi chỉ chứa kí tự số',
                }, safe=True)

        elif (numberphone != "") and (not re.search(r'^[0-9]{10,13}$', numberphone)):
            return JsonResponse(
                {
                    'type': 'error',
                    'message': 'SĐT không đúng định dạng(10 - 13 số)',
                    }, safe=True)
        elif (email != "") and (not re.search(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email)):
                return JsonResponse(
                {
                    'type': 'error',
                    'message': 'Email này không đúng định dạng'
                    }, safe=True)            
        else:
            try:
                id_user = request.user.id
                if numberphone == '':
                    numberphone = None
                if email == '':
                    email = None
                if age == '':
                    age = None
                if address == '':
                    address = None
                if profession == '':
                    profession = None
                if note == '':
                    note = None    
                update = Customer.objects.filter(id=id).update(user_id=id_user,full_name=fullname,numberphone=numberphone,email=email,age=age,address=address,profession=profession, status_id=status, type_id=type,note=note)
                return JsonResponse(
                    {
                        'type': 'success',
                        'message': 'Cập nhập Khách hàng thành công'
                        }, safe=True)
            except Exception as e:
                return JsonResponse(
                        {
                        'type': 'error',
                        'message': 'Lỗi' + str(e)
                        },safe=True)


class DeleteCustomerView(View):
    def get(self,request,id):
        data = get_object_or_404(Customer, pk=id)
        if data.status != None:
            id_status = data.status.id
            name_status = data.status.name
        if data.status == None:
            id_status = None
            name_status = None
        if data.type != None:
            id_type = data.type.id
            name_type = data.type.name
        if data.type == None:
            id_type = None
            name_type = None
        customer = {
            'id':data.id,
            'full_name': data.full_name,
            'numberphone': data.numberphone,
            'age': data.age,
            'email': data.email,
            'address': data.address,
            'profession': data.profession,
            'id_type': id_type,
            'name_type':name_type,
            'id_status':id_status,
            'name_status':name_status,
            'note':data.note,
        }
        return JsonResponse(
                {
                'type': 'success',
                'data_customer':customer
                },safe=True)

    def post(self,request,id):
        try:
            data = get_object_or_404(Customer, pk=id)
            data.delete()
            return JsonResponse(
                {
                    'type': 'success',
                    'message': 'Xóa Khách hàng thành công'
                    }, safe=True)
        except Exception as e:
            return JsonResponse(
                {
                    'type': 'error',
                    'message': 'Lỗi ' + str(e)
                    }, safe=True)
        

