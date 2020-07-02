from app.serializers import Data_Serializer
from app.utils import auth, throttle, permission, pagination

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from rest_framework.response import Response
from rest_framework import status
from app import models

from app.serializers import NewBook_Serializer, Userinfo_Serializer


# http://127.0.0.1:8000/app/v1/book/
class BookView(APIView):
    '''
        局部使用认证、权限、节流、解析器、渲染器，全局使用版本器
    '''
    authentication_classes = [auth.My_authentication]
    permission_classes = [permission.My_permission]
    throttle_classes = [throttle.My_throttle]

    '''
    默认使用的解析器
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ],
    默认使用的渲染器
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
    '''
    # parser_classes = []
    # renderer_classes = []

    def get(self, request, *args, **kwargs):
        context = {
            'ret': 'ok',
            'code': 1,
        }
        return Response(context)


# http://127.0.0.1:8000/app/v1/userinfo/
class UserinfoView(APIView):
    '''
        使用自定义的序列化类进行操作
        单删，群删的接口不应该删除数据，而是将数据的is_delete属性置为1
    '''

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            try:
                ser = Userinfo_Serializer(
                    instance=models.UserInfo.objects.get(
                        pk=pk), many=False)
                context = {
                    'ret': ser.data,
                    'code': 1,
                }
                return Response(context)
            except BaseException:
                context = {
                    'ret': '输入的id不合法',
                    'code': 0,
                }
                return Response(context)
        else:
            queryset = models.UserInfo.objects.filter(is_delete=False)
            ser = Userinfo_Serializer(instance=queryset, many=True)
            context = {
                'ret': ser.data,
                'code': 1,
            }
            return Response(context)

    def delete(self, request, *args, **kwargs):
        # 删除只需要pk就可以，，is_delete作为一个开关不需要其他参数
        # 单删通过url，群删传一个列表,无需序列化的参入
        pk = kwargs.get('pk')
        if pk:
            pks = [pk]
        elif not pk:
            pks = request.data.get('pks')
        if not pks:
            context = {'ret': '请传入pk', 'code': '2'}
            return Response(context)
        else:
            if models.UserInfo.objects.filter(
                    pk__in=pks).update(
                    is_delete=True):
                return Response({'ret': "删除成功"})
            else:
                return Response({'ret': '删除失败'})


# http://127.0.0.1:8000/app/v1/mbook/
class BookModelView(ModelViewSet):
    '''
        单增，群增;单查群查 接口的实现
    '''
    queryset = models.NewBook.objects
    pagination_class = pagination.Mypagination
    serializer_class = NewBook_Serializer

    def create(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, dict):
            many = False
        elif isinstance(data, list):
            many = True
        else:
            context = {'ret': '传入的数据有误', 'code': 4}
            return Response(context)
        serializer = self.get_serializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers)


# http://127.0.0.1:8000/app/v1/data/


class DataView(ModelViewSet):
    '''
        单改（局部单改，整体单改） 根据你是通过put请求还是patch请求
        http://127.0.0.1:8000/app/v1/data/1/
    '''
    queryset = models.Data.objects.all()
    pagination_class = pagination.Mypagination
    serializer_class = Data_Serializer

    # 整体群改和局部群改的相似
    # 改的步骤：先将数据清洗，剔除不存的的pk，然后找出初始的结果集赋给instance
    # 将提交的数据赋给data，partial为True局部，否则整体
    # 将序列化类关联自定义的ListSerializer，实现update方法（具体实现看群增，遍历）
    # todo 群改的数据过滤按照前端传来的数据过滤，最好的格式为
    #  {'pk1':{update_data},'pk2':{update_data}
    #  }  直接删除pk就删除value了

    # 过滤器的使用
    from rest_framework.filters import SearchFilter, OrderingFilter
    filter_backends = [SearchFilter]
    search_fields = ['name']
    # /?search=‘李’
    # ordering_fields = ['-number','pk']
    # /?ordering=-number,pk，先按price降序，如果出现price相同，再按pk升序

    # todo 还可以使用django-filter进行高精确的过滤
