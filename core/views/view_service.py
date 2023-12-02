
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from core.models import Customer, Order, Product, Service, TypeCustommer, TypeStatus, UserAccount
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import re

class ServiceView(View):
    def get(self, request):
        if request.user.is_superuser:
            list_service = Service.objects.all().order_by('-id')
            # paginator = Paginator(customer_list, 10)
            # page = request.GET.get('page')
            # try:
            #     customers = paginator.page(page)
            # except PageNotAnInteger:
            #     customers = paginator.page(1)
            # except EmptyPage:
            #     customers = paginator.page(paginator.num_pages)

            context = {
                'list_service':list_service
            }
            return render(request, 'service.html', context)
        
        return HttpResponse("Bạn không có quyền truy cập vào đây.")
        
    def post(self,request):
        if request.user.is_superuser:
            service = str(request.POST['service']).strip()
            function = str(request.POST['function']).strip() 
            note = str(request.POST['note']).strip()
            
            if (service == '') or (function == '') or (note == ''):
                return JsonResponse(
                    {
                        'type': 'error',
                        'message': 'Lỗi thiếu thông tin bắt buộc: Tên dịch vụ, tác dụng, lưu ý',
                        }, safe=True)

            elif (service != "") and (Service.objects.filter(service=service).exists() == True):
                return JsonResponse(
                {
                    'type': 'error',
                    'message': 'Tên dịch vụ này đã tồn tại.',
                    }, safe=True)

            else:
                try:
                    create_ser = Service.objects.create(service=service,function=function,note=note)
                    return JsonResponse(
                        {
                            'type': 'success',
                            'message': 'Thêm mới dịch vụ thành công'
                            }, safe=True)
                except Exception as e:
                    return JsonResponse(
                            {
                            'type': 'error',
                            'message': 'Lỗi ' + str(e)
                            },safe=True)

        return HttpResponse("Bạn không có quyền truy cập vào đây.")
        
        
class UpdateServiceView(View):
    def get(self,request,id):
        if request.user.is_superuser:
            data = get_object_or_404(Service, pk=id)
            
            data_service = {
                'id':data.id,
                'service': data.service,
                'function': data.function,
                'note': data.note,
            }
            return JsonResponse(
                    {
                    'type': 'success',
                    'data_service':data_service
                    },safe=True)
        return HttpResponse("Bạn không có quyền truy cập vào đây.")
            
    def post(self,request,id):
        if request.user.is_superuser:
            data_se = get_object_or_404(Service, pk=id)
            service = str(request.POST['service']).strip()
            function = str(request.POST['function']).strip() 
            note = str(request.POST['note']).strip()

            if (service == '') or (function == '') or (note == ''):
                    return JsonResponse(
                        {
                            'type': 'error',
                            'message': 'Lỗi thiếu thông tin bắt buộc: Tên dịch vụ, tác dụng, lưu ý',
                            }, safe=True)

            
            else:
                try:
                    id_user = request.user.id
                    update = Service.objects.filter(id=id).update(service=service,function=function,note=note)
                    return JsonResponse(
                        {
                            'type': 'success',
                            'message': 'Cập nhập dịch vụ thành công'
                            }, safe=True)
                except Exception as e:
                    return JsonResponse(
                        {
                        'type': 'error',
                        'message': 'Lỗi ' + str(e)
                        },safe=True)
        return HttpResponse("Bạn không có quyền truy cập vào đây.")


class DeleteServiceView(View):
    def get(self,request,id):
        if request.user.is_superuser:
            data = get_object_or_404(Service, pk=id)
            data_service = {
                'id':data.id,
                'service': data.service,
                'function': data.function,
                'note': data.note,
            }
            return JsonResponse(
                    {
                    'type': 'success',
                    'data_service':data_service
                    },safe=True)
        return HttpResponse("Bạn không có quyền truy cập vào đây.")

    def post(self,request,id):
        if request.user.is_superuser:
            try:
                data = get_object_or_404(Service, pk=id)
                data.delete()
                return JsonResponse(
                    {
                        'type': 'success',
                        'message': 'Xóa dịch vụ thành công'
                        }, safe=True)
            except Exception as e:
                return JsonResponse(
                    {
                        'type': 'error',
                        'message': 'Lỗi ' + str(e)
                        }, safe=True)
        
        return HttpResponse("Bạn không có quyền truy cập vào đây.")

