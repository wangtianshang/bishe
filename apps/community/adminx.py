import xadmin
from .models import Node,Topic

class NodeAdmin(object):
    list_display = ['name','add_time']
    search_fields = ['name']
    list_filter = ['name']


class TopicAdmin(object):
    list_display = ['name','content' ,'add_time','click_num','number','floor','add_time']
    search_fields = ['name','content' ,'add_time','click_num','number']
    list_filter = ['name','content' ,'add_time','click_num','number']

xadmin.site.register(Node, NodeAdmin)
xadmin.site.register(Topic, TopicAdmin)