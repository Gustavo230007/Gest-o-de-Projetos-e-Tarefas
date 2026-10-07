from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import Jogador, Time


class TimeDetailViewTests(TestCase):
	def test_time_detail_shows_only_players_from_selected_team(self):
		time = Time.objects.create(
			nome="Vasco",
			cidade="Rio de Janeiro",
			data_fundacao=date(1898, 8, 21),
		)
		outro_time = Time.objects.create(
			nome="Outro time",
			cidade="Sao Paulo",
			data_fundacao=date(1900, 1, 1),
		)
		Jogador.objects.create(nome="Jogador do Vasco", posicao="Atacante", idade=25, time=time)
		Jogador.objects.create(nome="Jogador de outro time", posicao="Defensor", idade=26, time=outro_time)

		response = self.client.get(reverse("core:time_detail", args=[time.pk]))

		self.assertContains(response, "Jogador do Vasco")
		self.assertNotContains(response, "Jogador de outro time")
