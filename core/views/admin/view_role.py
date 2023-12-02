# from django.contrib import messages
# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import redirect, render
# from django.views import View
# # from core.models import Permission, Role, User
# from django.contrib.auth.decorators import login_required
# import json
# from django.core import serializers
# from django.shortcuts import get_object_or_404
# from django.http import Http404

# class ManageRoleView(View):
#     def get(self, request):
#         if request.user.is_superuser:
#             list_role = Role.objects.all()
#             list_per = Permission.objects.all()
#             context = {
#                 'list_role':list_role,
#                 'list_per':list_per,
#             }
#             return render(request, 'admin/admin_role.html',context)
#         else:
#             return HttpResponse("Bạn không có quyền truy cập vào đây.")

#     def post(self, request):
#         if request.user.is_superuser:
#             name_role = str(request.POST['name']).strip()
#             num_level = str(request.POST['level']).strip() 
#             str_description = request.POST['description']
#             list_per = request.POST.getlist('permission[]')
#             if name_role == '':
#                 return JsonResponse(
#                     {
#                         'type': 'error',
#                         'message': 'Lỗi thiếu thông tin bắt buộc: Tên vai trò',
#                         }, safe=True)
#             elif num_level == '':
#                 return JsonResponse(
#                     {
#                         'type': 'error',
#                         'message': 'Lỗi thiếu thông tin bắt buộc: Bậc',
#                         }, safe=True)
#             elif len(list_per) == 0:
#                 return JsonResponse(
#                     {
#                         'type': 'error',
#                         'message': 'Lỗi thiếu thông tin bắt buộc: Quyền',
#                         }, safe=True)
#             else:
#                 if Role.objects.filter(name=name_role, ).exists():
#                     return JsonResponse(
#                         {
#                             'type': 'error',
#                             'message': 'Vai trò này đã tồn tại trên hệ thống',
#                             }, safe=True)
#                 else:
#                     createRole = Role.objects.create(name=name_role, level=num_level,description=str_description)
#                     createRole.permission.add(*list_per)
#                     return JsonResponse(
#                         {
#                             'type': 'success',
#                             'message': 'Thêm mới vai trò thành công'
#                             }, safe=True)
            
#         else:
#             return HttpResponse("Bạn không có quyền truy cập vào đây.")
    


# class UpdaeRoleView(View):
#     def get(self,request,id):
#         if request.user.is_superuser:
#             try:
#                 data_role = get_object_or_404(Role, pk=id)
#             except Role.DoesNotExist:
#                 raise Http404("Không tìm thấy dữ liệu phù hợp.")
#             list_per = data_role.permission.all()
#             list_permission =  serializers.serialize('json', list_per)
#             data_json = json.loads(list_permission)
#             list_id_per = [data['pk']  for data in  data_json]
#             list_name_per = [data['fields']['name'] for data in  data_json]
#             role = {
#                 'id':data_role.id,
#                 'name': data_role.name,
#                 'level': data_role.level,
#                 'description': data_role.description,
#                 'list_id_per': list_id_per,
#                 'list_name_per':list_name_per,
#             }
#             # data = json.loads(role)
#             # data = serializers.serialize("json", data_role)
#             return JsonResponse(
#                         {
#                         'type': 'success',
#                         'data_role':role
#                         },safe=True)
#         else:
#             return HttpResponse("Bạn không có quyền truy cập vào đây.")

#     def post(self, request,id):
#         try:
#             data_role = get_object_or_404(Role, pk=id)
#         except Role.DoesNotExist:
#             raise Http404("Không tìm thấy dữ liệu phù hợp.")

#         name_role = str(request.POST['name']).strip()
#         num_level = str(request.POST['level']).strip()
#         data_description = str(request.POST['description']).strip()
#         list_per = request.POST.getlist('permission[]')

#         if name_role == '':
#                 return JsonResponse(
#                     {
#                         'type': 'error',
#                         'message': 'Lỗi thiếu thông tin bắt buộc: Tên vai trò',
#                         }, safe=True)
#         elif num_level == '':
#             return JsonResponse(
#                 {
#                     'type': 'error',
#                     'message': 'Lỗi thiếu thông tin bắt buộc: Bậc',
#                     }, safe=True)
#         elif len(list_per) == 0:
#             return JsonResponse(
#                 {
#                     'type': 'error',
#                     'message': 'Lỗi thiếu thông tin bắt buộc: Quyền',
#                     }, safe=True)
#         else:
#             try:
#                 updaterole = Role.objects.filter(id=id).update(name = name_role, level=num_level, description=data_description)
#                 data_role.permission.clear()
#                 data_role.permission.add(*list_per)
#                 return JsonResponse(
#                     {
#                         'type': 'success',
#                         'message': 'Cập nhập vai trò thành công!'
#                         }, safe=True)
#             except:
#                 return JsonResponse(
#                     {
#                         'type': 'error',
#                         'message': 'Cập nhập vai trò không thành công!'
#                         }, safe=True)

