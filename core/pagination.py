from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict 


from django.core.paginator import Paginator
from django.utils.functional import cached_property
from rest_framework.pagination import PageNumberPagination

class FasterDjangoPaginator(Paginator):
    @cached_property
    def count(self):
        return self.object_list.values('id').count()


class FasterPageNumberPagination(PageNumberPagination):
    django_paginator_class = FasterDjangoPaginator