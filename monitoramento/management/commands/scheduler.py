from monitoramento.models import Acao
from monitoramento.forms import AcaoForm
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.conf import settings
from django.core.mail import send_mail
import requests
import json 

def update_price():
    acoes = Acao.objects.all()

    if len(acoes) != 0:
        for acao in acoes:
            api_resquet = requests.get(
            "https://api.hgbrasil.com/finance/stock_price?key=b653093a&symbol=" + acao.symbol)
            new_price = None
            api = json.loads(api_resquet.content)
            for result in api['results'].keys():
                new_price = api['results'][result]["price"]
            

            if new_price != float(acao.recent_price):
                new_acao = {
                    "symbol": acao.symbol,
                    "recent_price": acao.recent_price,
                    "monitor_price": acao.monitor_price,
                    "monitor_type": acao.monitor_type
                }

                form = AcaoForm(instance=acao, data=new_acao)

                if form.is_valid():
                    form.save()
                                     
            
            if acao.monitor_type == 'buy':

                if new_price >= float(acao.monitor_price):
                    send_mail(
                        'Compra de Ação!',
                        'Seu ativo monitorado '+ str(acao.symbol) + ' atingiu o valor desejado para compra!',
                        'renanbmello@gmail.com',
                        ['renanbmello@gmail.com'],
                        fail_silently=False,
                    )
            else:
                if new_price <= float(acao.monitor_price):
                    send_mail(
                        'Venda de Ação!',
                        'Seu ativo monitorado '+ str(acao.symbol) + ' atingiu o valor desejado para venda!',
                        'renanbmello@gmail.com',
                        ['renanbmello@gmail.com'],
                        fail_silently=False,
                    )
           


       

class Command(BaseCommand):
    # help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        scheduler.add_job(update_price, trigger=CronTrigger(minute="*/15"), id="my_job", max_instances=1, replace_existing=True)

        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()