from  django.shortcuts import redirect, render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login as log_in, logout
from django.contrib.auth.hashers import check_password, make_password
from core.models import UserAccount
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import re #thư viện biểu thức chính quy

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return render(request, 'auth/login.html', {})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        next_url = request.POST.get('next', '')
        
        user = authenticate(username=username, password=password)

        # user =  authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_lock:
                context = {
                    'message': 'Tài khoản của bạn tạm thời đã bị khóa, vui lòng liên hệ Admin để được hỗ trợ. Xin cảm ơn!'
                }
                return render(request, 'auth/login.html', context)

            log_in(request, user)
            if next_url :
                return HttpResponseRedirect(next_url)
            else:
                return redirect('home')
                
        else:
            context = {
                'message' : 'Thông tin tài khoản hoặc mật khẩu không đúng !!'
            }
            return render(request, 'auth/login.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/login')

@login_required(login_url='/login')
# decorator được sử dụng để bảo vệ một view 
# khỏi việc được truy cập bởi người dùng chưa đăng nhập.
def ChangePasswordView(request):
    #check dữ liệu đầu vào
    #xác nhận mật khẩu mới khớp, đúng định dạng
        if request.method == 'POST':
            passwordold = request.POST.get('password', '')
            passwordnew = request.POST.get('password1', '')
            passwordnewrepeat = request.POST.get('password2', '')
            if passwordold == '' or passwordnew == '' or passwordnewrepeat == '' :
                # messages.error(request,'Trường yêu cầu không được bỏ trống!')
                context = {
                            'Trường yêu cầu không được bỏ trống!',
                        }
            else:
                if passwordnew != passwordnewrepeat :
                    # messages.error(request,'Mật khẩu nhập lại không trùng khớp!')
                    context = {
                                'message':'Mật khẩu nhập lại không trùng khớp!',
                        }
                else:
                    # biểu thức chính quy để định dạng mật khẩu
                    if re.match(r'(?=.{8})(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[!@#$%^&*])', passwordnew):
                        # no match
                        if (request.user.check_password(passwordold)):
                            #check pass_old và pass_new
                            UserAccount.objects.filter(id=request.user.id).update(password=make_password(passwordnew))
                            # messages.success(request, 'Mật khẩu đã được thay đổi thành công')
                            context = {
                                'message':'Mật khẩu đã được thay đổi thành công',
                            }
                            
                        else:
                            # messages.error(request,'Mật khẩu cũ chưa chính xác!')
                            context = {
                                    'message':'Mật khẩu cũ chưa chính xác!',
                                }
                    else:
                        # messages.error(request,'Mật khẩu không đúng định dạng yêu cầu!')
                        context = {
                            'message':"Mật khẩu phải có 8 kí tự gồm chữ hoa, thường, số, kí tự đặc biệt!",
                        }
            return render(request, 'auth/change_password.html',context)
            # return JsonResponse(
            #     {'message_success' : message_success,
            #     'message_error' : message_error
            #     },safe=False)
        else:
            return render(request, 'auth/change_password.html',)
# django.contrib.auth xác thực mật khẩu ở model 
# class-based view và hàm xác thực xử lý mật khẩu
# tbao phản hồi qua context khi render template



