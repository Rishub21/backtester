from django.shortcuts import render
from django.http import HttpResponse
from portfolio_constructor import get_adjusted_close


ticker_list = []
# Create your views here.
def index(request):
    response = render(request,"finpy/index.html")
    return response


    if request.method == "POST":
        stockquery = request.POST.get("stockquery")
        global ticker_list
        tickerlist.append(stockquery)


def plotter(request):

    if request.method == "POST":
        startDate = request.POST.get("starting")
        endDate = request.POST.get("end")
        get_adjusted_close(ticker_list, startDate, endDate)
