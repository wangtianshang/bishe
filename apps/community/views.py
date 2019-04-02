from django.shortcuts import render
from django.views.generic.base import View#以类的形式实现 需要继承djang的view
# Create your views here.
class CommunView(View):
    def get(self,request):
        return render(request,'shequ.html')