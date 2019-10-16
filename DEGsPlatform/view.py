from django.shortcuts import render
from django.http import HttpResponse
from django.http import FileResponse
from django.views.decorators import csrf
import pandas as pd
#from .cal import IsColumnExist,SelectDeg

def home(request):
    context = {}
    context['upload_res'] = "Step 1"
    return render(request,"indexPage.html",context)

def upload_csv(request):
    global file_in
    data = {}   #????????
    if request.POST:
        data['upload_res'] = "upload success!"
        File = request.FILES["file"]
        file_in = pd.read_csv(File)
        data['size'] = file_in.shape[0]
    return render(request,"indexPage.html",data)


def check_column(request):
    global control_in
    global case_in
    data = {}
    c = None
    if request.POST:
        control_in = request.POST.get('control')
        case_in = request.POST.get('case')

        #method:
        c = file_in.columns.values.tolist()
        if control_in in c:
            if case_in in c:
                data['info'] = "Both columns are valid. Please proceed to the next step!"
            else:
                data['info'] = "Case column is not exist. Please check or reload file!"
        else:
            if case_in in c:
                data['info'] = "Control column is not exist. Please check or reload file!"
            else:
                data['info'] = "Both columns are not exist. Please check or reload file!"

        #data['info'] = IsColumnExist()
    return render(request,"indexPage.html",data)


def cal_degs(request):
    data  = {}
    gev_in = 0
    pv_in = 0
    filtered_data = None
    if request.POST:
        gev_in = request.POST.get('express_value')
        pv_in = request.POST.get('p_value')

        #method:
        filtered_data = file_in[(abs(file_in['A']-file_in['B']) > float(gev_in)) & (file_in['p_value'] < float(pv_in))]
        
        #filtered_data = SelectDeg(gev_in,pv_in)
        num = filtered_data.shape[0]
        data['feedback'] = "We have select %d DE_genes" %num
    return render(request,"indexPage.html",data)

