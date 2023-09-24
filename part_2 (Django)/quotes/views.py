from django.views.generic.edit import CreateView
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin

from .utils import get_mongodb


def main(request, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})


class QuoteCreateView(LoginRequiredMixin, CreateView):
    model = quotes
    fields = ['quote', 'tags', 'author']
    template_name = 'quotes/quote_form.html'
    success_url = reverse_lazy('quotes')
