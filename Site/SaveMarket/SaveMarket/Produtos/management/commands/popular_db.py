import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from SaveMarket.Produtos.models import MercadoParceiro, Produto


class Command(BaseCommand):
    help = "Popula o banco de dados com mercados e produtos de exemplo"

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpar',
            action='store_true',
            help='Apaga todos os mercados e produtos antes de popular',
        )

    def handle(self, *args, **options):
        if options['limpar']:
            Produto.objects.all().delete()
            MercadoParceiro.objects.all().delete()
            self.stdout.write(self.style.WARNING('Dados antigos apagados.'))

        # ── MERCADOS ──
        mercados_dados = [
            ("Mercado São João", "Rua das Flores, 123 — Copacabana, Rio de Janeiro/RJ"),
            ("Supermercado Preço Bom", "Av. Nossa Senhora de Copacabana, 540 — Rio de Janeiro/RJ"),
            ("Padaria Pão Quente", "Rua Barata Ribeiro, 88 — Botafogo, Rio de Janeiro/RJ"),
            ("Açougue do Zé", "Rua Voluntários da Pátria, 200 — Botafogo, Rio de Janeiro/RJ"),
            ("Hortifruti Natural", "Rua Visconde de Pirajá, 415 — Ipanema, Rio de Janeiro/RJ"),
            ("Restaurante Sabor Caseiro", "Av. Atlântica, 1702 — Copacabana, Rio de Janeiro/RJ"),
        ]

        mercados = []
        for nome, endereco in mercados_dados:
            mercado, _ = MercadoParceiro.objects.get_or_create(
                nome=nome, defaults={'endereco': endereco}
            )
            mercados.append(mercado)
        self.stdout.write(self.style.SUCCESS(f'{len(mercados)} mercados criados.'))

        # ── PRODUTOS POR CATEGORIA ──
        # (titulo, categoria, preco_original)
        produtos_dados = [
            ("Leite Integral 1L", "laticinio", 5.49),
            ("Iogurte Natural 170g", "laticinio", 3.99),
            ("Queijo Mussarela 500g", "laticinio", 24.90),
            ("Manteiga com Sal 200g", "laticinio", 9.90),
            ("Pão de Forma Integral", "padaria", 6.99),
            ("Pão Francês (10un)", "padaria", 8.50),
            ("Bolo de Cenoura", "padaria", 18.00),
            ("Croissant", "padaria", 5.50),
            ("Filé de Frango 1kg", "carnes", 18.90),
            ("Carne Moída 500g", "carnes", 15.00),
            ("Linguiça Toscana 1kg", "carnes", 22.00),
            ("Maçã Gala (kg)", "frutas", 7.99),
            ("Banana Prata (kg)", "frutas", 5.49),
            ("Mamão Papaya (un)", "frutas", 4.99),
            ("Alface Crespa (un)", "vegetais", 3.49),
            ("Tomate (kg)", "vegetais", 6.99),
            ("Cenoura (kg)", "vegetais", 4.49),
            ("Lasanha Congelada 600g", "congelados", 19.90),
            ("Pizza Congelada 460g", "congelados", 16.50),
            ("Hambúrguer Bovino (4un)", "lanches", 12.90),
            ("Arroz Branco 5kg", "despensa", 27.90),
            ("Feijão Preto 1kg", "despensa", 8.99),
            ("Refrigerante Cola 2L", "bebidas", 9.50),
            ("Suco de Laranja 1L", "bebidas", 7.99),
        ]

        criados = 0
        for titulo, categoria, preco_orig in produtos_dados:
            mercado = random.choice(mercados)

            # desconto entre 20% e 60%
            desconto = random.uniform(0.20, 0.60)
            preco_desc = round(preco_orig * (1 - desconto), 2)

            # validade entre hoje e 7 dias à frente
            dias = random.randint(0, 7)
            validade = timezone.now().date() + timedelta(days=dias)

            Produto.objects.create(
                mercado=mercado,
                titulo=titulo,
                categoria=categoria,
                preco_original=preco_orig,
                preco_desconto=preco_desc,
                validade=validade,
            )
            criados += 1

        self.stdout.write(self.style.SUCCESS(f'{criados} produtos criados.'))
        self.stdout.write(self.style.SUCCESS('Banco populado com sucesso! 🎉'))
