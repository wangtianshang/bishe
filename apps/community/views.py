from django.shortcuts import render
from django.views.generic.base import View
from .models import Node
#用来制作分页
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
class CommunView(View):
    def get(self,request):
        all_node = Node.objects.all()
        for i in all_node:
            print(i.name)
        return render(request,"shequ.html",{
            'all_node':all_node
        })