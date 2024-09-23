from celery.worker.state import requests
from django.shortcuts import render
from .scrapper import scrape_amazon_product , recommend_best_product

# Create your views here.

def index(request):
    return render(request, 'index.html')

def scrap(request):
    if request.method == 'POST':
        search_term = request.POST['search_term']
        product_data = scrape_amazon_product(search_term)
        best_product = recommend_best_product(product_data)
        # Pass the scraped data directly to the template
        return render(request, 'results.html', {'products': product_data, 'best_product': best_product})
    else:
        return render(request, 'index.html')

