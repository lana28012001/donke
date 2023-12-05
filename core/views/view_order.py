
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from core.models import Buoi, Customer, Day, DetailOrderProduct, DetailOrderService, FileOrder, Order, Product, Service, TypeCustommer, TypeStatus, UserAccount
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
import copy

from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import re
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import datetime
import json
import re
from django.conf import settings
import io
import xlsxwriter
from django.db.models import Sum
import os, sys
import time
import subprocess
from django.db.models import Q
from django.utils import timezone
from unidecode import unidecode
import locale
from pathlib import Path
import shutil
import itertools
locale.setlocale(locale.LC_ALL, "")

def ListOrder(request):
    if request.method == 'GET':
        # paginator = Paginator(order_list, 10)
        # page = request.GET.get('page')
        # try:
        #     orders = paginator.page(page)
        # except PageNotAnInteger:
        #     orders = paginator.page(1)
        # except EmptyPage:
        #     orders = paginator.page(paginator.num_pages)

        dict_total_img_before = {}
        dict_total_img_after = {}
        id_user =  request.user.id
        list_order = Order.objects.filter(user_id=id_user).order_by('-id')
        for i_order in list_order:
            list_data_img = FileOrder.objects.filter(img_order_id=i_order.id)
            list_img_before = []
            list_img_after = []
            for i_img in list_data_img:
                if i_img.file_before != '':
                    list_img_before.append([i_order.id,i_img.file_before])
                if i_img.file_after != '':
                    list_img_after.append([i_order.id,i_img.file_after])
                    
            if len(list_img_before) > 0:
                dict_total_img_before[i_order.id] = list_img_before
            if len(list_img_after) > 0:
                dict_total_img_after[i_order.id] = list_img_after

        context = {
            'list_order':list_order,
            'list_before':dict_total_img_before,
            'list_after':dict_total_img_after,

        }
        return render(request, 'order/list_order.html', context)
    
@login_required
def AddOrder(request):
    if  request.method == 'GET':
        if request.user.is_superuser:
            list_customer = Customer.objects.all()
            list_day = Day.objects.all()
            list_buoi = Buoi.objects.all()

            # print(len(list_customer))
            list_product = Product.objects.all()
            list_service = Service.objects.all()
            context = {
                'list_customer':list_customer,
                'list_day':list_day,
                'list_buoi':list_buoi,
                'list_product':list_product,
                'list_service':list_service,
                
                }
            return render(request, 'order/add_order.html', context)
        else:
            id =  request.user.id
            list_customer = Customer.objects.filter(user_id=id).all()
            list_product = Product.objects.all()
            list_service = Service.objects.all()
            list_day = Day.objects.all()
            list_buoi = Buoi.objects.all()
            context = {
                'list_customer':list_customer,
                'list_product':list_product,
                'list_service':list_service,
                'list_day':list_day,
                'list_buoi':list_buoi,
                
                }
            return render(request, 'order/add_order.html', context)
    elif  request.method == 'POST':
        try:

            if request.POST['day_re_examination'] == '':
                day_re_examination = None
            else:
                day_re_examination = request.POST['day_re_examination']
            if request.POST['use_to'] == '':
                use_to = None
            else:
                use_to = request.POST['use_to']
            if request.POST['detail_caleder_examination'] == '':
                detail_caleder_examination = None
            else:
                detail_caleder_examination = request.POST['detail_caleder_examination']
            if request.POST['note_order'] == '':
                note_order = None
            else:
                note_order = request.POST['note_order']
            if request.POST['pathological'] == '':
                pathological = None
            else:
                pathological = request.POST['pathological']
            # chi tiết sản phẩm trong đơn kê
            list_day = []
            for field in request.POST:
                if "day-" in field:
                    list_day.append(field)
            list_buoi = []
            for field in request.POST:
                if "buoi-" in field:
                    list_buoi.append(field)
            list_product = []
            for field in request.POST:
                if "product-" in field:
                    list_product.append(field)
            if len(list_day) > 0:
                data_order = Order.objects.create(user_id=request.POST['user'],customer_id=request.POST['customer'],day_re_examination=day_re_examination,use_to=use_to,detail_caleder_examination=detail_caleder_examination,note_order=note_order,pathological=pathological)
                for idx,i in enumerate(list_day):
                    if request.POST[i] != "":
                        data_product_order = DetailOrderProduct.objects.create(user_id=request.POST['user'],order_id=data_order.pk,day_id=request.POST[list_day[idx]],product_id=request.POST[list_product[idx]],buoi_id=request.POST[list_buoi[idx]])

            # chi tiết dịch vụ trong đơn kê
            list_service = []
            # requestPost = request.POST
            for field in request.POST:
                if "service-" in field:
                    list_service.append(field)
            list_time = []
            for field in request.POST:
                if "time-" in field:
                    list_time.append(field)
            list_note = []
            for field in request.POST:
                if "note-" in field:
                    list_note.append(field)
            if len(list_service) > 0:
                for idx,i in enumerate(list_service):
                    if request.POST[i] != "":
                        data_product_order = DetailOrderService.objects.create(user_id=request.POST['user'],order_id=data_order.pk,service_id=request.POST[list_service[idx]],time=request.POST[list_time[idx]],note=request.POST[list_note[idx]])

            fs = FileSystemStorage()
            # file anh truoc dieu tri
            list_file_before = request.FILES.getlist('file_before[]')
            for i_file_before in list_file_before:
                new_name_before = "add_before_"+ unidecode(str(request.POST['customer']).replace(' ','-')) + "_"+ datetime.datetime.now().strftime("%Y%m%d%H%M%S") +"."+ str(i_file_before.name).split('.')[-1]
                filename = fs.save(new_name_before, i_file_before)
                FileOrder.objects.create(file_before="media\\"+filename, img_order_id = data_order.pk)
            
            # file anh sau dieu tri
            list_file_after = request.FILES.getlist('file_after[]')
            for i_file_after in list_file_after:
                new_name_after = "add_after_"+ unidecode(str(request.POST['customer']).replace(' ','-')) + "_"+ datetime.datetime.now().strftime("%Y%m%d%H%M%S") +"."+ str(i_file_after.name).split('.')[-1]
                filename = fs.save(new_name_after, i_file_after)
                FileOrder.objects.create(file_after="media\\"+filename, img_order_id = data_order.pk)
            
            messages.success(request, 'Thêm đơn kê thành công!')
            return redirect('manage_order')

        except Exception as e:
            print(e)
            HttpResponse('Thêm đơn kê thất bại!, Vui lòng kiểm tra lại')
       
@login_required
def UpdateOrder(request,id):
    if  request.method == 'GET':
        orders = get_object_or_404(Order, pk=id)
        datacustomer = orders.customer.id
        # print(datacustomer)
        list_order_product = DetailOrderProduct.objects.filter(order_id=orders.pk)
        list_order_service = DetailOrderService.objects.filter(order_id=orders.pk)
        customers = Customer.objects.all()
        products = Product.objects.all()
        services = Service.objects.all()
        days = Day.objects.all()
        sessions = Buoi.objects.all()
        list_img = FileOrder.objects.filter(img_order_id=orders.pk)
        list_before = []
        list_after = []
        for i_img in list_img:
            if i_img.file_before != '':
                list_before.append(i_img.file_before.url)
            if i_img.file_after != '':
                list_after.append(i_img.file_after.url)
                
        context = {
            'id_order': orders.pk,
            'orders': orders,
            'datacustomer':datacustomer,
            'list_customer':customers,
            'products':products,
            'services':services,
            'days':days,
            'sessions':sessions,
            'list_order_product':list_order_product,
            'list_order_service':list_order_service,
            'list_before':list_before,
            'list_after':list_after,
            'use_to':orders.use_to,
            'note_order':orders.note_order,
            }
        return render(request, 'order/update_order.html', context)     
    else:
        try:
            get_data_order = get_object_or_404(Order, pk=id)

            if request.POST['day_re_examination'] == '' or request.POST['day_re_examination'] == 'None':
                day_re_examination = None
            else:
                day_re_examination = request.POST['day_re_examination']

            if request.POST['use_to'] == '' or request.POST['use_to'] == 'None':
                use_to = None
            else:
                use_to = request.POST['use_to']

            if request.POST['detail_caleder_examination'] == '' or request.POST['detail_caleder_examination'] == 'None':
                detail_caleder_examination = None
            else:
                detail_caleder_examination = request.POST['detail_caleder_examination']

            if request.POST['note_order'] == '' or request.POST['note_order'] == 'None':
                note_order = None
            else:
                note_order = request.POST['note_order']

            if request.POST['pathological'] == '' or request.POST['pathological'] == 'None':
                pathological = None
            else:
                pathological = request.POST['pathological']

            data_order = Order.objects.filter(id=id).update(user_id=request.POST['user'],customer_id=request.POST['customer'],day_re_examination=day_re_examination,use_to=use_to,detail_caleder_examination=detail_caleder_examination,note_order=note_order,pathological=pathological)

            # chi tiết sản phẩm trong đơn kê
            list_day = []
            for field in request.POST:
                if "day-" in field:
                    list_day.append(field)
            list_buoi = []
            for field in request.POST:
                if "buoi-" in field:
                    list_buoi.append(field)
            list_product = []
            for field in request.POST:
                if "product-" in field:
                    list_product.append(field)
            list_productid = []
            for field in request.POST:
                if "productid-" in field:
                    list_productid.append(field)

            list_product_order_old = DetailOrderProduct.objects.filter(order_id=id)

            if (len(list_day) > 0) and (len(list_product_order_old) == len(list_day)): # Câp nhật sản phẩm
                for idx, i_product in enumerate(list_product_order_old):
                    # d = request.POST[list_day[idx]]
                    # pro = request.POST[list_product[idx]]
                    # b = request.POST[list_buoi[idx]]
                    # print(i_product.product.product)
                    data_product_order_update = DetailOrderProduct.objects.filter(id=request.POST[list_productid[idx]]).update(user_id=request.POST['user'],day_id=request.POST[list_day[idx]],product_id=request.POST[list_product[idx]],buoi_id=request.POST[list_buoi[idx]])
            
            elif (len(list_day) > 0) and (len(list_product_order_old) < len(list_day)): # Thêm hàng sản phẩm: Xóa sản phẩm cũ và Thêm list sản phẩm theo order_id
                list_product_order_old.delete()
                for idx,i in enumerate(list_day):
                    if request.POST[i] != "":
                        data_product_create = DetailOrderProduct.objects.create(user_id=request.POST['user'],order_id=id,day_id=request.POST[list_day[idx]],product_id=request.POST[list_product[idx]],buoi_id=request.POST[list_buoi[idx]])
            
            elif (len(list_product_order_old) > len(list_day)): # Xóa bớt hàng sản phẩm: Xóa sản phẩm cũ và Thêm list sản phẩm theo order_id
                list_product_order_old.delete()
                for idx,i in enumerate(list_day):
                    if request.POST[i] != "":
                        data_product_create = DetailOrderProduct.objects.create(user_id=request.POST['user'],order_id=id,day_id=request.POST[list_day[idx]],product_id=request.POST[list_product[idx]],buoi_id=request.POST[list_buoi[idx]])

            # chi tiết dịch vụ trong đơn kê
            list_service = []
            for field in request.POST:
                if "service-" in field:
                    list_service.append(field)
            list_time = []
            for field in request.POST:
                if "time-" in field:
                    list_time.append(field)
            list_note = []
            for field in request.POST:
                if "note-" in field:
                    list_note.append(field)
            list_serviceid = []
            for field in request.POST:
                if "serviceid-" in field:
                    list_serviceid.append(field)
            
            list_service_order_old = DetailOrderService.objects.filter(order_id=id)

            if (len(list_service) > 0) and (len(list_service_order_old) == len(list_service)): # cập nhật hàng dịch vụ
                for idx, i_service in enumerate(list_service_order_old):
                    data_service_order_update = DetailOrderService.objects.filter(id=request.POST[list_serviceid[idx]]).update(user_id=request.POST['user'],service_id=request.POST[list_service[idx]],time=request.POST[list_time[idx]],note=request.POST[list_note[idx]])
                    
            elif (len(list_service) > 0) and (len(list_service_order_old) < len(list_service)): # Thêm hàng dịch vụ: Xóa dịch vụ cũ và Thêm list dịch vụ theo order_id
                list_service_order_old.delete()
                for idx,i in enumerate(list_service):
                    if request.POST[i] != "":
                        data_service_create = DetailOrderService.objects.create(user_id=request.POST['user'],order_id=id,service_id=request.POST[list_service[idx]],time=request.POST[list_time[idx]],note=request.POST[list_note[idx]])
            
            elif (len(list_service_order_old) > len(list_service)): # Xóa bớt hàng dịch vụ: Xóa dịch vụ cũ và Thêm list dịch vụ theo order_id
                list_service_order_old.delete()
                for idx,i in enumerate(list_service):
                    if request.POST[i] != "":
                        data_service_create = DetailOrderService.objects.create(user_id=request.POST['user'],order_id=id,service_id=request.POST[list_service[idx]],time=request.POST[list_time[idx]],note=request.POST[list_note[idx]])
            
            fs = FileSystemStorage()

            # xoa anh cu
            # data_file_old = FileOrder.objects.filter(img_order_id=id)
            # for i_file in data_file_old:
            #     if i_file.file_before != "":
            #         name_file_before = str(i_file.file_before.name).split("\\")[-1]
            #         if os.path.isfile("media/" +name_file_before):
            #             os.remove("media/" +name_file_before)
            #     if i_file.file_after != "":
            #         name_file_after = str(i_file.file_after.name).split("\\")[-1]
            #         if os.path.isfile("media/" +name_file_after):
            #             os.remove("media/" +name_file_after)

            #     i_file.delete()
            # data_file_old.delete()

            # file anh truoc dieu tri
            list_file_before = request.FILES.getlist('file_before[]')
            for i_file_before in list_file_before:
                new_name_before = "update_before_"+ str(id) +"_"+ unidecode(str(request.POST['customer']).replace(' ','-')) + "_"+ datetime.datetime.now().strftime("%Y%m%d%H%M%S") +"."+ str(i_file_before.name).split('.')[-1]
                file_save_before = fs.save(new_name_before, i_file_before)
                FileOrder.objects.create(file_before="media\\"+file_save_before, img_order_id = get_data_order.pk)

            # file anh sau dieu tri
            list_file_after = request.FILES.getlist('file_after[]')
            for i_file_after in list_file_after:
                new_name_after = "update_after_"+ str(id) +"_"+ unidecode(str(request.POST['customer']).replace(' ','-')) + "_"+ datetime.datetime.now().strftime("%Y%m%d%H%M%S") +"."+ str(i_file_after.name).split('.')[-1]
                file_save_after = fs.save(new_name_after, i_file_after)
                FileOrder.objects.create(file_after="media\\"+file_save_after, img_order_id = get_data_order.id)

            messages.success(request, 'Cập nhật đơn kê thành công!')
            return redirect('manage_order')

        except Exception as e:
            print(e)
            HttpResponse('Cập nhật kê thất bại!, Vui lòng kiểm tra lại')


class DeleteOrderView(View):
    def get(self,request,id):
        orders = get_object_or_404(Order, pk=id)
        datacustomer = orders.customer.id
        # print(datacustomer)
        
        context = {
            'id_order': orders.pk,
            'full_name': orders.customer.full_name,
            'user': orders.user.username,
            'numberphone':orders.customer.numberphone,
            'email':orders.customer.email,
            }
        return JsonResponse(
                {
                'type': 'success',
                'data_order':context
                },safe=True)
    def post(self,request,id):
        try:
            data_order_delete = get_object_or_404(Order, pk=id)
            # data_order_delete = Order.objects.filter(id=id).delete()

            data_file = FileOrder.objects.filter(img_order_id=id)
            # print(len(data_file))
            for i_file in data_file:
                if i_file.file_before != "":
                    name_file_before = str(i_file.file_before.name).split("\\")[-1]
                    if os.path.isfile("media/" +name_file_before):
                        os.remove("media/" +name_file_before)

                if i_file.file_after != "":
                    name_file_after = str(i_file.file_after.name).split("\\")[-1]
                    if os.path.isfile("media/" +name_file_after):
                        os.remove("media/" +name_file_after)
                
                i_file.delete()

            data_file.delete()
            data_order_delete.delete()
            return JsonResponse(
                {
                    'type': 'success',
                    'message': 'Xóa đơn kê thành công'
                    }, safe=True)
        except Exception as e:
            return JsonResponse(
                {
                    'type': 'error',
                    'message': 'Lỗi ' + str(e)
                    }, safe=True)
   
@login_required
def ViewOrder(request,id):
    orders = get_object_or_404(Order, pk=id)
    list_order_product = DetailOrderProduct.objects.filter(order_id=orders.pk)
    list_order_service = DetailOrderService.objects.filter(order_id=orders.pk)
    list_img = FileOrder.objects.filter(img_order_id=orders.pk)
    list_before = []
    list_after = []
    for i_img in list_img:
        if i_img.file_before != '':
            list_before.append(i_img.file_before.url)
        if i_img.file_after != '':
            list_after.append(i_img.file_after.url)
            
    context = {
        'id_order': orders.pk,
        'orders': orders,
        'list_order_product':list_order_product,
        'list_order_service':list_order_service,
        'list_before':list_before,
        'list_after':list_after,
        }
    return render(request, 'order/view_order.html', context) 

@login_required
def Home_Export_Excel1(request):
    if request.method == 'POST':

        data_Order = Order.objects.filter(id=request.POST.get('id'))


        if len(data_Order) == 0:
            response_data = {}
            response_data["message"] = 'notexist'
            return HttpResponse(json.dumps(response_data), content_type="application/json")



        # qs_QC = qs_Master_Products.values_list('product_code','exchange')

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        strNgay = str(data_Order[0].created_at).split(' ')[0]
        try:
            strTaiKham = str(data_Order[0].day_re_examination).split(' ')[0]
        except:
            strTaiKham = ''

        strTenKH = str(data_Order[0].customer.full_name)
        strTenCho = str(data_Order[0].customer.numberphone)
        try:
            strBenhly = str(data_Order[0].pathological)
        except:
            strBenhly = ' '
        
        date_order_code = str("date_filter").replace('-','')
        strSoPhieu = str(data_Order[0].pk).zfill(6)
        strNhanvien = str(data_Order[0].user.full_name())
        #format
        # title= workbook.add_format({'bold': True,'font_size':16,'align': 'center','font':'Arial'})
        bold = workbook.add_format({'bold': True,'font_size':16,'font':'Arial'})
        normal = workbook.add_format({'font_size':16,'font':'Arial'})
        centeralign = workbook.add_format({'font_size':16,'font':'Arial','bold':True})
        centeralign.set_align('top')
        italic = workbook.add_format({'font_size':16,'font':'Arial','italic':True})
        # Add a number format for cells with money.
        money = workbook.add_format({'num_format': '#,##0 ','border': 1,'font':'Arial'})
        money1 = workbook.add_format({'num_format': '#,##0 ','font':'Arial'})
        header_format = workbook.add_format({'bold': True,'border': 1,'font_size':16,'font':'Arial','align': 'center'})
        cell_format = workbook.add_format({'border': 1,'text_wrap':True,'font_size':16,'font':'Arial'})
        cell_format2 = workbook.add_format({'border': 1,'text_wrap':True,'font_size':16,'font':'Arial','align': 'center'})

        worksheet = workbook.add_worksheet()
        worksheet.merge_range('A1:G1', "Cecilia Spa", workbook.add_format({'bold': True,'font_size':16,'align': 'center','font':'Arial'}))
        worksheet.merge_range('A2:G2', "Số 297/21, Đường Trường Chinh, Thanh Khê, Đà Nẵng", workbook.add_format({'font_size':16,'align': 'center','font':'Arial'}))
        worksheet.merge_range('A3:G3', "SDT: 0965284848 - Website: https://ceciliaspa.vn/ ", workbook.add_format({'font_size':16,'align': 'center','font':'Arial'}))
        worksheet.merge_range('I1:K1', "ĐƠN LIỆU TRÌNH", workbook.add_format({'bold': True,'font_size':16,'align': 'center','font':'Arial'}))


        worksheet.write('I2', "Ngày",italic)
        worksheet.write('J2', strNgay,italic)

        worksheet.write('B5', "Tên khách hàng:",bold)
        worksheet.write('B6', "Số điện thoại:",bold)
        worksheet.write('B7', "Bệnh lý:",bold)

        worksheet.write('I3', "Số đơn:",bold)
        worksheet.write('I4', "Nhân viên:",bold)
        worksheet.write('I6', "Tái khám:",bold)
        worksheet.write('C5', strTenKH,normal)
        worksheet.write('C6', strTenCho,normal)
        worksheet.write('C7', strBenhly,normal)
        worksheet.write('J3', strSoPhieu,normal)
        worksheet.write('J4', strNhanvien,normal)
        worksheet.write('J6', strTaiKham,normal)
        col_product = 0
        row_product = 10
        col_service = 6
        row_service = 10

        intStt = 1
        strTongtien = 0
        for i_Order in data_Order:
            data_DetailOrderProduct =  DetailOrderProduct.objects.filter(order=i_Order.id)
            data_DetailOrderService =  DetailOrderService.objects.filter(order=i_Order.id)
            # print(len(data_DetailOrderProduct))
            # print(len(data_DetailOrderService))


            if len(data_DetailOrderProduct) != 0:
                worksheet.merge_range('B9:B10', "NGÀY", header_format)
                worksheet.merge_range('C9:C10', "BUỔI", header_format)
                worksheet.merge_range('D9:D10', "ROUTINE", header_format)
                worksheet.merge_range('E9:E10', "LƯU Ý", header_format)
                list_day = set([i.day for i in data_DetailOrderProduct])

                for i_day in list_day:
                    int_row_day = 0
                    list_day_row = []
                    for i_DetailOrderProduct in data_DetailOrderProduct:
                        if i_day == i_DetailOrderProduct.day:
                            list_day_row.append(i_DetailOrderProduct)
                    
                    list_buoi = set([i.buoi for i in list_day_row])
            
                    for i_buoi in list_buoi:
                        for i_day_row in list_day_row:
                            str_product_note = ''
                            if i_buoi == i_day_row.buoi:
                                if i_day_row.day == None:
                                    str_day_row = None
                                elif i_day_row.day != None:
                                    str_day_row = i_day_row.day
                                if i_day_row.buoi == None:
                                    str_buoi = None
                                elif i_day_row.buoi != None:
                                    str_buoi = i_day_row.buoi
                                if i_day_row.product == None:
                                    str_product = None
                                elif i_day_row.product != None:
                                    str_product = i_day_row.product
                                    if i_day_row.product.note == None:
                                        str_product_note = None
                                    elif i_day_row.product.note != None:
                                        str_product_note = i_day_row.product.note
                                
                                    
                                worksheet.write_string(row_product,col_product+1, str(str_day_row),cell_format)
                                worksheet.write_string(row_product,col_product+2, str(str_buoi),cell_format)                        
                                worksheet.write_string(row_product,col_product+3, str(str_product),cell_format)
                                worksheet.write_string(row_product,col_product+4, str(str_product_note),cell_format)
                                row_product+=1
    
                
            if len(data_DetailOrderService) != 0:
                worksheet.merge_range('H9:H10', "DỊCH VỤ", header_format)
                worksheet.merge_range('I9:I10', "THỜI GIAN", header_format)
                worksheet.merge_range('J9:J10', "LƯU Ý", header_format)
                for i_DetailOrderService in data_DetailOrderService:
                    if i_DetailOrderService.service == None:
                        str_service = None
                    elif i_DetailOrderService.service != None:
                        str_service = i_DetailOrderService.service
                    if i_DetailOrderService.time == None:
                        str_time = None
                    elif i_DetailOrderService.time != None:
                        str_time = i_DetailOrderService.time
                    if i_DetailOrderService.note == None:
                        str_note = None
                    elif i_DetailOrderService.note != None:
                        str_note = i_DetailOrderService.note
                        
                    worksheet.write_string(row_service,col_service+1, str(str_service),cell_format)
                    worksheet.write_string(row_service,col_service+2, str(str_time),cell_format)                        
                    worksheet.write_string(row_service,col_service+3, str(str_note),cell_format)
                    row_service+=1

            if i_Order.use_to == None:
                str_userto = ''
            elif i_Order.use_to != None:
                str_userto = i_Order.use_to
            if i_Order.detail_caleder_examination == None:
                str_detail = ''
            elif i_Order.detail_caleder_examination != None:
                str_detail = i_Order.detail_caleder_examination

            worksheet.write_string(row_product+2,col_product+1, "Cách sử dụng: ",bold)
            worksheet.write_string(row_product+2,col_product+2, str(str_userto),cell_format)

            worksheet.write_string(row_product+4,col_product+1, "Chi tiết lịch khám: ",bold)
            worksheet.write_string(row_product+4,col_product+2, str(str_detail),cell_format)
        
        worksheet.set_column('A:A', 5) # STT
        worksheet.set_column('B:B', 25)
        worksheet.set_column('C:C', 25) # Tên SP
        worksheet.set_column('D:D', 30) # DVT
        worksheet.set_column('E:E', 35) # QC
        worksheet.set_column('F:F', 2) # Số lượng sỉ
        worksheet.set_column('G:G', 2) # Số lượng lẻ
        worksheet.set_column('H:H', 25) # DG sỉ
        worksheet.set_column('I:I', 15) # DG lẻ
        worksheet.set_column('J:J', 30) # Thành tiền
        worksheet.set_column('K:K', 5)
        # worksheet.set_column('C:F', 13)
        worksheet.set_row(0, 20)
        pages_horz = 1
        pages_vert = 0
        worksheet.fit_to_pages(pages_horz,pages_vert)
        worksheet.set_margins(left=0.6,right=0.6,top=0.3,bottom=0.1)
        worksheet.set_landscape()
        workbook.close()
        # print(settings.BASE_DIR)
        path_folder = str(settings.BASE_DIR) + "/core/static/Export_File/export_excel_home/" + datetime.datetime.now().strftime("%Y%m%d")
        if not os.path.exists(path_folder):
            os.makedirs(path_folder)
        name_file = str(data_Order[0].id)+"_"+unidecode(str(data_Order[0].customer.full_name).replace(' ','-'))+'_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.xlsx'
        with open(path_folder + '/' + name_file,'wb') as static_file:
            static_file.write(output.getvalue())
        response_data = {}
        response_data["message"] = 'success'
        response_data["Path_File"] = '/static/Export_File/export_excel_home/' + datetime.datetime.now().strftime("%Y%m%d") + '/' + name_file
        # qs_Order.update(status_print=2)
        return HttpResponse(json.dumps(response_data), content_type="application/json")