from rest_framework.throttling import SimpleRateThrottle


class My_throttle(SimpleRateThrottle):
    '''
        也可以继承BaseThrottle类，实现allow_request方法，还是要获取对象的标识信息
    '''
    scope = 'shuaiqi'  # 全剧终，配置rate使用

    def get_cache_key(self, request, view):  # 返回唯一标识信息：ip地址
        return request._request.META.get('REMOTE_ADDR')
