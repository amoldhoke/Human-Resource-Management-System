from rest_framework.pagination import PageNumberPagination

class CandidatePagination(PageNumberPagination):
 page_size = 10
 page_query_param = 'p'
 page_size_query_param = 'records'
 max_page_size = 100
 last_page_strings = ('last','end')