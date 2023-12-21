import json
from re import I
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView, 
)
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from core.serializers import NotificationListViewSerializer, DetailOrderProductSerializer
from core.models import Notifications, DetailOrderProduct
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

#Lớp kế thừa từ ListAPIView, hiển thị list noti
class List_Notification(ListAPIView):
    #ktra nguoi dung xac thuc chua
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationListViewSerializer
    filter_backends = (DjangoFilterBackend,)
    #phương thức lọc (có điều kiện) noti của user 
    def get_queryset(self):
        queryset = Notifications.objects.filter(user=self.request.user,is_view=False).order_by('-id')
        # print(len(queryset))
        return queryset

def View_More_Notification(request):
    list_notification = Notifications.objects.filter(user_id=request.user.id).order_by('-id').all()
    #truyền list vào context để use trong template
    context = {
                'list_notification':list_notification
            }
    return render(request, 'notification.html', context)

def Notification_is_sent(request,id):
    if request.method == 'POST':
        try:
            Notifications.objects.filter(id=id).update(is_sent=True)
            return JsonResponse(
                    {
                    'type': 'success',
                    'message':'Đã gửi'
                    },safe=True)
        except:
            return JsonResponse(
                    {
                    'type': 'error',
                    'message':'Không tìm thấy ID'
                    },safe=True)
def Notification_is_view(request,id):
    if request.method == 'POST':
        try:
            Notifications.objects.filter(id=id).update(is_view=True)
            return JsonResponse(
                    {
                    'type': 'success',
                    'message':'Đã xem'
                    },safe=True)
        except:
            return JsonResponse(
                    {
                    'type': 'error',
                    'message':'Không tìm thấy ID'
                    },safe=True)
#decorator xử lí các method post và get
@api_view(['POST','GET'])
#API endpoint với cả method get và post
def ManageNotification(request, pk=None):
    if request.method == 'GET':
        detailOrderProduct = DetailOrderProduct.objects.filter(any_product=False)
        serializer = DetailOrderProductSerializer(detailOrderProduct, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        notification_serializer = NotificationListViewSerializer(data=request.data)
        DetailOrderProduct.objects.filter(id=request.data['idproduct']).update(any_product=True)
        if notification_serializer.is_valid():
            notification_serializer.save()
            return Response(notification_serializer.data)
        return Response(notification_serializer.errors, status=HTTP_400_BAD_REQUEST)

    