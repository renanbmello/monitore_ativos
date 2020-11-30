from django.shortcuts import render, redirect
from .models import Acao
from .forms import AcaoForm
from django.contrib import messages
import requests
import json


def home(request):
    if request.method == 'POST':
        listAcao = []
        api_resquet = requests.get(
            "https://api.hgbrasil.com/finance/stock_price?key=b653093a&symbol=" + str(request.POST['symbol']))
        
        symbol = None 

        try:
            
            symbol = Acao.objects.get(symbol=str(request.POST['symbol']).upper())


        except Exception as e:
            
            
            api = "Erro"

        try:
            api = json.loads(api_resquet.content)
            for result in api['results'].keys():
                listAcao.append(api['results'][result])    
        except Exception as e: 
            api = "Erro"
        return render(request, 'home.html', {'exists': symbol, 'listAcao': listAcao})

    else:
        acoes = Acao.objects.all()
        listAcao = []

        for acao in acoes:
            listAcao.append(acao)

        return render(request, 'home.html', {'bank': acoes, 'exists': acoes, 'listAcao': listAcao})

            

def acao(request):
    if request.method == 'POST':        
        try:
            acao = Acao.objects.get(symbol=str(request.POST['symbol']))

            form = AcaoForm(instance=acao, data=request.POST or none)

            if form.is_valid():
                form.save()
                messages.success(request, ("Atualizado"))
            
            return redirect(home)

        except Exception as e:
            form = AcaoForm(request.POST or none)

            if form.is_valid():
                form.save()
                messages.success(request, ("Monitorando"))
        
        return redirect(home)
   

def delete(request, acao_id):
    item = Acao.objects.get(symbol = acao_id)
    item.delete()
    messages.success(request,("Ação deletada"))

    return redirect(home)


 