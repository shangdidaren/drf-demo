from django.urls import path, re_path,include
from app import views
from rest_framework.routers import DefaultRouter
route = DefaultRouter()
route.register('mbook',views.BookModelView)
route.register('data',views.DataView)
app_name = 'app'

urlpatterns = [
    # path('?P<version>[v1|v2]+)/user/', UserView.as_view()),
    # re_path('(?P<version>[v1|v2]+)/user/(?P<pk>\d+)', UserView.as_view(), name='gp'),
    # re_path('(?P<version>[v1|v2]+)/user/', UserView.as_view()),

    # re_path('(?P<version>[v1|v2]+)/test/$', Test.as_view({'get': 'list','post':'create'})),
    # re_path('(?P<version>[v1|v2]+)/test/(?P<pk>\d+)/$', Test.as_view({'get':'retrieve',
    #                                                                 'delete':'destroy',
    #                                                                 'put': 'update',
    #                                                                 'patch':'partial_update'
    #
    #                                                              })),
    re_path('(?P<version>[v1|v2]+)/book/',views.BookView.as_view(), name='book'),

    re_path('(?P<version>[v1|v2]+)/userinfo/(?P<pk>[0-9]+)', views.UserinfoView.as_view(), name='userinfo'),
    re_path('(?P<version>[v1|v2]+)/userinfo/',views.UserinfoView.as_view(), name='userinfos'),

    re_path('(?P<version>[v1|v2]+)/', include(route.urls)),

]
