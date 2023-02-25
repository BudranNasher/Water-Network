from django.db import models

#valves
class Valve(models.Model):
    long = models.DecimalField(max_digits=15, decimal_places=13)
    lat = models.DecimalField(max_digits=15, decimal_places=13)
    soft_delete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

#tree points 
class Tree(models.Model):
    long = models.DecimalField(max_digits=15, decimal_places=13)
    lat = models.DecimalField(max_digits=15, decimal_places=13)
    valve = models.ForeignKey(Valve, on_delete=models.CASCADE, related_name='valves', null = True, blank = True)
    distance = models.SmallIntegerField(null = True, blank = True)

    def __str__(self):
        return str(self.id)
