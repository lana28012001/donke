#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from core.models import Customer, FileProduct, Order, Product, TypeCustommer, TypeStatus, UserAccount
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.files.storage import FileSystemStorage
from core.forms import ProductForm
import os
import locale
locale.setlocale(locale.LC_ALL, "")
from unidecode import unidecode


def ListProduct(request):
    if request.user.is_superuser:
        list_product = Product.objects.all().order_by('-id')

        # id_user =  request.user.id
        # list_product = Product.objects.filter(user_id=id_user).order_by('-id')
        dict_img = {}
        for i_pro in list_product:
            list_img = []
            list_data_img = FileProduct.objects.filter(file_product_id=i_pro.id)
            # print(len(list_data_img))
            for i_img in list_data_img:
                if i_img.images_product != '':
                    list_img.append([i_pro.id,i_img.images_product])

            if len(list_img) > 0:
                dict_img[i_pro.id] = list_img

        # paginator = Paginator(customer_list, 10)
        # page = request.GET.get('page')
        # try:
        #     customers = paginator.page(page)
        # except PageNotAnInteger:
        #     customers = paginator.page(1)
        # except EmptyPage:
        #     customers = paginator.page(paginator.num_pages)

        context = {
            'list_product':list_product,
            'dict_img':dict_img
        }
        return render(request, 'product/list_product.html', context)
    
    return HttpResponse("Bạn không có quyền truy cập vào đây.")
        
def AddProduct(request):
    if  request.method == 'GET':
        return render(request, 'product/add_product.html')

    elif request.method == 'POST':
        form_product = ProductForm(request.POST)
        list_file_product = request.FILES.getlist('images_product[]')
        if form_product.is_valid():
            # process form data
            data_product = form_product.save()
            fs = FileSystemStorage()
            # list_file_acept = []
            for i_file in list_file_product:
                if str(i_file.name).endswith(".svg") or str(i_file.name).endswith(".png") or str(i_file.name).endswith(".jpg") or str(i_file.name).endswith(".jpeg"):
                    new_name = "add_product_"+ unidecode(str(form_product.cleaned_data['product']).replace(' ','-')) + "_"+ datetime.datetime.now().strftime("%Y%m%d%H%M%S") +"."+ str(i_file.name).split('.')[-1]
                    file_name_save = fs.save(new_name, i_file)
                    
                    FileProduct.objects.create(images_product="media\\"+file_name_save, file_product_id = data_product.pk)
            messages.success(request, 'Thêm sản phẩm thành công')
            return redirect('manage_product')
        else:
            list_err =[]
            list_erro = form_product.errors
            for key,values in list_erro.items():
                list_err.append("Lỗi: "+ key +  " "+ str(values[0]))
            return render(request, 'product/add_product.html', {
                'messages': list_err,
            })


def UpdateProduct(request,id):
    if  request.method == 'GET':
        data = get_object_or_404(Product, pk=id)
        list_data_img = []
        list_img = FileProduct.objects.filter(file_product_id=data.id)
        for img in list_img:
            # print(img.images_product)
            if img.images_product != "":
                list_data_img.append(img.images_product)
        context = {
            'id_product':data.id,
            'product': data.product,
            'price': data.price,
            'function': data.function,
            'dosage': data.dosage,
            'keyword': data.keyword,
            'estimate': data.estimate,
            'note': data.note,
            'list_img':list_data_img
        }
        return render(request, 'product/update_product.html', context)

    elif  request.method == 'POST':
        
        get_data_product = get_object_or_404(Product, pk=id)
        form = ProductForm(request.POST, instance=get_data_product)
        if form.is_valid():
            form.save()
            fs = FileSystemStorage()

            data_file_old = FileProduct.objects.filter(file_product_id=id)
            for i_file in data_file_old:
                name_file = str(i_file.images_product.name).split("\\")[-1]
                if os.path.isfile("media/" +name_file):
                    os.remove("media/" +name_file)

                i_file.delete()
            data_file_old.delete()

            list_file_update = request.FILES.getlist('images_product[]')
            for indx, i_file in enumerate(list_file_update):
                if str(i_file.name).endswith(".svg") or str(i_file.name).endswith(".png") or str(i_file.name).endswith(".jpg") or str(i_file.name).endswith(".jpeg"):
                    # name = unidecode(str(form.cleaned_data['product']).replace(' ','-'))
                    new_name = "update_product_"+ str(id) +"_"+ unidecode(str(form.cleaned_data['product']).replace(' ','-')) + "_"+ datetime.datetime.now().strftime("%Y%m%d%H%M%S") +"."+ str(i_file.name).split('.')[-1]
                    
                    file_new_save = fs.save(new_name, i_file)
                    FileProduct.objects.create(images_product="media\\"+file_new_save, file_product_id = get_data_product.pk)

            messages.success(request, 'Cập nhật sản phẩm thành công!')
            return redirect('manage_product')
        else:
            list_err =[]
            list_form_erro = form.errors
            for key,values in list_form_erro.items():
                list_err.append("Lỗi: "+ key +  " "+ str(values[0]))

            return render(request, 'product/update_product.html', 
            {
                'messages': list_err,
                'id_product':id,
            })

class DeleteProductView(View):
    def get(self,request,id):
        data = get_object_or_404(Product, pk=id)
        data_product = {
            'id':data.id,
            'product': data.product,
            'function': data.function,
            'dosage': data.dosage,
            'note': data.note,
        }
        return JsonResponse(
                {
                'type': 'success',
                'data_product':data_product
                },safe=True)

    def post(self,request,id):
        try:
            data_product = get_object_or_404(Product, pk=id)
            
            data_file = FileProduct.objects.filter(file_product_id=id)
            # print(len(data_file))
            for i_file in data_file:
                name_file = str(i_file.images_product.name).split("\\")[-1]
                if os.path.isfile("media/" +name_file):
                    print(name_file)
                    os.remove("media/" +name_file)

                i_file.delete()
            data_file.delete()

            data_product.delete()
            return JsonResponse(
                {
                    'type': 'success',
                    'message': 'Xóa sản phẩm thành công'
                    }, safe=True)
        except Exception as e:
            return JsonResponse(
                {
                    'type': 'error',
                    'message': 'Lỗi ' + str(e)
                    }, safe=True)
        

