from django.shortcuts import HttpResponse

from django.shortcuts import redirect, render
from django.views import View
from core.models import *


class HomeView(View):
    def get(self,request):
        if request.user.is_authenticated == False:
            return render(request, 'auth/login.html', {})
        else:
            if request.user.is_superuser:
                count_product = Product.objects.all().count()
                count_customer = Customer.objects.all().count()
                count_service = Service.objects.all().count()
                count_order = Order.objects.all().count()
                context = {
                    'count_product':count_product,
                    'count_customer':count_customer,
                    'count_service':count_service,
                    'count_order':count_order,
                    'room_name': "broadcast"

                }
                return render(request, 'home/index.html',context)
            else:
                id =  request.user.id
                count_customer = Customer.objects.filter(user_id=id).count()
                count_order = Order.objects.filter(user_id=id).count()
                context = {
                    'count_customer':count_customer,
                    'count_order':count_order,
                    'room_name': "broadcast"

                }
                return render(request, 'home/index.html',context)


