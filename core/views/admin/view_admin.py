
# from audioop import reverse
# from django.contrib import messages
# from django.http import HttpResponse
# from django.shortcuts import redirect, render
# from django.views import View

# from django.contrib.auth.hashers import make_password

# # from core.models import Permission, Role, User
# from django.contrib.auth.decorators import login_required

# @login_required
# def AddUser(request):
#     if request.user.is_superuser:
#         if request.method == 'POST':
#             username = request.POST['username']
#             email = request.POST['email']
#             phonenumber = request.POST['phonenumber']
#             new_user = User.objects.create(username=username, password=make_password(username), email= email, phonenumber = phonenumber )
#             messages.success(request, 'Thêm User thành công!')
#             return redirect('manageuser')
#         else:
#             return render(request, 'admin/add_user.html')
#     return HttpResponse("Bạn không có quyền truy cập vào đây.")
    

# @login_required
# def EditUser(request, id):
#     if request.user.is_superuser:
#         if request.method == 'GET':
#             print('vào edit')
#             user = User.objects.get(id=id)
#             context = {'user': user}
#             return render(request, 'admin/edit_user.html', context)
#     return HttpResponse("Bạn không có quyền truy cập vào đây.")

# @login_required
# def UpdateUser(request, id):
#     if request.user.is_superuser:
#         if request.method == 'POST':
#             try:
#                 data = User.objects.get(id=id)
#                 data.address = request.POST['address']
#                 data.phonenumber = request.POST['phonenumber']
#                 data.email = request.POST['email']
#                 data.save()
#                 messages.success(request, 'Cập nhật User thành công!')
#                 return redirect(r'/edit/user/'+id)
#             except Exception as e:
#                 print(e)
#                 messages.error(request, 'Cập nhật User không thành công!')
#                 return redirect(r'/edit/user/'+id)
#     return HttpResponse("Bạn không có quyền truy cập vào đây.")
    

# @login_required
# def DeleteUser(request, id):
#     if request.user.is_superuser:
#         member = User.objects.get(id=id)
#         member.delete()
#         messages.error(request, 'Xóa khách hàng thành công!')
#         return redirect('manageuser')
#     return HttpResponse("Bạn không có quyền truy cập vào đây.")
