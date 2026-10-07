from django.db import models

# Create your models here.
class Time(models.Model):
    nome = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    data_fundacao = models.DateField()

    def __str__(self):
        return self.nome
    
class Jogador(models.Model):        
    nome = models.CharField(max_length=100)
    posicao = models.CharField(max_length=50)
    idade = models.IntegerField()
    time = models.ForeignKey(Time, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome