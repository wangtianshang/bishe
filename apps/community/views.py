from django.shortcuts import render
from django.views.generic.base import View#�������ʽʵ�� ��Ҫ�̳�djang��view
# Create your views here.
class CommunView(View):
    def get(self,request):
        return render(request,'shequ.html')