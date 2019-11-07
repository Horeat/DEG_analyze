from django.shortcuts import render
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.views.decorators import csrf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#from .cal import IsColumnExist,SelectDeg

def home(request):
    context = {}
    context['upload_res'] = "Step 1"
    return render(request,"indexPage.html",context)

def upload_csv(request):
    global file_in
    data = {}   
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
                data['info'] = "Both columns are valid. Please continue"
                return render(request,"methodPage.html",data)
            else:
                data['info'] = "Case column is not exist. Please check or reload file!"
                return render(request,"indexPage.html",data)
        else:
            if case_in in c:
                data['info'] = "Control column is not exist. Please check or reload file!"
                return render(request,"indexPage.html",data)
            else:
                data['info'] = "Both columns are not exist. Please check or reload file!"
                return render(request,"indexPage.html",data)

        #data['info'] = IsColumnExist()



def draw_pictures(data_file,filtered_data_file):
    data_in = data_file
    filtered_data_in = filtered_data_file
    remaining_data_in = data_in[~data_in[data_in.columns.values.tolist()[0]].isin(filtered_data_in.loc[:,data_in.columns.values.tolist()[0]])]
    gene_data = data_in.loc[:,[control_in,case_in]]
    filtered_gene_data = filtered_data_in.loc[:,[control_in,case_in]]
    remaining_gene_data = remaining_data_in.loc[:,[control_in,case_in]]

    sns.set(style="whitegrid", context="notebook")

    plt.figure(figsize=(6,4))   #箱图
    plt.title('Box Chart of Original dataset')
    plt.ylabel('Gene Express Value')
    plt.xlabel('Group Name')
    sns.boxplot(data = gene_data)
    sns.swarmplot(data = gene_data,color = 'grey')
    plt.savefig('./static/images/box1.png')

    plt.figure(figsize=(6,4))   
    plt.title('Box Chart of DEGs dataset')
    plt.ylabel('Gene Express Value')
    plt.xlabel('Group Name')
    sns.boxplot(data = filtered_gene_data)
    sns.swarmplot(data = filtered_gene_data,color = 'grey')
    plt.savefig('./static/images/box2.png')

    plt.figure(figsize=(6,4))   
    plt.title('Box Chart of Filtered dataset')
    plt.ylabel('Gene Express Value')
    plt.xlabel('Group Name')
    sns.boxplot(data = remaining_gene_data)
    sns.swarmplot(data = remaining_gene_data,color = 'grey')
    plt.savefig('./static/images/box3.png')


    plt.figure(figsize=(6,4))   #散点图
    plt.title('Scatter Chart of Original dataset')
    plt.ylabel('Gene Express Value')
    plt.xlabel('Group Name')
    sns.scatterplot(x=[0 for i in range(gene_data.shape[0])] , y=list(gene_data.loc[:,control_in]))
    sns.scatterplot(x=[1 for i in range(gene_data.shape[0])] , y=list(gene_data.loc[:,case_in]))
    plt.xlim(-0.7,1.7)
    plt.xticks([0,1], [control_in,case_in])
    plt.savefig('./static/images/scatter1.png')

    plt.figure(figsize=(6,4))  
    plt.title('Scatter Chart of DEGs dataset')
    plt.ylabel('Gene Express Value')
    plt.xlabel('Group Name')
    sns.scatterplot(x=[0 for i in range(filtered_gene_data.shape[0])] , y=list(filtered_gene_data.loc[:,control_in]))
    sns.scatterplot(x=[1 for i in range(filtered_gene_data.shape[0])] , y=list(filtered_gene_data.loc[:,case_in]))
    plt.xlim(-0.7,1.7)
    plt.xticks([0,1], [control_in,case_in])
    plt.savefig('./static/images/scatter2.png')

    plt.figure(figsize=(6,4))  
    plt.title('Scatter Chart of Filtered dataset')
    plt.ylabel('Gene Express Value')
    plt.xlabel('Group Name')
    sns.scatterplot(x=[0 for i in range(remaining_gene_data.shape[0])] , y=list(remaining_gene_data.loc[:,control_in]))
    sns.scatterplot(x=[1 for i in range(remaining_gene_data.shape[0])] , y=list(remaining_gene_data.loc[:,case_in]))
    plt.xlim(-0.7,1.7)
    plt.xticks([0,1], [control_in,case_in])
    plt.savefig('./static/images/scatter3.png')


    plt.figure(figsize=(6,4))   #折线图
    plt.title('Line Chart of Original dataset')
    plt.ylabel('Gene Express Value')
    plt.xlabel('Index Of Gene')
    sns.lineplot(x=[i+1 for i in range(gene_data.shape[0])] , y=list(gene_data.loc[:,control_in]) , label = 'Control')
    sns.lineplot(x=[i+1 for i in range(gene_data.shape[0])] , y=list(gene_data.loc[:,case_in]) , label = 'Case')
    plt.savefig('./static/images/line1.png')

    plt.figure(figsize=(6,4))  
    plt.title('Line Chart of DEGs dataset')
    plt.ylabel('Gene Express Value')
    plt.xlabel('Index Of Gene')
    sns.lineplot(x=[i+1 for i in range(filtered_gene_data.shape[0])] , y=list(filtered_gene_data.loc[:,control_in]) , label = 'Control')
    sns.lineplot(x=[i+1 for i in range(filtered_gene_data.shape[0])] , y=list(filtered_gene_data.loc[:,case_in]) , label = 'Case')
    plt.savefig('./static/images/line2.png')

    plt.figure(figsize=(6,4))  
    plt.title('Line Chart of Filtered dataset')
    plt.ylabel('Gene Express Value')
    plt.xlabel('Index Of Gene')
    sns.lineplot(x=[i+1 for i in range(remaining_gene_data.shape[0])] , y=list(remaining_gene_data.loc[:,control_in]) , label = 'Control')
    sns.lineplot(x=[i+1 for i in range(remaining_gene_data.shape[0])] , y=list(remaining_gene_data.loc[:,case_in]) , label = 'Case')
    plt.savefig('./static/images/line3.png')


    plt.figure(figsize=(6,4))   #热图
    plt.title('Heat Map of Original dataset')
    plt.ylabel('Gene Express Value')
    plt.xlabel('Index Of Gene')
    sns.heatmap(gene_data,annot=True)
    plt.savefig('./static/images/heat1.png')

    plt.figure(figsize=(6,4)) 
    plt.title('Heat Map of DEGs dataset')
    plt.ylabel('Gene Express Value')
    plt.xlabel('Index Of Gene')
    sns.heatmap(filtered_gene_data,annot=True)
    plt.savefig('./static/images/heat2.png')

    plt.figure(figsize=(6,4)) 
    plt.title('Heat Map of Filtered dataset')
    plt.ylabel('Gene Express Value')
    plt.xlabel('Index Of Gene')
    sns.heatmap(remaining_gene_data,annot=True)
    plt.savefig('./static/images/heat3.png')


def cal_degs(request):
    data  = {}
    gev_in = 0
    pv_in = 0
    filtered_data = None
    if request.POST:
        gev_in = request.POST.get('express_value')
        pv_in = request.POST.get('p_value')

        #method:
        filtered_data = file_in[(abs(file_in[control_in]-file_in[case_in]) > float(gev_in)) & (file_in['p_value'] < float(pv_in))]
        
        #filtered_data = SelectDeg(gev_in,pv_in)
        num = filtered_data.shape[0]
        data['feedback'] = "We have select %d DE_genes" %num
        filtered_data.to_csv('D:/filtered_data.csv',index = False)
        draw_pictures(file_in,filtered_data)
    return render(request,"outcomePage.html",data)


def download_file(request):
    def file_iterator(file_name,chunk_size=512):
        with open(file_name, 'rb') as f:
            if f:
                yield f.read(chunk_size)
                print ('下载完成')
            else:
                print ('未完成下载')

    the_file_name = 'D:/filtered_data.csv'
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachement;filename="{0}"'.format(the_file_name)
    return response


 