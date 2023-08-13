from urllib.parse import urlencode

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.urls import reverse


def paginate_queryset(queryset, page, per_page):
    paginator = Paginator(queryset, per_page)

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return items, paginator.num_pages


def get_request_params(request):
    query_params = request.GET.copy()
    query_params.pop('page', None)
    query_string = urlencode(query_params)

    if query_string:
        query_string = '&' + query_string

    return query_string

