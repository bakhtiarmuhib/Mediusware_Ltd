from typing import Any
from django.views import generic
from django.views.generic.list import ListView
from product.models import Variant,Product
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator

class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


class ProductListView(ListView):
    model = Product
    paginate_by = 2 
    ordering = ['id']
    template_name = 'products/list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_item'] = Product.objects.count()
        return context


def search(request):
    
    if request.method == 'POST':
        print(request.POST['title'])
        print(request.POST['price_from'])
        print(request.POST['price_to'])
        print(request.POST['date'])

        # print(request.POST['title'])
        # title__icontains= request.POST['title']
        result = Product.objects.filter(
            Q(title__icontains= request.POST['title']) &
            Q(product__price__range =(request.POST['price_from'],request.POST['price_to']))
            
            
            )
        
        
        if len(result)>0:
            
            total = len(result)
            return render(request, 'products/search.html',{
                                                
                                                'result':result,
                                                'total' : total
                                            })
        else:
            return render(request, 'products/no-search-found.html')
    
    return render(request, 'products/no-search-found.html')