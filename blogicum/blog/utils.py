from django.core.paginator import Paginator


def paginate(model, page_number):
    paginator = Paginator(model, 10)
    page_obj = paginator.get_page(page_number)
    return page_obj
