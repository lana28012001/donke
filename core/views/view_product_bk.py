
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
import re
from django.core.files.storage import FileSystemStorage

class ProductView(View):
    def get(self, request):
        if request.user.is_superuser:
            list_product = Product.objects.all().order_by('-id')
            # paginator = Paginator(customer_list, 10)
            # page = request.GET.get('page')
            # try:
            #     customers = paginator.page(page)
            # except PageNotAnInteger:
            #     customers = paginator.page(1)
            # except EmptyPage:
            #     customers = paginator.page(paginator.num_pages)

            context = {
                'list_product':list_product
            }
            return render(request, 'product.html', context)
        
        return HttpResponse("Bạn không có quyền truy cập vào đây.")
        
    def post(self,request):
        
        product = str(request.POST['product']).strip()
        price = str(request.POST['price']).strip()
        # fit = str(request.POST['fit']).strip()
        # compare = str(request.POST['compare']).strip()
        function = str(request.POST['function']).strip()
        dosage = str(request.POST['dosage']).strip()
        keyword = str(request.POST['keyword']).strip() 
        estimate = str(request.POST['estimate']).strip()
        note = str(request.POST['note']).strip()
        list_file_product = request.FILES.getlist('images_product[]')
        
        if (product == '') or (price == '') or (function == '') or (dosage == '') or (keyword == '') or (estimate == '') or (note == ''):
            return JsonResponse(
                {
                    'type': 'error',
                    'message': 'Lỗi thiếu thông tin bắt buộc: Tên sản phẩm, Giá, Phù hợp da, So sánh, Công dụng, Tần suất sử dụng, Từ khóa Routine, Ước lượng sử dụng, Lưu ý',
                    }, safe=True)

        elif (product != "") and (Product.objects.filter(product=product).exists() == True):
            return JsonResponse(
            {
                'type': 'error',
                'message': 'Tên sản phẩm này đã tồn tại.',
                }, safe=True)

        else:
            try:
                createpro = Product.objects.create(product=product,price=price,function=function,dosage=dosage,keyword=keyword,estimate=estimate,note=note)
                fs = FileSystemStorage()
                for indx, i_file in enumerate(list_file_product):
                    filename = fs.save(i_file.name, i_file)
                    FileProduct.objects.create(images_product="media\\"+filename, file_product = createpro.pk)

                return JsonResponse(
                        {
                            'type': 'success',
                            'message': 'Thêm mới sản phẩm thành công'
                            }, safe=True)
            except Exception as e:
                return JsonResponse(
                        {
                        'type': 'error',
                        'message': 'Lỗi' + str(e)
                        },safe=True)
        
        
class UpdateProductView(View):
    def get(self,request,id):
        data = get_object_or_404(Product, pk=id)
        
        data_product = {
            'id':data.id,
            'product': data.product,
            'price': data.price,
            # 'fit': data.fit,
            # 'compare': data.compare,
            'function': data.function,
            'dosage': data.dosage,
            'keyword': data.keyword,
            'estimate': data.estimate,
            'note': data.note,
        }
        return JsonResponse(
                {
                'type': 'success',
                'data_product':data_product
                },safe=True)
        
    def post(self,request,id):
        data_cu = get_object_or_404(Product, pk=id)
        product = str(request.POST['product']).strip()
        price = str(request.POST['price']).strip()
        # fit = str(request.POST['fit']).strip()
        # compare = str(request.POST['compare']).strip()
        function = str(request.POST['function']).strip()
        dosage = str(request.POST['dosage']).strip()
        keyword = str(request.POST['keyword']).strip() 
        estimate = str(request.POST['estimate']).strip()
        note = str(request.POST['note']).strip()

        if (product == '') or (price == '') or (function == '') or (dosage == '') or (keyword == '') or (estimate == '') or (note == ''):
            return JsonResponse(
                {
                    'type': 'error',
                    'message': 'Lỗi thiếu thông tin bắt buộc: Tên sản phẩm, Giá, Phù hợp da, So sánh, Công dụng, Tần suất sử dụng, Từ khóa Routine, Ước lượng sử dụng, Lưu ý',
                    }, safe=True)
        else:
            try:
                # id_user = request.user.id
                update = Product.objects.filter(id=id).update(product=product,price=price,function=function,dosage=dosage,keyword=keyword,estimate=estimate,note=note)
                return JsonResponse(
                    {
                        'type': 'success',
                        'message': 'Cập nhập sản phẩm thành công'
                        }, safe=True)
            except Exception as e:
                return JsonResponse(
                    {
                    'type': 'error',
                    'message': 'Lỗi ' + str(e)
                    },safe=True)

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
            data = get_object_or_404(Product, pk=id)
            data.delete()
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
        

