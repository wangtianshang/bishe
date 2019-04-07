import xadmin
from .models import Node,Topic,PingLun,HuiFu

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


class HuiFuAdmin(object):

    list_display = ['huifu_pinglun', 'cengji', 'pinglun_text', 'huifu_user_name', 'mubiao_user_name']
    search_fields = ['huifu_pinglun', 'cengji', 'pinglun_text', 'huifu_user_name', 'mubiao_user_name']
    list_filter = ['huifu_pinglun', 'cengji', 'pinglun_text', 'huifu_user_name', 'mubiao_user_name']

xadmin.site.register(Node, NodeAdmin)
xadmin.site.register(Topic, TopicAdmin)
xadmin.site.register(PingLun, PingLunAdmin)
xadmin.site.register(HuiFu, HuiFuAdmin)