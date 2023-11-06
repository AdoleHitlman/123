from rest_framework.pagination import PageNumberPagination

class HabitPagination(PageNumberPagination):
    pagesize = 5
