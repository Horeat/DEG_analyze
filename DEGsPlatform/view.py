from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators import csrf
import pandas as pd

file_df = None

def home(request):
    context = {}
    context['upload_res'] = "Step 1"
    return render(request,"indexPage.html",context)

def upload_csv(request):
    data = {}
    if request.POST:
        data['upload_res'] = "upload success!"
        File = request.FILES["file"]
        file_df = pd.read_csv(File)
        data['size']=file_df["A"][0]
    
    return render(request,"indexPage.html",data)
    # else:
    #     return HttpResponse("222")

def check_column(request):
    pass

def cal_degs(request):
    data  = {}
    gev = 0
    pv = 0
    if request.POST:
        gev = request.POST["express_value"]
        pv = request.POST["p_value"]
    return HttpResponse('222')