import discord
from discord.ext import commands
from discord.ui import Button, View
import json
import numbers
import os
from pathlib import Path
import difflib
from flask import Flask
from threading import Thread
from dotenv import load_dotenv
from datetime import datetime
from datetime import datetime
from zoneinfo import ZoneInfo

load_dotenv()

app = Flask("")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)

canal_laricas_id = None
hora_local = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d-%m-%Y %H:%M:%S")

# Definindo os produtos com a quantidade de ingredientes necessária para cada um
produtos = {
    '🍔 X-Tudo': {
        'ingredientes': {'🥩 Hambúrguer': 1, '🦐 Camarão': 1, '🥬 Alface': 1, '🍅 Tomate': 1, '🧀 Queijo': 1, '🧈 Manteiga': 1, '🍞 Pão de Hambúrguer': 1},
        'peso': 0.5,
        'categoria': 'comida'
    },
    '🥗 X-Salada': {
        'ingredientes': {'🥩 Hambúrguer': 1, '🥬 Alface': 1, '🍅 Tomate': 1, '🧀 Queijo': 1, '🧈 Manteiga': 1, '🍞 Pão de Hambúrguer': 1},
        'peso': 0.5,
        'categoria': 'comida'
    },
    '🥪 X-Burguer': {
        'ingredientes': {'🥩 Hambúrguer': 1, '🧀 Queijo': 1, '🧈 Manteiga': 1, '🍞 Pão de Hambúrguer': 1},
        'peso': 0.5,
        'categoria': 'comida'
    },
    '🍤 Espeto camarão': {
        'ingredientes': {'🦐 Camarão': 1},
        'peso': 0.5,
        'categoria': 'comida'
    },
    '🐟 Caviar': {
        'ingredientes': {'🐟 Sardinha': 1},
        'peso': 0.5,
        'categoria': 'comida'
    },
    '🌽 Milho Cozido': {
        'ingredientes': {'🌽 Milho': 2},
        'peso': 0.5,
        'categoria': 'comida'
    },
    '🍵 Chá Camomila': {
        'ingredientes': {'💧 Água': 1, '🍵 Camomila': 1},
        'peso': 0.5,
        'categoria': 'bebida'
    },
    '🍓 Suco Morango': {
        'ingredientes': {'🍓 Morango': 2, '💧 Água': 1},
        'peso': 0.5,
        'categoria': 'bebida'
    },
    '🍍 Suco Abacaxi': {
        'ingredientes': {'🍍 Abacaxi': 2, '💧 Água': 1},
        'peso': 0.5,
        'categoria': 'bebida'
    },
    '🍌 Suco Banana': {
        'ingredientes': {'🍌 Banana': 2, '💧 Água': 1},
        'peso': 0.5,
        'categoria': 'bebida'
    },
    '🍋 Suco Maracujá': {
        'ingredientes': {'🍋 Maracujá': 2, '💧 Água': 1},
        'peso': 0.5,
        'categoria': 'bebida'
    },
    '🥝 Suco Kiwi': {
        'ingredientes': {'🥝 Kiwi': 2, '💧 Água': 1},
        'peso': 0.5,
        'categoria': 'bebida'
    },
    '🥭 Suco Caju': {
        'ingredientes': {'🥭 Caju': 2, '💧 Água': 1},
        'peso': 0.5,
        'categoria': 'bebida'
    },
    '🍊 Suco Laranja': {
        'ingredientes': {'🍊 Laranja': 2, '💧 Água': 1},
        'peso': 0.5,
        'categoria': 'bebida'
    },
    '🍇 Suco Uva': {
        'ingredientes': {'🍇 Uva': 2, '💧 Água': 1},
        'peso': 0.5,
        'categoria': 'bebida'
    },
    '🍑 Suco Pêssego': {
        'ingredientes': {'🍑 Pêssego': 2, '💧 Água': 1},
        'peso': 0.5,
        'categoria': 'bebida'
    },
    '☕ Café': {
        'ingredientes': {'☕ Grãos de Café': 1, '💧 Água': 1},
        'peso': 0.5,
        'categoria': 'bebida'
    },
    '⚡ Energético': {
        'ingredientes': {'⚡ Grãos de Guaraná': 1, '💧 Água': 1},
        'peso': 0.5,
        'categoria': 'bebida'
    },
    '🍞 Pão de Hambúrguer': {
        'ingredientes': {'🌾 Farinha de Trigo': 1},
        'peso': 0.2,
        'categoria': 'comida'
    },
    '🥩 Hambúrguer': {
        'ingredientes': {
            '🥩 Cupim Cru': 1,
            '🥩 Músculo Cru': 1,
            '🥩 Picanha Cru': 1,
            '🥩 Costela Cru': 1,
            '🥩 Maminha Cru': 1
        },
        'peso': 0.2,
        'categoria': 'comida'
    },
    '🌾 Farinha de Trigo': {
        'ingredientes': {'🌾 Trigo': 1},
        'peso': 0.2,
        'categoria': 'comida'
    },
}

pesos_ingredientes = {
    '🥩 Hambúrguer': 0.2,
    '🦐 Camarão': 0.3,
    '🥬 Alface': 0.2,
    '🍅 Tomate': 0.2,
    '🧀 Queijo': 0.5,
    '🧈 Manteiga': 0.3,
    '🍞 Pão de Hambúrguer': 0.2,
    '🐟 Sardinha': 0.3,
    '🌽 Milho': 0.1,
    '💧 Água': 0.5,
    '🍵 Camomila': 0.3,
    '🍓 Morango': 0.1,
    '🍍 Abacaxi': 0.1,
    '🍌 Banana': 0.1,
    '🍋 Maracujá': 0.3,
    '🥝 Kiwi': 0.1,
    '🥭 Caju': 0.1,
    '🍊 Laranja': 0.1,
    '🍇 Uva': 0.1,
    '🍑 Pêssego': 0.1,
    '☕ Grãos de Café': 0.3,
    '⚡ Grãos de Guaraná': 0.2,
    '🌾 Farinha de Trigo': 0.2,
    '🌾 Trigo': 0.2,
    '🥩 Cupim Cru': 0.7,
    '🥩 Músculo Cru': 0.4,
    '🥩 Picanha Cru': 0.8,
    '🥩 Costela Cru': 0.6,
    '🥩 Maminha Cru': 0.5,
}

ingredientes = { 
    "comida": [
        "🥩 Hambúrguer", "🦐 Camarão", "🥬 Alface", "🍅 Tomate", "🧀 Queijo", "🧈 Manteiga", "🍞 Pão de Hambúrguer", "🐟 Sardinha", "🌽 Milho", "🌾 Trigo" , "🌾 Farinha de Trigo", "🥩 Cupim Cru", "🥩 Músculo Cru", "🥩 Picanha Cru", "🥩 Costela Cru", "🥩 Maminha Cru"
    ],
    "bebida": [
        "☕ Grãos de Café", "⚡ Grãos de Guaraná", "🍵 Camomila", "💧 Água", '🍓 Morango', '🍍 Abacaxi', '🍌 Banana', '🍋 Maracujá', '🥝 Kiwi', '🥭 Caju', '🍊 Laranja', '🍇 Uva', '🍑 Pêssego',
        ]
    }

# Dicionário para armazenar temporários
producoes_em_espera = {}

producoes_usuario = {}

mensagens_stock = {}
mensagens_historico = {}

# Pasta onde este ficheiro .py está guardado
BASE_DIR = Path(__file__).resolve().parent

# JSON ficará na MESMA pasta do .py
ARQ_STOCK = BASE_DIR / "dados_estoque.json"
HISTORICO_FILE = BASE_DIR /'historico_stock.json'

def gravar_historico(user_id: int, username: str, canal: str, operacao: str, adicionados: dict = None, retirados: dict = None):
    if adicionados is None:
        adicionados = {}
    if retirados is None:
        retirados = {}

    entrada = {
        "timestamp": datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d-%m-%Y %H:%M:%S"),
        "user_id": str(user_id),
        "username": username,
        "canal": canal,
        "operacao": operacao,
        "adicionados": adicionados,
        "retirados": retirados
    }

    try:
        with open(HISTORICO_FILE, 'r', encoding='utf-8') as f:
            historico = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        historico = []

    historico.append(entrada)

    with open(HISTORICO_FILE, 'w', encoding='utf-8') as f:
        json.dump(historico, f, indent=4, ensure_ascii=False)

def obter_historico():
    try:
        with open(HISTORICO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def carregar_estoque() -> dict[str, dict]:
    try:
        with open(ARQ_STOCK, "r", encoding="utf-8") as f:
            bruto = json.load(f)
        return bruto
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

producoes_stock: dict[str, dict] = carregar_estoque()
producao_temp: dict[str, dict] = {}  # IDs como string, sempre

def criar_view_atualizar_stock(user_id: int, producao: dict, produtos_produzidos: dict) -> View:
    view = View(timeout=None)
    botao = Button(label="🔄 Atualizar Stock", style=discord.ButtonStyle.primary)

    async def callback(interaction: discord.Interaction):
        if interaction.user.id != user_id:
            await interaction.response.send_message("Este botão não é para você.", ephemeral=True)
            return

        # ✅ Obtém o ID correto, dependendo do canal
        uid_str = get_contextual_user_id(interaction)
        producoes_stock.setdefault(uid_str, {})
        estoque = producoes_stock[uid_str]

        produtos_especiais = ['🍔 X-Tudo', '🥗 X-Salada', '🥪 X-Burguer', '🥩 Hambúrguer', '🌾 Farinha de Trigo']

        for produto, qtd in produtos_produzidos.items():
            divisor = 2 if produto in produtos_especiais else 1
            porcoes = qtd // divisor

            for ingrediente, qtd_receita in produtos[produto]['ingredientes'].items():
                qtd_ingrediente_total = qtd_receita * porcoes
                qtd_atual = estoque.get(ingrediente, 0)
                novo_qtd = qtd_atual - qtd_ingrediente_total
                estoque[ingrediente] = max(novo_qtd, 0)
                if estoque[ingrediente] == 0:
                    del estoque[ingrediente]

        for produto, qtd in produtos_produzidos.items():
            qtd_antes = estoque.get(produto, 0)
            estoque[produto] = qtd_antes + qtd
    
        salvar_estoque(producoes_stock)

        await interaction.response.send_message("✅ Estoque atualizado com sucesso!", ephemeral=True)

        for item in view.children:
            item.disabled = True
        await interaction.message.edit(view=view)

    botao.callback = callback
    view.add_item(botao)
    return view

def pode_produzir(produto: str, quantidade: int, estoque: dict[str, int]) -> bool:
    ingredientes_necessarios = produtos[produto]['ingredientes']
    produtos_especiais = ['🍔 X-Tudo', '🥗 X-Salada', '🥪 X-Burguer', '🥩 Hambúrguer', '🌾 Farinha de Trigo']

    if produto in produtos_especiais:
        porcoes = quantidade // 2
        if porcoes == 0:
            return False  # Precisa de pelo menos 2 para fazer 1 porção
        quantidade_para_verificar = porcoes
    else:
        quantidade_para_verificar = quantidade

    for ingrediente, qtd_necessaria in ingredientes_necessarios.items():
        if estoque.get(ingrediente, 0) < qtd_necessaria * quantidade_para_verificar:
            return False

    return True

def consumir_ingredientes(produto, quantidade, estoque):
    ingredientes_necessarios = produtos[produto]['ingredientes']

    produtos_especiais = ['🍔 X-Tudo', '🥗 X-Salada', '🥪 X-Burguer','🥩 Hambúrguer','🌾 Farinha de Trigo']

    # Calcula a quantidade ajustada para produtos especiais
    if produto in produtos_especiais:
        porcoes = quantidade // 2
        quantidade_ajustada = porcoes
    else:
        quantidade_ajustada = quantidade

    # Agora percorre cada ingrediente necessário, retirando a quantidade ajustada
    for ingrediente, qtd_necessaria in ingredientes_necessarios.items():
        # Ajusta a quantidade necessária para produtos especiais
        if produto in produtos_especiais:
            qtd_necessaria = qtd_necessaria / 2  # Divida a quantidade necessária pela metade

        # Calcula a quantidade total a ser retirada (quantidade necessária vezes quantidade ajustada)
        total_a_retira = qtd_necessaria * quantidade_ajustada

        # Subtrai a quantidade total do estoque
        estoque[ingrediente] -= total_a_retira

        # Se o estoque do ingrediente for menor ou igual a zero, remove o ingrediente
        if estoque[ingrediente] <= 0:
            del estoque[ingrediente]

def criar_view(user_id):
    if user_id in producoes_usuario:
        producoes_usuario[user_id] = {}

    view = View(timeout=None)

    for produto in produtos:
        nome_botao = produto.replace('_', ' ').title()
        botao = Button(label=nome_botao, style=discord.ButtonStyle.primary)
        async def callback(interaction, produto=produto, nome_botao=nome_botao):
            if interaction.user.id != user_id:
                await interaction.channel.send("Esse botão não é para você.", ephemeral=True)
                return

            await interaction.response.defer()

            # Apagar qualquer mensagem de quantidade anterior, se existir
            if 'quantidade_msg' in producoes_usuario[user_id]:
                try:
                    await producoes_usuario[user_id]['quantidade_msg'].delete()
                except discord.Forbidden:
                    pass
                del producoes_usuario[user_id]['quantidade_msg']  # Remove a chave da mensagem de quantidade

            if user_id not in producoes_usuario:
                producoes_usuario[user_id] = {}

            qtd = producoes_usuario[user_id].get('quantidade_temp')
            if qtd is None:
                await interaction.channel.send("❌ Digite a quantidade no chat antes de clicar no botão.", delete_after=10)
                return

            qtd_original = qtd  # Guarda a quantidade original para comparar depois

            # Verificar se o produto é um dos específicos que queremos modificar a quantidade
            if produto in ['🍤 Espeto_camarão', '🐟 Caviar', '🍔 X-Tudo', '🥗 X-Salada', '🥪 X-Burguer','🥩 Hambúrguer','🌾 Farinha de Trigo','🍞 Pão de Hambúrguer']:
                if qtd % 2 == 1:  # Se o número for ímpar
                    qtd += 1  # Adiciona 1
                    # Envia a mensagem informando que a quantidade foi ajustada
                    mensagem_ajuste = await interaction.channel.send(
                        f"⚠️⚠️ **A quantidade foi ajustada de {qtd_original} para {qtd}**.⚠️⚠️"
                    )
                    # Armazenar a mensagem de ajuste para posterior exclusão
                    producoes_usuario[user_id]['quantidade_msg'] = mensagem_ajuste

            # Atualiza a produção do usuário com a quantidade do produto
            producoes_usuario[user_id][produto] = producoes_usuario[user_id].get(produto, 0) + qtd
            producoes_usuario[user_id]['quantidade_temp'] = None

            # Calcula o peso total da produção
            peso_total = 0
            for prod, qtd_produto in producoes_usuario[user_id].items():
                if prod not in ['quantidade_temp', 'quantidade_msg', 'producoes_msg']:
                    peso_total += produtos[prod]['peso'] * qtd_produto

            # Gera o texto da produção atual, incluindo o peso total
            texto = gerar_texto_producao(user_id)

            msg = producoes_usuario[user_id].get('producoes_msg')
            if msg:
                try:
                    await msg.delete()
                except (discord.Forbidden, discord.NotFound):
                    pass
                producoes_usuario[user_id].pop('producoes_msg', None)

            # Atualiza a produção com a nova mensagem
            producoes_usuario[user_id]['producoes_msg'] = await interaction.channel.send(
                f"✅ Adicionado **{qtd}x {nome_botao}**.\n\n{texto}"
            )

        botao.callback = callback
        view.add_item(botao)

    botao_calcular = Button(label="🧮Calcular Total", style=discord.ButtonStyle.success)

    async def calcular_callback(interaction):
        if interaction.user.id != user_id:
            await interaction.channel.send("Esse botão não é para você.", ephemeral=True)
            return

        await interaction.response.defer()

        uid_str = get_contextual_user_id(interaction)
        producoes_stock.setdefault(uid_str, {})
        estoque_final = producoes_stock[uid_str]

        producao = producoes_usuario.get(user_id, {})
        texto = gerar_texto_final(producao)

        if 'producoes_msg' in producoes_usuario[user_id]:
            try:
                await producoes_usuario[user_id]['producoes_msg'].delete()
            except discord.NotFound:
                pass
            except discord.Forbidden:
                pass  

        produtos_produzidos = {
            k: v for k, v in producoes_usuario.get(user_id, {}).items()
            if k not in ['quantidade_temp', 'quantidade_msg', 'producoes_msg']
        }

        produtos_especiais = ['🍔 X-Tudo', '🥗 X-Salada', '🥪 X-Burguer', '🥩 Hambúrguer', '🌾 Farinha de Trigo']

        # --- Verificar ingredientes insuficientes ---
        insuficientes = []
        for produto_, qtd_ in produtos_produzidos.items():
            divisor = 2 if produto_ in produtos_especiais else 1
            porcoes = qtd_ // divisor if divisor else qtd_

            for ing, qtd_receita in produtos[produto_]['ingredientes'].items():
                total_ingrediente = qtd_receita * porcoes
                disponivel = estoque_final.get(ing, 0)
                if disponivel < total_ingrediente:
                    insuficientes.append(f"{ing} (Precisa: {total_ingrediente}, Tem: {disponivel})")

        await interaction.channel.send("\nClique no botão abaixo para atualizar o estoque com a produção:")

        # Cria view com botão Atualizar Stock
        view_final = View(timeout=None)
        botao_atualizar = Button(label="🔄 Atualizar Stock", style=discord.ButtonStyle.success)

        if insuficientes:
            botao_atualizar.disabled = True
            alerta_texto = "⚠️⚠️Ingredientes insuficientes para produzir:⚠️⚠️\n• " + "\n• ".join(insuficientes)
            await interaction.channel.send(alerta_texto)
        else:
            botao_atualizar.disabled = False

        async def atualizar_stock_cb(interaction):
            if interaction.user.id != user_id:
                await interaction.response.send_message("Este botão não é para você.", ephemeral=True)
                return

            canal_nome = interaction.channel.name
            username = interaction.user.name
            uid_str = get_contextual_user_id(interaction)
            producoes_stock.setdefault(uid_str, {})
            estoque_final = producoes_stock[uid_str]

            produtos_produzidos_cb = {
                k: v for k, v in producoes_usuario.get(user_id, {}).items()
                if k not in ['quantidade_temp', 'quantidade_msg', 'producoes_msg']
            }

            produtos_especiais_cb = ['🍔 X-Tudo', '🥗 X-Salada', '🥪 X-Burguer', '🥩 Hambúrguer', '🌾 Farinha de Trigo']

            ingredientes_usados = {}

            # Verifica e atualiza ingredientes no estoque
            for produto_, qtd_ in produtos_produzidos_cb.items():
                divisor = 2 if produto_ in produtos_especiais_cb else 1
                porcoes = qtd_ // divisor if divisor else qtd_

                for ing, qtd_receita in produtos[produto_]['ingredientes'].items():
                    total_ingrediente = qtd_receita * porcoes
                    estoque_atual = estoque_final.get(ing, 0)
                    if estoque_atual < total_ingrediente:
                        await interaction.response.send_message(
                            f"❌ Ingrediente insuficiente: {ing} (Necessário: {total_ingrediente}, Disponível: {estoque_atual})",
                            ephemeral=True
                        )
                        return

                    estoque_final[ing] = estoque_atual - total_ingrediente
                    if estoque_final[ing] <= 0:
                        del estoque_final[ing]

                    ingredientes_usados[ing] = ingredientes_usados.get(ing, 0) + total_ingrediente

            # Atualiza produtos produzidos no estoque
            for produto_, qtd_ in produtos_produzidos_cb.items():
                estoque_final[produto_] = estoque_final.get(produto_, 0) + qtd_

            # Chama direto gravar_historico aqui (sem passar por salvar_estoque)
            gravar_historico(
                user_id=user_id,
                username=username,
                canal=canal_nome,
                operacao='produzir',
                adicionados=produtos_produzidos_cb,
                retirados=ingredientes_usados
            )

            # Também é bom salvar o estoque no arquivo para persistência
            salvar_estoque(producoes_stock)

            producoes_usuario[user_id] = {}  # Limpa produção temporária

            botao_atualizar.disabled = True

            await interaction.response.edit_message(content="✅ Estoque atualizado com sucesso!", view=view_final)
            await interaction.message.edit(view=view_final)


        botao_atualizar.callback = atualizar_stock_cb
        view_final.add_item(botao_atualizar)

        await interaction.channel.send(view=view_final)
        producoes_usuario[user_id]['producoes_msg'] = await interaction.channel.send(texto)

        try:
            await interaction.message.delete()
        except discord.Forbidden:
            pass

    botao_calcular.callback = calcular_callback
    view.add_item(botao_calcular)

    botao_cancelar = Button(label="❌Cancelar Produção", style=discord.ButtonStyle.danger)

    async def cancelar_callback(interaction):
        if interaction.user.id != user_id:
            await interaction.channel.send("Esse botão não é para você.", ephemeral=True)
            return

        await interaction.response.defer()

        if 'producoes_msg' in producoes_usuario[user_id]:
            try:
                await producoes_usuario[user_id]['producoes_msg'].delete()
            except discord.NotFound:
                pass  # Mensagem já não existe, pode ignorar
            except discord.Forbidden:
                pass  

        producoes_usuario[user_id] = {}
        await interaction.channel.send("🚫 Operação foi cancelada com sucesso.")

        try:
            await interaction.message.delete()
        except discord.Forbidden:
            pass

    botao_cancelar.callback = cancelar_callback
    view.add_item(botao_cancelar)

    return view

def criar_view_ingredientes(interaction: discord.Interaction) -> View:
    user_id = get_contextual_user_id(interaction)
    view = View(timeout=None)
    
    if user_id not in producoes_usuario:
        producoes_usuario[user_id] = {}

    # Botões para produzir comida ou bebida
    botao_comida = Button(label="🍽️ Produzir Comida", style=discord.ButtonStyle.primary)
    botao_bebida = Button(label="🥤 Produzir Bebida", style=discord.ButtonStyle.primary)

    # Botão para cancelar a operação (vermelho)
    botao_cancelar = Button(label="❌ Cancelar", style=discord.ButtonStyle.danger)
    # Botão para produzir (verde)
    botao_produzir = Button(label="✅ Produzir", style=discord.ButtonStyle.success)

    async def callback_comida(interaction):
        if not await tem_permissao(interaction, user_id):
            await interaction.response.send_message("Esse botão não é para você.", ephemeral=True)
            return

        await interaction.response.defer()

        producoes_usuario[user_id]['categoria_selecionada'] = 'comida'  # Armazena a categoria

        # Exibir os botões de ingredientes para comida
        view_comida = View(timeout=None)
        for ingrediente in ingredientes['comida']:  # Usando o dicionário de ingredientes para comida

            botao_ingrediente = Button(label=ingrediente, style=discord.ButtonStyle.primary)

            async def ingrediente_callback(interaction, ingrediente=ingrediente):
                if not await tem_permissao(interaction, user_id):
                    await interaction.response.send_message("Esse botão não é para você.", ephemeral=True)
                    return

                await interaction.response.defer()

                # Pega a quantidade digitada no chat
                qtd = producoes_usuario.get(interaction.user.id, {}).get("quantidade_temp")

                if qtd is None:
                    await interaction.channel.send("❌ Digite a quantidade no chat antes de clicar no botão.", delete_after=10)
                    return

                # Apagar mensagem de quantidade registrada, se houver
                if 'quantidade_msg' in producoes_usuario[user_id]:
                    try:
                        await producoes_usuario[user_id]['quantidade_msg'].delete()
                    except discord.Forbidden:
                        pass
                    del producoes_usuario[user_id]['quantidade_msg']

                # Atualiza a quantidade do ingrediente com a quantidade correta
                if ingrediente in producoes_usuario[user_id]:
                    producoes_usuario[user_id][ingrediente] += qtd  # Soma à quantidade existente
                else:
                    producoes_usuario[user_id][ingrediente] = qtd  # Inicializa a quantidade

                # Apagar a mensagem de ingredientes anterior, se houver
                if 'ingredientes_msg' in producoes_usuario[user_id]:
                    try:
                        await producoes_usuario[user_id]['ingredientes_msg'].delete()
                    except discord.Forbidden:
                        pass
                    del producoes_usuario[user_id]['ingredientes_msg']

                # Gera a lista de ingredientes acumulados
                texto_ingredientes = gerar_texto_lista_ingredientes(producoes_usuario[user_id])

                # Envia a nova mensagem com a lista de ingredientes
                msg = await interaction.channel.send(f"✅ Ingrediente **{ingrediente}** adicionado! Você tem agora **{producoes_usuario[user_id][ingrediente]}** {ingrediente}(s).\n\n{texto_ingredientes}")

                # Salva a nova mensagem
                producoes_usuario[user_id]['ingredientes_msg'] = msg

            botao_ingrediente.callback = ingrediente_callback
            view_comida.add_item(botao_ingrediente)

        # Adiciona o botão de cancelar e o botão de produzir
        view_comida.add_item(botao_cancelar)
        view_comida.add_item(botao_produzir)

        await interaction.message.edit(content="Escolha o ingrediente para comida.", view=view_comida)


    async def callback_bebida(interaction):
        if not await tem_permissao(interaction, user_id):
            await interaction.response.send_message("Esse botão não é para você.", ephemeral=True)
            return  

        await interaction.response.defer()

        producoes_usuario[user_id]['categoria_selecionada'] = 'bebida'  # Armazena a categoria

        # Exibir os botões de ingredientes para bebida
        view_bebida = View(timeout=None)
        for ingrediente in ingredientes['bebida']:  # Usando o dicionário de ingredientes para bebida

            botao_ingrediente = Button(label=ingrediente, style=discord.ButtonStyle.primary)

            async def ingrediente_callback(interaction, ingrediente=ingrediente):
                if not await tem_permissao(interaction, user_id):
                    await interaction.response.send_message("Esse botão não é para você.", ephemeral=True)
                    return

                await interaction.response.defer()

                # Pega a quantidade digitada no chat
                qtd = producoes_usuario.get(interaction.user.id, {}).get("quantidade_temp")

                if qtd is None:
                    await interaction.channel.send("❌ Digite a quantidade no chat antes de clicar no botão.", delete_after=10)
                    return

                # Apagar mensagem de quantidade registrada, se houver
                if 'quantidade_msg' in producoes_usuario[user_id]:
                    try:
                        await producoes_usuario[user_id]['quantidade_msg'].delete()
                    except discord.Forbidden:
                        pass
                    del producoes_usuario[user_id]['quantidade_msg']

                # Atualiza a quantidade do ingrediente com a quantidade correta
                if ingrediente in producoes_usuario[user_id]:
                    producoes_usuario[user_id][ingrediente] += qtd  # Soma à quantidade existente
                else:
                    producoes_usuario[user_id][ingrediente] = qtd  # Inicializa a quantidade

                # Apagar qualquer mensagem anterior de ingredientes, se existir
                if 'ingredientes_msg' in producoes_usuario[user_id]:
                    try:
                        await producoes_usuario[user_id]['ingredientes_msg'].delete()
                    except discord.Forbidden:
                        pass
                    del producoes_usuario[user_id]['ingredientes_msg']

                # Gerar a lista de ingredientes acumulados
                texto_ingredientes = gerar_texto_lista_ingredientes(producoes_usuario[user_id])

                # Envia a nova mensagem com a lista de ingredientes
                msg = await interaction.channel.send(f"✅ Ingrediente **{ingrediente}** adicionado! Você tem agora **{producoes_usuario[user_id][ingrediente]}** {ingrediente}(s).\n\n{texto_ingredientes}")

                # Salva a nova mensagem
                producoes_usuario[user_id]['ingredientes_msg'] = msg

            botao_ingrediente.callback = ingrediente_callback
            view_bebida.add_item(botao_ingrediente)

        # Adiciona o botão de cancelar e o botão de produzir
        view_bebida.add_item(botao_cancelar)
        view_bebida.add_item(botao_produzir)

        await interaction.message.edit(content="Escolha o ingrediente para bebida.", view=view_bebida)


    async def callback_cancelar(interaction):
        if not await tem_permissao(interaction, user_id):
            await interaction.response.send_message("Esse botão não é para você.", ephemeral=True)
            return

        await interaction.response.defer()

        # Cancelar a operação e apagar todas as mensagens
        producoes_usuario[user_id] = {}

        # Apaga as mensagens dos ingredientes
        if 'ingredientes_msg' in producoes_usuario[user_id]:
            try:
                await producoes_usuario[user_id]['ingredientes_msg'].delete()
            except discord.Forbidden:
                pass
            del producoes_usuario[user_id]['ingredientes_msg']

        await interaction.message.edit(content="🚫 Operação foi cancelada com sucesso.", view=None)

    async def callback_produzir(interaction):
        if not await tem_permissao(interaction, user_id):
            await interaction.response.send_message("Esse botão não é para você.", ephemeral=True)
            return

        await interaction.response.defer()

        categoria = producoes_usuario[user_id].get('categoria_selecionada')
        if not categoria:
            await interaction.channel.send("❌ Você precisa selecionar comida ou bebida antes de produzir.", ephemeral=True)
            return

        estoque = producoes_usuario[user_id]

        # Apagar todas as mensagens anteriores do canal, exceto a fixada
        async for msg in interaction.channel.history(limit=100):
            if not msg.pinned and msg.author.bot:
                try:
                    await msg.delete()
                except (discord.Forbidden, discord.NotFound):
                    pass

        # Agora envia a nova mensagem com os botões para escolher o produto
        view_produtos = View(timeout=None)
        produtos_filtrados = [p for p, dados in produtos.items() if dados['categoria'] == categoria]

        for produto in produtos_filtrados:
            nome_botao = produto.replace('_', ' ').title()
            botao_produto = Button(label=nome_botao, style=discord.ButtonStyle.primary)

            async def produto_callback(interaction, produto=produto):
                if not await tem_permissao(interaction, user_id):
                    await interaction.response.send_message("Esse botão não é para você.", ephemeral=True)
                    return

                await interaction.response.defer()

                # Pega a quantidade digitada no chat
                quantidade = producoes_usuario.get(interaction.user.id, {}).get("quantidade_temp")

                if quantidade is None:
                    await interaction.channel.send("❌ Digite a quantidade no chat antes de clicar no botão.", delete_after=10)
                    return


                # Apagar a mensagem de quantidade, se existir
                if 'quantidade_msg' in estoque:
                    try:
                        await estoque['quantidade_msg'].delete()
                    except discord.Forbidden:
                        pass
                    del estoque['quantidade_msg']

                # Apagar mensagens de erro anteriores, se houver
                if 'msg_erro' in estoque:
                    try:
                        await estoque['msg_erro'].delete()
                    except discord.Forbidden:
                        pass
                    del estoque['msg_erro']

                # Apagar mensagem de aviso anterior, se houver
                if 'msg_aviso' in estoque:
                    try:
                        await estoque['msg_aviso'].delete()
                    except discord.Forbidden:
                        pass
                    del estoque['msg_aviso']

                # Verifica se o produto é Espeto de Camarão ou Caviar
                if produto in ['🍤 Espeto_camarão', '🐟 Caviar','🍞 Pão de Hambúrguer']:
                    # Arredonda a quantidade para o múltiplo de 2 mais próximo para os dois produtos
                    quantidade_arredondada = (quantidade // 2) * 2

                    if quantidade_arredondada < 2:
                        msg_erro = await interaction.channel.send(f"❌ Você precisa de pelo menos 2 unidades para produzir {produto}.")
                        estoque['msg_erro'] = msg_erro
                        return

                    # Exibe uma mensagem de arredondamento, se houver alteração
                    if quantidade != quantidade_arredondada:
                        msg_aviso = await interaction.channel.send(f"⚠️ A quantidade foi arredondada de {quantidade} para {quantidade_arredondada} para produzir {produto}.")
                        estoque['msg_aviso'] = msg_aviso

                    quantidade = quantidade_arredondada  # Atualiza a quantidade para a arredondada

                # Para os produtos especiais X‑Tudo, X‑Salada e X‑Burger,
                # forçamos que a quantidade seja par.
                produtos_especiais = ['🍔 X-Tudo', '🥗 X-Salada', '🥪 X-Burguer','🥩 Hambúrguer','🌾 Farinha de Trigo']
                if produto in produtos_especiais:
                    quantidade_arredondada = (quantidade // 2) * 2
                    # Se o arredondamento resultar em menos de 2 unidades, não é possível produzir
                    if quantidade_arredondada < 2:
                        msg_erro = await interaction.channel.send(f"❌ Você precisa de pelo menos 2 unidades para produzir {produto}.")
                        estoque['msg_erro'] = msg_erro
                        return
                    # Se o pedido não for par, exibe um aviso e atualiza a quantidade para o valor arredondado
                    if quantidade != quantidade_arredondada:
                        msg_aviso = await interaction.channel.send(
                            f"⚠️ A quantidade foi ajustada de {quantidade} para {quantidade_arredondada} para produzir {produto}."
                        )
                        estoque['msg_aviso'] = msg_aviso
                    quantidade = quantidade_arredondada

                # Verifica se há ingredientes suficientes para produzir a quantidade (já ajustada, se for o caso)
                if pode_produzir(produto, quantidade, estoque):
                    consumir_ingredientes(produto, quantidade, estoque)

                    if 'produtos_produzidos' not in estoque:
                        estoque['produtos_produzidos'] = {}
                    estoque['produtos_produzidos'][produto] = estoque['produtos_produzidos'].get(produto, 0) + quantidade

                    # Apagar mensagem de sucesso anterior, se houver
                    if 'msg_sucesso' in estoque:
                        try:
                            await estoque['msg_sucesso'].delete()
                        except discord.Forbidden:
                            pass
                        del estoque['msg_sucesso']

                    # Envia nova mensagem de sucesso
                    msg_sucesso = await interaction.channel.send(f"✅ {quantidade}x {produto} produzido com sucesso!")
                    estoque['msg_sucesso'] = msg_sucesso

                    # Apagar mensagem de ingredientes restantes anterior, se houver
                    if 'ingredientes_restantes_msg' in estoque:
                        try:
                            await estoque['ingredientes_restantes_msg'].delete()
                        except discord.Forbidden:
                            pass
                        del estoque['ingredientes_restantes_msg']

                    # Gera o texto final atualizado
                    texto_final = gerar_texto_lista_produtos_ingredientes(estoque)
                    msg_texto = await interaction.channel.send(texto_final)
                    estoque['ingredientes_restantes_msg'] = msg_texto

                else:
                    msg_erro = await interaction.channel.send(f"❌ Ingredientes insuficientes para produzir {quantidade}x {produto}.")
                    estoque['msg_erro'] = msg_erro


            botao_produto.callback = produto_callback
            view_produtos.add_item(botao_produto)

        # Botão Finalizar
        botao_finalizar = Button(label="✅ Finalizar", style=discord.ButtonStyle.success)

        async def callback_finalizar(interaction):
            if not await tem_permissao(interaction, user_id):
                await interaction.response.send_message("Esse botão não é para você.", ephemeral=True)
                return

            await interaction.response.defer()

            # Apagar todas as mensagens anteriores do canal, exceto a mensagem fixada
            async for msg in interaction.channel.history(limit=100):
                if not msg.pinned and msg.author.bot:
                    try:
                        await msg.delete()
                    except discord.Forbidden:
                        pass

            uid_str = get_contextual_user_id(interaction)
            producoes_stock.setdefault(uid_str, {})
            estoque_final = producoes_stock[uid_str]


            estoque = producoes_usuario[user_id]
            produtos_produzidos = estoque.get('produtos_produzidos', {})

                # --- Verificação de ingredientes suficientes ---
            produtos_especiais = ['🍔 X-Tudo', '🥗 X-Salada', '🥪 X-Burguer', '🥩 Hambúrguer', '🌾 Farinha de Trigo']
            insuficientes = []

            for produto_, qtd_ in produtos_produzidos.items():
                divisor = 2 if produto_ in produtos_especiais else 1
                porcoes = qtd_ // divisor if divisor else qtd_

                for ing, qtd_receita in produtos[produto_]['ingredientes'].items():
                    total = qtd_receita * porcoes
                    disponivel = estoque_final.get(ing, 0)
                    if disponivel < total:
                        insuficientes.append(f"{ing} (Precisa: {total}, Tem: {disponivel})")

            await interaction.channel.send("\nClique no botão abaixo para atualizar o estoque com a produção:")

            # Cria o botão 🔄 Atualizar Stock
            botao_atualizar = Button(label="🔄 Atualizar Stock", style=discord.ButtonStyle.primary)

            if insuficientes:
                botao_atualizar.disabled = True
                alerta_texto = "⚠️⚠️Ingredientes insuficientes para produzir:⚠️⚠️\n• " + "\n• ".join(insuficientes)
                await interaction.channel.send(alerta_texto)
            else:
                botao_atualizar.disabled = False

            async def atualizar_stock_cb(interacao):
                if not await tem_permissao(interacao, user_id):
                    await interacao.response.send_message("Esse botão não é para você.", ephemeral=True)
                    return

                username = interacao.user.name
                canal_nome = interacao.channel.name
                uid_str = get_contextual_user_id(interacao)
                producoes_stock.setdefault(uid_str, {})
                estoque_final = producoes_stock[uid_str]

                produtos_especiais = ['🍔 X-Tudo', '🥗 X-Salada', '🥪 X-Burguer', '🥩 Hambúrguer', '🌾 Farinha de Trigo']
                ingredientes_usados = {}  # inicializar o dicionário antes do loop

                for produto_, qtd_ in produtos_produzidos.items():
                    divisor = 2 if produto_ in produtos_especiais else 1
                    porcoes = qtd_ // divisor if divisor else qtd_

                    for ing, qtd_receita in produtos[produto_]['ingredientes'].items():
                        total = qtd_receita * porcoes
                        estoque_final[ing] = estoque_final.get(ing, 0) - total
                        if estoque_final[ing] < 0:
                            estoque_final[ing] = 0

                        # registra ingredientes usados para o histórico
                        ingredientes_usados[ing] = ingredientes_usados.get(ing, 0) + total

                for produto_, qtd_ in produtos_produzidos.items():
                    estoque_final[produto_] = estoque_final.get(produto_, 0) + qtd_

                gravar_historico(
                    user_id=uid_str,
                    username=username,
                    canal=canal_nome,
                    operacao='produzir',
                    adicionados=produtos_produzidos,
                    retirados=ingredientes_usados
                )

                salvar_estoque(producoes_stock)
                await interacao.channel.send("✅ Stock atualizado com sucesso!")

                botao_atualizar.disabled = True
                await interacao.message.edit(view=view_final)

            botao_atualizar.callback = atualizar_stock_cb
            view_final = View(timeout=None)
            view_final.add_item(botao_atualizar)

            await interaction.channel.send(view=view_final)

            texto_finalizar = gerar_texto_finalizar(estoque)
            await interaction.channel.send(texto_finalizar)

        botao_finalizar.callback = callback_finalizar
        view_produtos.add_item(botao_finalizar)

        # Botão Cancelar
        botao_cancelar_final = Button(label="❌ Cancelar", style=discord.ButtonStyle.danger)

        async def callback_cancelar_final(interaction):
            if not await tem_permissao(interaction, user_id):
                await interaction.response.send_message("Esse botão não é para você.", ephemeral=True)
                return

            await interaction.response.defer()

            producoes_usuario[user_id] = {}

            # Apagar todas as mensagens anteriores do canal, exceto a mensagem fixada
            async for msg in interaction.channel.history(limit=100):
                if not msg.pinned and msg.author.bot:
                    try:
                        await msg.delete()
                    except (discord.Forbidden, discord.NotFound):
                        pass

            await interaction.channel.send("🚫 Produção cancelada com sucesso.")

        botao_cancelar_final.callback = callback_cancelar_final
        view_produtos.add_item(botao_cancelar_final)


        # Envia a mensagem para o usuário com os produtos
        if 'produtos_msg' not in estoque:
            msg_botao = await interaction.channel.send("Escolha um produto para produzir:", view=view_produtos)
            estoque['produtos_msg'] = msg_botao

        # Envia a mensagem de ingredientes restantes, mas sem a parte dos ingredientes
        texto_final = gerar_texto_lista_produtos_ingredientes(estoque)
        msg_texto = await interaction.channel.send(texto_final)
        estoque['ingredientes_restantes_msg'] = msg_texto

    # Define os callbacks para os botões de comida, bebida, cancelar e produzir
    botao_comida.callback = callback_comida
    botao_bebida.callback = callback_bebida
    botao_cancelar.callback = callback_cancelar
    botao_produzir.callback = callback_produzir

    # Adiciona os botões de comida e bebida
    view.add_item(botao_comida)
    view.add_item(botao_bebida)

    return view

def gerar_texto_lista_ingredientes(dados_usuario):
    texto = "📦 Ingredientes adicionados até agora:\n"
    peso_total = 0

    # Percorrendo os ingredientes no 'dados_usuario'
    for item, qtd in dados_usuario.items():
        if item in pesos_ingredientes:  # Verifica se o item está no dicionário de pesos de ingredientes
            if qtd > 0:  # Só processa se a quantidade for maior que 0
                peso_ingrediente = pesos_ingredientes.get(item, 0)  # Obtém o peso do ingrediente
                peso_item = peso_ingrediente * qtd  # Peso total do ingrediente
                texto += f"- {item}: {qtd} unidades - Peso: {peso_item}kg\n"
                peso_total += peso_item  # Soma o peso total

    if texto.strip() == "📦 Ingredientes adicionados até agora:":
        texto += "Nenhum ingrediente adicionado ainda."

    texto += f"\n⚖️ Peso Total: {peso_total}kg"
    return texto

def gerar_texto_lista_produtos_ingredientes(dados_usuario):
    texto = "📦 Produtos a produzir:\n"
    produtos_produzidos = dados_usuario.get('produtos_produzidos', {})
    ingredientes_usados = {}
    peso_total_produtos = 0  # Peso total dos produtos a produzir
    peso_total_ingredientes_restantes = 0  # Peso total dos ingredientes restantes
    especial = False

    produtos_especiais = ['🍔 X-Tudo', '🥗 X-Salada', '🥪 X-Burguer','🥩 Hambúrguer','🌾 Farinha de Trigo']

    if produtos_produzidos:
        for produto, qtd in produtos_produzidos.items():
            texto += f"- {produto}: {qtd} unidades - Peso: {produtos[produto]['peso'] * qtd}kg\n"
            peso_total_produtos += produtos[produto]['peso'] * qtd  # Soma o peso total dos produtos

            porcoes = qtd //2 if produto in produtos_especiais else qtd  # Ajuste para produtos especiais

            for ingrediente, quantidade_receita in produtos[produto]['ingredientes'].items():
                if produto in produtos_especiais:
                    quantidade_receita /= 2  # Ajusta para produtos especiais, se necessário

                total_ingrediente = quantidade_receita * porcoes
                if produto in produtos_especiais:
                    ingredientes_usados[ingrediente] = ingredientes_usados.get(ingrediente, 0) + total_ingrediente
                    especial = True

    else:
        texto += "Nenhum produto adicionado ainda.\n"
    texto += f"\n⚖️ Peso Total dos Produtos a Produzir: {peso_total_produtos}kg\n\n"

    # Ingredientes restantes
    texto += "\n📝 Ingredientes restantes:\n"
    encontrou = False

    for ingrediente in ingredientes['comida'] + ingredientes['bebida']:
        if ingrediente in dados_usuario:
            if especial == True:
                restante = int(round(dados_usuario[ingrediente] - ingredientes_usados.get(ingrediente, 0)))
            else:    
                restante = int(round(dados_usuario[ingrediente]))
            if restante > 0:
                peso_ingrediente = pesos_ingredientes.get(ingrediente, 0)
                peso_restante = round(peso_ingrediente * restante, 2)
                texto += f"- {ingrediente}: {restante} unidades - Peso: {peso_restante}kg\n"
                peso_total_ingredientes_restantes += round(peso_restante)
                encontrou = True

    if not encontrou:
        texto += "Nenhum ingrediente restante."

    # Exibe o peso total dos produtos a produzir e o peso total dos ingredientes restantes
    texto += f"\n⚖️ Peso Total dos Ingredientes Restantes: {peso_total_ingredientes_restantes}kg"

    return texto

def gerar_texto_finalizar(dados_usuario):
    texto = "\n📦 Produtos Finalizados:\n"
    produtos_produzidos = dados_usuario.get('produtos_produzidos', {})
    peso_total = 0

    if produtos_produzidos:
        for produto, qtd in produtos_produzidos.items():
            peso_produto = produtos[produto]['peso'] * qtd  # Calcula o peso do produto
            peso_total += peso_produto
            texto += f"- {produto}: {qtd} - Peso {produtos[produto]['peso']}kg\n"
    else:
        texto += "Nenhum produto foi finalizado.\n"

    texto += f"\n⚖️ Peso Total dos produtos finalizados: {peso_total:.2f}kg"
    return texto

def gerar_texto_producao(user_id: int) -> str:
    dados = producoes_usuario.get(user_id, {})
    if not dados:
        return "❌ Nenhum item em produção."

    linhas = []
    peso_total = 0

    for item, qtd in dados.items():
        if not isinstance(qtd, (int, float)):
            continue  # ignora valores inválidos

        peso = 0
        if item in produtos:
            peso = produtos[item]["peso"]
        elif item in pesos_ingredientes:
            peso = pesos_ingredientes[item]

        subtotal = peso * qtd
        peso_total += subtotal
        linhas.append(f"**{item}** x{qtd} - {subtotal:.2f}kg")

    linhas.append(f"\n**⚖️ Peso atual da produção:** {peso_total:.2f} kg")
    return "\n".join(linhas)

def gerar_texto_final(producao):
    linhas = ["**🍖 Resumo Final da Produção:**"]
    peso_total_produtos = 0
    ingredientes_totais = {}
    peso_total_ingredientes = 0

    produtos_especiais = ['🍔 X-Tudo', '🥗 X-Salada', '🥪 X-Burguer','🌾 Farinha de Trigo']

    for produto, qtd in producao.items():
        if produto in ['quantidade_temp', 'quantidade_msg', 'producoes_msg']:
            continue
        if qtd > 0:
            peso_produto = produtos[produto]['peso'] * qtd
            peso_total_produtos += peso_produto
            linhas.append(f"\n__**{produto.replace('_', ' ').title()}**__: {qtd} unidade(s)")

            # Reduzir ingredientes para metade se for produto especial
            divisor = 2 if produto in produtos_especiais else 1

            for ingrediente, quantidade in produtos[produto]['ingredientes'].items():
                total_ingrediente = (quantidade * qtd) // divisor
                ingredientes_totais[ingrediente] = ingredientes_totais.get(ingrediente, 0) + total_ingrediente

    linhas.append(f"\n**⚖️ Peso total dos produtos:** {peso_total_produtos:.2f} kg")

    if not ingredientes_totais:
        return "Nenhum item produzido ainda."

    linhas.append("\n**🥦 Ingredientes totais por item:**")
    for ingrediente, total in ingredientes_totais.items():
        peso_individual = pesos_ingredientes.get(ingrediente, 0)
        peso_ingrediente_total = peso_individual * total
        peso_total_ingredientes += peso_ingrediente_total
        linhas.append(f"- {ingrediente}: {total} unidades - {peso_ingrediente_total:.2f} kg")

    linhas.append(f"\n**⚖️ Peso total dos ingredientes:** {peso_total_ingredientes:.2f} kg")

    return "\n".join(linhas)

def criar_view_inicial(user_id):
    view = View(timeout=None)

    # Botões para escolha da produção
    botao_produtos = Button(label="Produzir por Produtos", style=discord.ButtonStyle.primary)
    botao_ingredientes = Button(label="Produzir por Ingredientes", style=discord.ButtonStyle.primary)
    botao_stock = Button(label="Estoque", style=discord.ButtonStyle.primary)
    async def callback_produtos(interaction):
        if interaction.user.id != user_id:
            await interaction.channel.send("Esse botão não é para você.", ephemeral=True)
            return

        await interaction.response.defer()

        # Enviar a mensagem com os botões de produtos
        view_produtos = criar_view(user_id)
        await interaction.message.edit(content="Escolha o produto que você deseja produzir.", view=view_produtos)

    async def callback_ingredientes(interaction):
        if interaction.user.id != user_id:
            await interaction.channel.send("Esse botão não é para você.", ephemeral=True)
            return

        await interaction.response.defer()

        # Enviar a mensagem com os botões de ingredientes
        view_ingredientes = criar_view_ingredientes(interaction)
        await interaction.message.edit(content="Escolha o ingrediente que você deseja produzir.", view=view_ingredientes)

    async def callback_stock(interaction):
        if interaction.user.id != user_id:
            await interaction.channel.send("Esse botão não é para você.", ephemeral=True)
            return

        await interaction.response.defer()
        await interaction.message.delete()

        # Enviar a mensagem com os botões de produtos
        view_stock = criar_view_stock(interaction)
        await interaction.channel.send(content="Escolha o produto que você deseja produzir.", view=view_stock)



    # Atribuindo as callbacks aos botões
    botao_produtos.callback = callback_produtos
    botao_ingredientes.callback = callback_ingredientes
    botao_stock.callback = callback_stock

    # Adiciona os botões na view
    view.add_item(botao_produtos)
    view.add_item(botao_ingredientes)
    view.add_item(botao_stock)

    return view

def criar_view_botao_produzir(user_id: int) -> View:
    view = View(timeout=None)
    botao = Button(label="🚀 Produzir", style=discord.ButtonStyle.success)

    async def callback(interaction: discord.Interaction):
        if interaction.user.id != user_id:
            await interaction.channel.send("Esse botão não é para você.", ephemeral=True)
            return

        await interaction.response.defer()

        # Apaga mensagens antigas do bot
        async for msg in interaction.channel.history(limit=100):
            if not msg.pinned and msg.author.bot:
                try:
                    await msg.delete()
                except (discord.Forbidden, discord.NotFound):
                    pass

        # 🔁 Corrigido: Carrega o JSON e inicializa o stock do usuário corretamente
        global producoes_stock
        producoes_stock.clear()
        producoes_stock.update(carregar_estoque())
        producoes_stock.setdefault(user_id, {})  # garante dicionário vazio se novo

        # Abre o menu inicial
        view_inicial = criar_view_inicial(user_id)
        await interaction.channel.send("Escolha como deseja produzir:", view=view_inicial)

    botao.callback = callback
    view.add_item(botao)
    return view

def criar_view_stock(interaction:discord.Interaction) -> View:
    view = View(timeout=None)
    user_id = get_contextual_user_id(interaction)

    # ---------- helpers ----------
    produtos_ingredientes = ['🥩 Hambúrguer', '🍞 Pão de Hambúrguer', '🌾 Farinha de Trigo']

    def adicionar(user_id: int, item: str, qtd: int):
        user_id = str(user_id)
        producoes_stock.setdefault(user_id, {})
        atual = producoes_stock[user_id].get(item, 0)
        producoes_stock[user_id][item] = atual + qtd

        if item in produtos_ingredientes:
            producoes_stock[user_id][item] = producoes_stock[user_id][item]

        salvar_estoque(producoes_stock) 
       
        gravar_historico(
            user_id=user_id,
            username=interaction.user.name,
            canal=interaction.channel.name,
            operacao="adicionar",
            adicionados={item: qtd},  # 1 foi adicionado
            retirados={}
            )
        
        return f"✅ Adicionado {qtd}x **{item}** ao estoque."
       
    def remover(user_id: int, item: str, qtd: int):
        user_id = str(user_id)
        if user_id not in producoes_stock or item not in producoes_stock[user_id]:
            return
        atual = producoes_stock[user_id][item]
        novo = max(0, atual - qtd)
        producoes_stock[user_id][item] = novo

        # Se for produto-ingrediente, sincroniza ambos
        if item in produtos_ingredientes:
            producoes_stock[user_id][item] = producoes_stock[user_id][item]

        salvar_estoque(producoes_stock)

        gravar_historico(
            user_id=user_id,
            username=interaction.user.name,
            canal=interaction.channel.name,
            operacao="remover",
            adicionados={},
            retirados={item: qtd}  # 1 foi retirado
            )

        return f"❌ Removido {qtd}x **{item}** do estoque."

    async def pede_quantidade(inter, nome_obj):
        await inter.channel.send(
            f"❌ Digite a quantidade no chat antes de clicar em **{nome_obj}**.",
            delete_after=10
        )

    async def obter_quantidade(interaction):
        qtd = producoes_usuario.get(interaction.user.id, {}).get("quantidade_temp")
        if qtd is None:
            await interaction.response.send_message(
                "❌ Digite a quantidade no chat antes de clicar no botão.",
                ephemeral=True
            )
            return None
        return qtd

    async def limpa_quantidade_msg(uid: int):
        """Apaga (se existir) a mensagem que confirma a quantidade digitada."""
        ref = producoes_stock.get(uid, {}).pop("quantidade_msg", None)
        if ref:
            try:
                await ref.delete()
            except (discord.Forbidden, discord.NotFound):
                pass

    def peso_item(nome: str) -> float:
        if nome in produtos:
            return produtos[nome]["peso"]
        if nome in pesos_ingredientes:
            return pesos_ingredientes[nome]
        return 0

    # ---------- apagar mensagens antigas ----------
    async def apagar_stock_antigo():
        if user_id in mensagens_stock:
            for msg in mensagens_stock[user_id]:
                try:
                    await msg.delete()
                except Exception:
                    pass
            mensagens_stock.pop(user_id)

    async def apagar_historico_antigo():
        if user_id in mensagens_historico:
            for msg in mensagens_historico[user_id]:
                try:
                    await msg.delete()
                except:
                    pass
            mensagens_historico.pop(user_id)

    # ---------- MENU PRINCIPAL ----------
    async def volta_menu(inter):
        await apagar_historico_antigo()
        await limpa_quantidade_msg(user_id)
        await limpa_acao_msg(user_id)
        await apagar_stock_antigo()
        await inter.message.delete()
        await inter.channel.send(
            "Escolha uma opção:", view=criar_view_stock(inter)
        )

    # ---------- SUB‑MENUS ----------
    async def abre_submenu(inter, colecao, titulo):
        await apagar_historico_antigo()
        await limpa_quantidade_msg(user_id)
        await limpa_acao_msg(user_id)
        await apagar_stock_antigo()
        await inter.message.delete()

        nova = View(timeout=None)
        for item in colecao:
            rotulo = item.replace('_', ' ').title()
            bot = Button(label=rotulo, style=discord.ButtonStyle.primary)

            async def item_cb(i, produto=item, nome=rotulo):
                # Apaga a mensagem da quantidade digitada assim que o botão é clicado
                await limpa_quantidade_msg(user_id)
                await limpa_acao_msg(user_id)

                qtd = producoes_usuario.get(interaction.user.id, {}).get("quantidade_temp")
                if not isinstance(qtd, int) or qtd <= 0:
                    await pede_quantidade(i, nome)
                    return

                # View para escolha adicionar ou remover
                acao = View(timeout=None)
                bt_add = Button(label="✅ Adicionar", style=discord.ButtonStyle.success)
                bt_rem = Button(label="❌ Remover",  style=discord.ButtonStyle.danger)

                async def add_cb(inter, prod=produto):
                    # Apaga mensagem da quantidade novamente ao clicar em "Adicionar"
                    await limpa_quantidade_msg(user_id)
                    await limpa_acao_msg(user_id)

                    if not await tem_permissao(inter,user_id):
                        await inter.response.send_message("Esse botão não é para você.", ephemeral=True)
                        return

                    qtd = await obter_quantidade(inter)
                    if qtd is None:
                        return

                    adicionar(user_id, prod, qtd)
                    producoes_stock[user_id].pop("quantidade_temp", None)

                    await inter.message.delete()
                    msg = await inter.channel.send(f"✅ Adicionado {qtd}x **{prod}**.")
                    producoes_stock[user_id]['acao_msg'] = msg 

                async def rem_cb(inter, prod=produto):
                    # Apaga mensagem da quantidade novamente ao clicar em "Remover"
                    await limpa_quantidade_msg(user_id)
                    await limpa_acao_msg(user_id)

                    if not await tem_permissao(interaction,user_id):
                        await inter.response.send_message(
                            "Esse botão não é para você.", ephemeral=True
                        )
                        return

                    qtd = await obter_quantidade(inter)
                    if qtd is None:
                        return

                    remover(user_id, prod, qtd)
                    producoes_stock[user_id].pop("quantidade_temp", None)

                    await inter.message.delete()
                    msg = await inter.channel.send(f"❌ Removido {qtd}x **{prod}**.")
                    producoes_stock[user_id]['acao_msg'] = msg

                bt_add.callback, bt_rem.callback = add_cb, rem_cb
                acao.add_item(bt_add)
                acao.add_item(bt_rem)
                await i.channel.send(f"O que fazer com **{qtd}x {nome}**?", view=acao)

            bot.callback = item_cb
            nova.add_item(bot)

        bt_back = Button(label="🔙 Voltar", style=discord.ButtonStyle.secondary)
        bt_back.callback = volta_menu
        nova.add_item(bt_back)

        await inter.channel.send(titulo, view=nova)

    # ---------- botões principais ----------
    bt_prod = Button(label="🛒 Produtos", style=discord.ButtonStyle.primary)
    bt_prod.callback = lambda i: abre_submenu(i, produtos, "🛒 Escolha um produto:")

    bt_beb = Button(label="🥤 Ingredientes Bebida", style=discord.ButtonStyle.secondary)
    bt_beb.callback = lambda i: abre_submenu(i, ingredientes["bebida"], "🥤 Escolha um ingrediente de bebida:")

    bt_com = Button(label="🍽️ Ingredientes Comida", style=discord.ButtonStyle.secondary)
    bt_com.callback = lambda i: abre_submenu(i, ingredientes["comida"], "🍽️ Escolha um ingrediente de comida:")

    bt_stock_main = Button(label="📦 Ver Stock", style=discord.ButtonStyle.success)
    bt_limpar = Button(label="🧹 Limpar Stock", style=discord.ButtonStyle.danger)

    async def limpar_cb(inter):
        if not await tem_permissao(interaction,user_id):
            await inter.response.send_message("Esse botão não é para você.", ephemeral=True)
            return

        confirm_view = View(timeout=30)
        bt_sim = Button(label="✅ Sim", style=discord.ButtonStyle.success)
        bt_nao = Button(label="❌ Não", style=discord.ButtonStyle.secondary)

        async def sim_cb(i):
            # Limpa dados
            await apagar_stock_antigo()
            if user_id in producoes_stock:
                producoes_stock[user_id].clear()
            else:
                producoes_stock[user_id] = {}
            salvar_estoque(producoes_stock)

            gravar_historico(
                user_id=user_id,
                username=interaction.user.name,
                canal=interaction.channel.name,
                operacao="limpar",
                adicionados={},
                retirados={"TODOS": "tudo"}
            )

            # Tenta apagar mensagem de confirmação
            try:
                await i.message.delete()
            except discord.NotFound:
                pass

            # Reenvia a tela de stock zerado com o botão "Limpar Stock"
            await stock_main_cb(i)

        async def nao_cb(i):
            await i.message.delete()

        bt_sim.callback = sim_cb
        bt_nao.callback = nao_cb
        confirm_view.add_item(bt_sim)
        confirm_view.add_item(bt_nao)

        msg = await inter.channel.send("⚠️ Tem certeza que deseja limpar **todo o seu stock**?", view=confirm_view)
        mensagens_stock.setdefault(user_id, []).append(msg)

    bt_limpar.callback = limpar_cb
    async def stock_main_cb(inter):
        await apagar_historico_antigo()
        await limpa_quantidade_msg(user_id)
        await limpa_acao_msg(user_id)
        if not await tem_permissao(interaction,user_id):
            await inter.response.send_message("Esse botão não é para você.", ephemeral=True)
            return

        await apagar_stock_antigo()

        # Ajuste de colunas
        col_nome = 19  # Reduzido de 28 → para reduzir espaço entre nome e quantidade
        col_q    = 4
        col_kg   = 6

        stock = producoes_stock.get(user_id, {})

        def alinhar(nome, qtd, peso, usar_uni=True):
            qtd_str = f"{qtd}" if not usar_uni else f"{qtd}"
            return f"{nome:<{col_nome}} | {qtd_str:>{col_q}} | {peso:>{col_kg}.2f}kg"

        # --- Ingredientes ---
        ingr_linhas = []
        for ing in ingredientes["comida"] + ingredientes["bebida"]:
            q = stock.get(ing, 0)
            kg = peso_item(ing) * q
            nome_corrigido = f" {ing}    " if ing.startswith("☕") else ing
            ingr_linhas.append(alinhar(nome_corrigido, q, kg, usar_uni=False))

        titulo_ing = f"{'Ingredientes ':<{col_nome}}  | {'Qtd  ':>{col_q}}| {'Peso':>{col_kg}}"
        sep_ing = "-" * len(titulo_ing)+ "--"

        texto_ing = "📋 **Ingredientes no estoque**\n"
        texto_ing += "```\n"
        texto_ing += titulo_ing + "\n" + sep_ing + "\n"
        texto_ing += "\n".join(ingr_linhas)
        texto_ing += "\n```"

        # --- Produtos ---
        prod_linhas = []
        for prod in produtos:
            q = stock.get(prod, 0)
            kg = peso_item(prod) * q
            nome_corrigido = f" {prod}             " if prod == "☕ Café" else prod  # espaço extra só aqui
            prod_linhas.append(alinhar(nome_corrigido, q, kg, usar_uni=True))

        titulo_prod = f"{'Produtos':<{col_nome}}  | {'Qtd':>{col_q}} | {'Peso':>{col_kg}}"

        sep_prod = "-" * len(titulo_prod) + "--"

        texto_prod = "📦 **Produtos no estoque**\n"
        texto_prod += "```\n"
        texto_prod += titulo_prod + "\n" + sep_prod + "\n"
        texto_prod += "\n".join(prod_linhas)
        texto_prod += "\n```"

        # Envio das mensagens
        mensagens = []
        msg_1 = await inter.channel.send(texto_ing)
        msg_2 = await inter.channel.send(texto_prod)

        # Botão de limpar
        botao_view = View(timeout=None)
        botao_view.add_item(bt_limpar)
        msg_3 = await inter.channel.send("🧹 Deseja limpar o stock atual?", view=botao_view)

        mensagens.extend([msg_1, msg_2, msg_3])
        mensagens_stock[user_id] = mensagens

    bt_stock_main.callback = stock_main_cb

        # ---------- BOTÃO: VER HISTÓRICO ----------
    bt_historico = Button(label="📜 Ver Histórico", style=discord.ButtonStyle.secondary)

    async def historico_cb(inter):
        await apagar_historico_antigo()
        await limpa_quantidade_msg(user_id)
        canal_atual = inter.channel.name  # exemplo: "gestão-laricas"
        historico = obter_historico()

        # FILTRAR: apenas entradas que tenham canal igual ao atual
        entradas = [h for h in historico if h.get("canal") == canal_atual]

        if not entradas:
            await inter.channel.send(
                f"📭 Nenhum histórico encontrado para este canal (`{canal_atual}`).",
                delete_after=5
            )
            return
        
    # Configurações de largura fixas para alinhamento
        col_user_oper = 20  # largura total para nome + seta + operação
        col_prod = 22

        linhas = []
        for h in entradas[-15:]:
            user = h.get("username", "Desconhecido")
            oper = h.get("operacao", "—").upper()

            # Cria string "nome → OPERACAO" com só 1 espaço antes da seta, sem ljust no nome
            user_oper = f"{user} → {oper}"

            adicionados = h.get("adicionados", {})
            retirados = h.get("retirados", {})

            if oper == "PRODUZIR":
                produto = next(iter(adicionados.keys()), None)
                qtd_prod = adicionados.get(produto, None) if produto else None
                produto_str = f"{produto} x{qtd_prod}" if produto else "-"

                ingredientes_usados = ", ".join(f"{k} x{v}" for k, v in retirados.items()) if retirados else "-"

                # Ajusta espaçamento: alinha o user_oper para manter barra alinhada
                parte_1 = user_oper.ljust(col_user_oper)
                produto_formatado = produto_str.ljust(col_prod)

                linha = f"{parte_1}| {produto_formatado}| {ingredientes_usados}"

            elif oper == "LIMPAR":
                # Caso especial: se for limpar estoque, mostra só TODOS sem 'x tudo'
                parte_1 = user_oper.ljust(col_user_oper)
                linha = f"{parte_1}| TODOS"

            else:
                itens = []
                if adicionados:
                    itens += [f"{k} x{v}" for k, v in adicionados.items()]
                if retirados:
                    itens += [f"{k} x{v}" for k, v in retirados.items()]

                itens_str = ", ".join(itens) if itens else "-"

                parte_1 = user_oper.ljust(col_user_oper)
                linha = f"{parte_1}| {itens_str}"

            linhas.append(linha)

        texto = "```\n" + "\n".join(linhas) + "\n```"
        msg = await inter.channel.send(f"📜 **Histórico de Movimentações**\n{texto}")
        mensagens_historico.setdefault(user_id, []).append(msg)

    bt_historico.callback = historico_cb

    for b in (bt_prod, bt_beb, bt_com, bt_stock_main, bt_historico):
        view.add_item(b)
    
    return view

def get_contextual_user_id(interaction: discord.Interaction) -> str:
    canal_nome = interaction.channel.name.lower()
    if canal_nome == "gestão-laricas":
        return "1"  # ID especial do restaurante
    return str(interaction.user.id)  # ID da pessoa

async def tem_permissao(interaction: discord.Interaction, user_id: str):
    channel = interaction.channel
    user = interaction.user

    if channel.name == "gestão-laricas":
        cargo_permitido = any(c.name.lower() in ['gerente', 'chefe'] for c in user.roles)
        return cargo_permitido
    else:
        # No canal normal, verifica se o usuário que interagiu é o dono da produção
        return str(user.id) == str(user_id)

async def limpa_acao_msg(uid: int):
    """Apaga (se existir) a mensagem '✅ …' ou '❌ …'."""
    ref = producoes_stock.get(uid, {}).pop("acao_msg", None)
    if ref:
        try:
            await ref.delete()
        except (discord.Forbidden, discord.NotFound):
            pass   

def salvar_estoque(dados: dict[int, dict], canal_nome: str | None = None):
    filtrado: dict[str, dict] = {}

    # Se canal_nome for 'gestão-laricas', salva só o ID 1
    salvar_so_id_1 = canal_nome and canal_nome.lower() == "gestão-laricas"

    for uid_int, user_data in dados.items():
        if salvar_so_id_1 and str(uid_int) != "1":
            continue  # ignora todos exceto o ID 1

        limpo = {
            k: v for k, v in user_data.items()
            if k != "quantidade_temp" and not k.endswith("_msg")
               and isinstance(v, (numbers.Number, str, list, dict))
        }

        if limpo:  # só grava se tiver dados
            filtrado[str(uid_int)] = limpo

    with open(ARQ_STOCK, "w", encoding="utf-8") as f:
        json.dump(filtrado, f, ensure_ascii=False, indent=4)

def finalizar_producao(user_id: int):
    dados = producao_temp.get(user_id, {})
    if not dados:
        return "❌ Nada foi produzido."

    for item, qtd in dados.items():
        producoes_stock.setdefault(user_id, {})
        producoes_stock[user_id][item] = producoes_stock[user_id].get(item, 0) + qtd

    salvar_estoque(producoes_stock)
    producao_temp[user_id] = {}  # limpa o temporário
    return "✅ Produção finalizada e salva no estoque!"

@bot.command()
async def produzir(ctx):
    try:
        await ctx.message.delete()
    except (discord.Forbidden, discord.NotFound):
        pass                 

    if 'produção' not in ctx.channel.name.lower() and 'gestão' not in ctx.channel.name.lower():
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send("❌ Este comando não está disponível nesta sala.", delete_after=10)
        return

    member = ctx.author
    producoes_usuario[member.id] = {}

    # Apaga mensagem antiga com o botão, se existir
    async for msg in ctx.channel.history(limit=10):
        if msg.author == ctx.bot.user and "Clique no botão abaixo para iniciar sua produção:" in msg.content:
            try:
                await msg.delete()
            except:
                pass
            break

    async for msg in ctx.channel.history(limit=None):  # Pega todas as mensagens do canal
        if not msg.pinned:  # Só apaga se a mensagem não estiver fixada
            try:
                await msg.delete()
            except (discord.Forbidden, discord.NotFound):
                pass

    # Envia a nova mensagem com o botão
    view_produzir = criar_view_botao_produzir(member.id)
    msg_produzir = await ctx.channel.send(
        "**Clique no botão abaixo para iniciar sua produção:**",
        view=view_produzir
    )
    try:
        await msg_produzir.pin()
    except:
        pass

    # Apaga a mensagem do comando !produzir
    try:
        await ctx.message.delete()
    except:
        pass

@bot.command()
async def iniciar(ctx):
    # Verifica se o comando !iniciar está sendo usado no canal 'iniciar'
    if ctx.channel.name != 'iniciar':
        # Apaga a última mensagem do usuário (o comando !iniciar)
        try:
            await ctx.message.delete()
        except (discord.Forbidden, discord.NotFound):  # Tratando ambos os erros
            pass

        # Envia a mensagem de erro
        await ctx.send("❌ Este comando não está disponível nesta sala.", delete_after=5)
        return

    guild = ctx.guild
    member = ctx.author

    # Apaga todas as mensagens do canal, exceto as fixadas
    async for message in ctx.channel.history(limit=None):
        if not message.pinned:
            try:
                await message.delete()
            except discord.Forbidden:
                pass

    categoria_producoes = discord.utils.get(guild.categories, name="Produções")
    if not categoria_producoes:
        categoria_producoes = await guild.create_category("Produções")

    # Atualizar permissões para que ninguém, exceto o criador e o bot, receba notificações sonoras
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
        member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        bot.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
    }

    # Impede que admins escrevam, mas permite que leiam
    for role in guild.roles:
        if role != guild.default_role and role.permissions.administrator:
            perms = discord.PermissionOverwrite()
            perms.read_messages = True
            perms.send_messages = False
            overwrites[role] = perms

    # Criar o canal
    channel_name = f'produção-{member.name.lower()}'
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if existing_channel:
        await existing_channel.send(f"🔄 {member.mention}, você já possui um canal de produção.", delete_after=10)
        return

    # Criar o canal de produção
    new_channel = await guild.create_text_channel(
        channel_name, 
        overwrites=overwrites, 
        category=categoria_producoes
    )
    await new_channel.send(f"✅ Canal de produção criado com sucesso! Comece sua produção, {member.mention}.")


    # Garantir que a categoria esteja com permissões restritas
    await categoria_producoes.set_permissions(guild.default_role, read_messages=False, send_messages=False)

    try:
        file = discord.File("producao.png", filename="producao.png")  # imagem local
        foto = await new_channel.send(file=file)
        await foto.pin()
    except Exception as e:
        print(f"Erro ao enviar imagem ou fixar de produção: {e}")

    if not member.guild_permissions.administrator:
        await ctx.channel.set_permissions(member, read_messages=False)
    
    # Enviar e fixar a mensagem inicial no novo canal
    mensagem_inicial = await new_channel.send("📌 **Em caso de algum problema use `!produzir`**")
    mensagem_inicial_2 = await new_channel.send("Se o não estiver  conseguindo resolver fale com algum adm.")
    try:
        await mensagem_inicial.pin()
        await mensagem_inicial_2.pin()
    except discord.Forbidden:
        pass

    view_produzir = criar_view_botao_produzir(member.id)
    msg_produzir = await new_channel.send(
        "**Clique no botão abaixo para iniciar sua produção:**",
        view=view_produzir
    )
    try:
        await msg_produzir.pin()          # se quiser fixar esse já
    except discord.Forbidden:
        pass

    if not member.guild_permissions.administrator:
        await ctx.channel.set_permissions(member, read_messages=False)

    try:
        await ctx.message.delete()
    except (discord.Forbidden, discord.NotFound):  # Tratando ambos os erros
        pass

@bot.command()
async def laricas(ctx):
    global canal_laricas_id

    cargos_permitidos = ["Gerente", "Chefe"]
    cargos_usuario = [role.name for role in ctx.author.roles]

    if not any(cargo in cargos_usuario for cargo in cargos_permitidos):
        await ctx.send("❌ Você não tem permissão para usar este comando.", delete_after=10)
        return

    guild = ctx.guild
    member = ctx.author

    canal = None

    # Verifica se existe a categoria
    categoria = discord.utils.get(guild.categories, name="Gestão Laricas")
    if categoria:
        canal = discord.utils.get(categoria.channels, name="gestão-laricas")


    if canal is None:
        # Criar categoria se não existir
        categoria = discord.utils.get(guild.categories, name="Gestão Laricas")
        if not categoria:
            categoria = await guild.create_category("Gestão Laricas")

        # Definir permissões para o canal Laricas
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
        }
        for role in guild.roles:
            if role.name in cargos_permitidos:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        overwrites[bot.user] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        canal = await guild.create_text_channel("gestão-laricas", category=categoria, overwrites=overwrites)
        canal_laricas_id = canal.id

        cargos_mention = " ".join(role.mention for role in guild.roles if role.name in cargos_permitidos)
        await canal.send(f"✅ Canal de produção do Laricas criado com sucesso! {cargos_mention}")

        # Aqui envia imagem, pins e menu APENAS na criação do canal
        try:
            file = discord.File("producao.png", filename="producao.png")  # imagem local
            foto = await canal.send(file=file)
            await foto.pin()
        except Exception as e:
            print(f"Erro ao enviar imagem ou fixar de produção: {e}")

        mensagem_inicial = await canal.send("📌 **Em caso de algum problema use `!produzir`**")
        mensagem_inicial_2 = await canal.send("Se não estiver conseguindo resolver fale com algum adm.")
        try:
            await mensagem_inicial.pin()
            await mensagem_inicial_2.pin()
        except discord.Forbidden:
            pass

        view_produzir = criar_view_botao_produzir(member.id)
        msg_produzir = await canal.send(
            "**Clique no botão abaixo para iniciar sua produção:**",
            view=view_produzir
        )
        try:
            await msg_produzir.pin()
        except discord.Forbidden:
            pass

        if not member.guild_permissions.administrator:
            await ctx.channel.set_permissions(member, read_messages=False)

    else:
        # Se canal já existe, só manda uma mensagem discreta ou só ignora, sem reenviar menu e imagens
        await ctx.send(f" Já pode usar o canal de produção do Laricas: {canal.mention}", delete_after=10)

    try:
        await ctx.message.delete()
    except (discord.Forbidden, discord.NotFound):
        pass

@bot.command()
async def testarnick(ctx):
    try:
        await ctx.author.edit(nick="Teste Nick")
        await ctx.send("✅ Nick alterado com sucesso!")
    except discord.Forbidden:
        await ctx.send("❌ Não tenho permissão para alterar o teu apelido.")
    except Exception as e:
        await ctx.send(f"⚠️ Ocorreu um erro: {e}")

@bot.event
async def on_message(message):
    if message.type == discord.MessageType.pins_add:
        try:
            await message.delete()        # remove o aviso
        except discord.Forbidden:
            pass                          # sem permissão para apagar
        return                            # não processa comandos nesse aviso


    if message.author == bot.user:
        return

    user_id = message.author.id
    content = message.content.lower().strip()

    # ----------- Lógica de HIERARQUIA ------------
    if message.channel.name.lower() == "hierarquia":
        nome = passaporte = cargo_texto = None
        linhas = message.content.splitlines()

        for linha in linhas:
            if linha.lower().startswith("nome:"):
                nome = linha.split(":", 1)[1].strip()
            elif linha.lower().startswith("passaporte:"):
                passaporte = linha.split(":", 1)[1].strip()
            elif linha.lower().startswith("cargo:"):
                cargo_texto = linha.split(":", 1)[1].strip()

        def normalizar_cargo(texto):
            texto = texto.lower()
            if "estagi" in texto:
                return "Estagiário"
            elif "chef" in texto:
                return "Chefe"
            elif "gerent" in texto:
                return "Gerente"
            else:
                return None

        cargo_normalizado = normalizar_cargo(cargo_texto)

        if nome and passaporte and cargo_normalizado:
            primeiro_nome = nome.split()[0]
            novo_nick = f"{primeiro_nome} | {passaporte}"

            member = message.guild.get_member(message.author.id)
            if member is None:
                await message.channel.send("❌ Erro ao identificar o membro no servidor.", delete_after=10)
            else:
                try:
                    await member.edit(nick=novo_nick)
                except discord.Forbidden:
                    await message.channel.send("❌ Sem permissão para alterar o apelido.", delete_after=10)

            role = discord.utils.find(lambda r: r.name.lower() == cargo_normalizado.lower(), message.guild.roles)
            if role:
                try:
                    await message.author.add_roles(role)
                except discord.Forbidden:
                    await message.channel.send("❌ Sem permissão para atribuir cargo.", delete_after=10)
            else:
                await message.channel.send(f"❌ Cargo '{cargo_normalizado}' não existe no servidor.", delete_after=10)

            await message.add_reaction("✅")
        else:
            await message.channel.send("❌ Formato inválido ou dados em falta. Certifique-se de usar:\n```\nNome: ...\nPassaporte: ...\nCargo: ...\n```", delete_after=10)

        return


    # ------------------ Tratamento de comandos com erros -------------------
    comandos_alias = {
        "!iniciar": [
            "!iniciar", "!inicar", "!inicair", "!inicir", "!inciar", "!inciar", "!inicar", "!inicair", "!inciciar",
            "!inicar", "!inica", "!inicarrr", "!iniciaar", "!iniicar", "!iniciarrr", "!inicia", "!iniiar", "!iniar",
            "!iniçiar", "!inikar", "!inicjar", "!iniciar1", "!jniciar", "!8niciar", "!9niciar"
        ],
        "!produzir": [
            "!produzir", "!prodizur", "!pruduzir", "!prod", "!prodzir", "!produzirr", "!prduzir", "!prouzdir",
            "!produzir1", "!prodzir", "!produr", "!produsir", "!prdouzir", "!priduzir", "!prodzur", "!proddzir",
            "!porduzir", "!pdoduzir", "!produsri", "!prkduzir", "!prodyzir", "!produzi", "!produrzir", "!rpoduzir"
        ],
        "!laricas": [
            "!laricas", "!larica", "!larikas", "!larricas", "!laricass", "!larikass", "!larickas", "!laricas1", "!laricaz",
            "!larjcas", "!larivas", "!larkcas", "!lzrjcas", "!lar9cas", "!larocas", "!kzrjcas", "!laricazs", "!laricazx",
            "!laridcas", "!larcias", "!laricax", "!laricak", "!laricazs", "!lzricas"
        ],
    }

    if any(content == alias for alias in comandos_alias["!iniciar"]):
        await bot.get_command("iniciar").callback(await bot.get_context(message))
        return

    if any(content == alias for alias in comandos_alias["!produzir"]):
        await bot.get_command("produzir").callback(await bot.get_context(message))
        return
    
    if any(content == alias for alias in comandos_alias["!laricas"]):
        await bot.get_command("laricas").callback(await bot.get_context(message))
        return
    
    await bot.process_commands(message)

    # Verifica se a mensagem é um número inteiro válido
    if message.content.isdigit():
        qtd = int(message.content)
        await limpa_acao_msg(user_id)

        # Verifica se o número é positivo
        if qtd <= 0:
            await message.channel.send("❌ Apenas números inteiros positivos são permitidos.", delete_after=10)
        else:
            # Apaga as mensagens de erro anteriores
            if user_id in producoes_usuario:
                if 'erro_msg' in producoes_usuario[user_id]:
                    try:
                        await producoes_usuario[user_id]['erro_msg'].delete()
                    except discord.Forbidden:
                        pass
                    del producoes_usuario[user_id]['erro_msg']

            # Apaga a mensagem de quantidade anterior, se houver
            msg = producoes_usuario.get(user_id, {}).pop('quantidade_msg', None)
            if msg:
                try:
                    await msg.delete()
                except (discord.NotFound, discord.Forbidden):
                    pass

            # Salva a quantidade e envia confirmação
            producoes_usuario[user_id]['quantidade_temp'] = qtd

            # Apaga a mensagem de erro da quantidade anterior, se houver
            if 'quantidade_msg' in producoes_usuario[user_id]:
                try:
                    await producoes_usuario[user_id]['quantidade_msg'].delete()
                except discord.Forbidden:
                    pass

            confirm_msg = await message.channel.send(f"📥 Quantidade **{qtd}** guardada! Agora clique no botão do produto.")
            producoes_usuario[user_id]['quantidade_msg'] = confirm_msg

            try:
                await message.delete()
            except discord.Forbidden:
                pass

        return

    # Se o conteúdo não for um número inteiro ou números positivos
    if not message.content.isdigit() or float(message.content) <= 0 or any(c in message.content for c in ['.', ',', '-', 'T', 't']):
        if user_id in producoes_usuario:
            # Apaga as mensagens de erro anteriores, se houver
            if 'erro_msg' in producoes_usuario[user_id]:
                try:
                    await producoes_usuario[user_id]['erro_msg'].delete()
                except discord.Forbidden:
                    pass
                del producoes_usuario[user_id]['erro_msg']

            # Envia a mensagem de erro
            erro_msg = await message.channel.send("❌ Apenas números inteiros positivos são permitidos. Tente novamente!", delete_after=10)
            producoes_usuario[user_id]['erro_msg'] = erro_msg

            # Apaga a mensagem errada
            try:
                await message.delete()
            except discord.Forbidden:
                pass

    await bot.process_commands(message)

@app.route("/")
def home():
    return "Bot está vivo!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def manter_online():
    t = Thread(target=run)
    t.start()

bot.run(os.getenv('DISCORD_TOKEN'))
