from rest_framework.pagination import CursorPagination


class Mypagination(CursorPagination):
    page_size = 2
    ordering = ['id']