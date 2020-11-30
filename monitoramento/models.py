from django.db import models

class Acao(models.Model):
    symbol = models.CharField(max_length=10)
    monitor_price = models.CharField(max_length=20)
    recent_price = models.CharField(max_length=20)
    monitor_type = models.CharField(max_length=5)
    
    def __str__(self):
        template = '{0.symbol} {0.monitor_price} {0.recent_price} {0.monitor_type}' 
        return {
            "symbol": self.symbol,
            "monitor_price": self.monitor_price,
            "recent_price": self.recent_price,
            "monitor_type": self.monitor_type,
        }



    
