import xadmin
from .models import Node,Topic,PingLun

class NodeAdmin(object):
    list_display = ['name','add_time']
    search_fields = ['name']
    list_filter = ['name']


class TopicAdmin(object):
    list_display = ['name','content' ,'add_time','click_num','number','floor','add_time']
    search_fields = ['name','content' ,'add_time','click_num','number']
    list_filter = ['name','content' ,'add_time','click_num','number']


class PingLunAdmin(object):
    list_display = ['pinglun_topic', 'cengji', 'mubiao_user', 'pinglun_text', 'pinglun_user']
    search_fields = ['pinglun_topic', 'cengji', 'mubiao_user', 'pinglun_text', 'pinglun_user']
    list_filter = ['pinglun_topic', 'cengji', 'mubiao_user', 'pinglun_text', 'pinglun_user']


xadmin.site.register(Node, NodeAdmin)
xadmin.site.register(Topic, TopicAdmin)
xadmin.site.register(PingLun, PingLunAdmin)