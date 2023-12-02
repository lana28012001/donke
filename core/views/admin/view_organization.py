# from django.contrib import messages
# from django.http import Http404, HttpResponse, JsonResponse
# from django.shortcuts import get_object_or_404, redirect, render
# # from django.shortcuts import render_to_response
# from django.views import View
# # from core.models import Group, Permission, Role, Organization, User
# from django.contrib.auth.decorators import login_required
# from django.core import serializers
# import json


# class ManageOrganizationView(View):
#     def get(self, request):
#         if request.user.is_superuser:
#             list_organization = Organization.objects.all()
#             list_group = Group.objects.all()
#             context = {
#                 'list_organization':list_organization,
#                 'list_group':list_group,
#             }
#             return render(request, 'admin/admin_organization.html',context)
#         else:
#             return HttpResponse("Bạn không có quyền truy cập vào đây.")

#     def post(self, request):
#         if request.user.is_superuser:
#             data_name = str(request.POST['name']).strip() 
#             data_code = str(request.POST['code']).strip()
#             data_group = request.POST['group']
#             data_sign_site = str(request.POST['sign_site']).strip()
#             data_address = str(request.POST['address']).strip()
#             data_number_phone = str(request.POST['number_phone']).strip()
#             data_note = str(request.POST['note']).strip()
#             data_code = str(data_code).strip()
#             if data_name == "":
#                 return JsonResponse(
#                     {
#                         'type': 'error',
#                         'message': 'Lỗi thiếu thông tin bắt buộc: Mã đơn vị',
#                         }, safe=True)
#             elif data_code == "":
#                 return JsonResponse(
#                     {
#                         'type': 'error',
#                         'message': 'Lỗi thiếu thông tin bắt buộc: Tên đơn vị',
#                         }, safe=True)
#             else:
#                 if Organization.objects.filter(name=data_name, ).exists():
#                     return JsonResponse(
#                         {
#                             'type': 'error',
#                             'message': 'Tên Đơn vị này đã tồn tại trên hệ thống',
#                             }, safe=True)
#                 elif Organization.objects.filter(code=data_code, ).exists():
#                      return JsonResponse(
#                         {
#                             'type': 'error',
#                             'message': 'Mã Đơn vị này đã tồn tại trên hệ thống',
#                             }, safe=True)

#                 else:
#                     if data_number_phone == "":
#                         data_number_phone = None
#                     data = Organization.objects.create(code=data_code,name=data_name,group_id=data_group,sign_site=data_sign_site,address=data_address,number_phone=data_number_phone,note=data_note)
#                     return JsonResponse(
#                         {
#                             'type': 'success',
#                             'message': 'Thêm mới đơn vị thành công'
#                             }, safe=True)
                    
            
#         else:
#             return HttpResponse("Bạn không có quyền truy cập vào đây.")
    

# class UpdaeOrganizationView(View):
#     def get(self,request,id):
#         if request.user.is_superuser:
#             data = get_object_or_404(Organization, pk=id)
#             if data.group == None:
#                 id_group = None
#                 name_group = None
#             else:
#                 id_group = data.group.id
#                 name_group = data.group.name

#             site = {
#                 'id':data.id,
#                 'name': data.name,
#                 'code': data.code,
#                 'sign_site': data.sign_site,
#                 'address': data.address,
#                 'number_phone': data.number_phone,
#                 'note': data.note,
#                 'id_group': id_group,
#                 'name_group':name_group,
#             }
#             return JsonResponse(
#                         {
#                         'type': 'success',
#                         'data_organization':site
#                         },safe=True)
#         else:
#             return HttpResponse("Bạn không có quyền truy cập vào đây.")

#     def post(self, request,id):
#         try:
#             data_role = get_object_or_404(Organization, pk=id)
#         except Organization.DoesNotExist:
#             raise Http404("Không tìm thấy dữ liệu phù hợp.")

#         data_name = str(request.POST['name']).strip()
#         data_code = str(request.POST['code']).strip()
#         data_sign_site = str(request.POST['sign_site']).strip()
#         data_address = str(request.POST['address']).strip()
#         data_number_phone = str(request.POST['number_phone']).strip()
#         data_note = str(request.POST['note']).strip()
#         data_group = str(request.POST['group']).strip()

#         if data_code == "":
#             return JsonResponse(
#                 {
#                     'type': 'error',
#                     'message': 'Lỗi thiếu thông tin bắt buộc:Mã đơn vị',
#                     }, safe=True)
#         elif data_name == "":
#             return JsonResponse(
#                 {
#                     'type': 'error',
#                     'message': 'Lỗi thiếu thông tin bắt buộc:Tên đơn vị',
#                     }, safe=True)
#         else:
#             if data_number_phone == "":
#                 data_number_phone = None
#             updaterole = Organization.objects.filter(id=id).update(name=data_name,code=data_code,group_id=data_group,sign_site=data_sign_site,address=data_address,number_phone=data_number_phone,note=data_note)
#             return JsonResponse(
#                 {
#                     'type': 'success',
#                     'message': 'Cập nhập đơn vị thành công'
#                     }, safe=True)


# class DeleteOrganizationView(View):
#     def get(self,request,id):
#         if request.user.is_superuser:
#             try:
#                 data = get_object_or_404(Organization, pk=id)
#             except Organization.DoesNotExist:
#                 raise Http404("Không tìm thấy dữ liệu phù hợp.")
#             if data.group == None:
#                 id_group = None
#                 name_group = None
#             else:
#                 id_group = data.group.id
#                 name_group = data.group.name

#             site = {
#                 'id':data.id,
#                 'name': data.name,
#                 'code': data.code,
#                 'sign_site': data.sign_site,
#                 'address': data.address,
#                 'number_phone': data.number_phone,
#                 'note': data.note,
#                 'id_group': id_group,
#                 'name_group':name_group,
#             }
#             return JsonResponse(
#                         {
#                         'type': 'success',
#                         'data_organization':site
#                         },safe=True)
#         else:
#             return HttpResponse("Bạn không có quyền truy cập vào đây.")

#     def post(self,request,id):
#         try:
#             data = get_object_or_404(Organization, pk=id)
#         except Organization.DoesNotExist:
#             raise Http404("Không tìm thấy dữ liệu phù hợp.")

#         data.delete()
#         return JsonResponse(
#             {
#                 'type': 'success',
#                 'message': 'Xóa đơn vị thành công'
#                 }, safe=True)


