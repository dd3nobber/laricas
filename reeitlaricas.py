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

load_dotenv()

app = Flask("")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)

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

producoes_usuario = {}

mensagens_stock = {}

# Pasta onde este ficheiro .py está guardado
BASE_DIR = Path(__file__).resolve().parent

# JSON ficará na MESMA pasta do .py
ARQ_STOCK = BASE_DIR / "dados_estoque.json"

def carregar_estoque() -> dict[int, dict]:
    try:
        with open(ARQ_STOCK, "r", encoding="utf-8") as f:
            bruto = json.load(f)
        return {int(uid): data for uid, data in bruto.items()}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

producoes_stock: dict[int, dict] = carregar_estoque()
producao_temp: dict[int, dict] = {}  # Armazena o que o usuário está produzindo no momento

def criar_view_atualizar_stock(user_id: int, producao: dict, produtos_produzidos: dict) -> View:
    view = View(timeout=None)
    botao = Button(label="🔄 Atualizar Stock", style=discord.ButtonStyle.primary)

    async def callback(interaction: discord.Interaction):
        if interaction.user.id != user_id:
            await interaction.response.send_message("Este botão não é para você.", ephemeral=True)
            return

        # Remover ingredientes usados
        producoes_stock.setdefault(user_id, {})
        estoque = producoes_stock[user_id]

        # Remove os ingredientes usados
        for produto, qtd in produtos_produzidos.items():
            divisor = 2 if produto in ['🍔 X-Tudo', '🥗 X-Salada', '🥪 X-Burguer', '🥩 Hambúrguer', '🌾 Farinha de Trigo'] else 1
            porcoes = qtd // divisor if produto in ['🍔 X-Tudo', '🥗 X-Salada', '🥪 X-Burguer', '🥩 Hambúrguer', '🌾 Farinha de Trigo'] else qtd

            for ingrediente, qtd_receita in produtos[produto]['ingredientes'].items():
                qtd_ingrediente_total = qtd_receita * porcoes
                estoque[ingrediente] = estoque.get(ingrediente, 0) - qtd_ingrediente_total
                if estoque[ingrediente] < 0:
                    estoque[ingrediente] = 0  # evitar negativo

        # Adicionar produtos produzidos ao estoque
        for produto, qtd in produtos_produzidos.items():
            estoque[produto] = estoque.get(produto, 0) + qtd

        salvar_estoque(producoes_stock)

        await interaction.response.send_message("✅ Estoque atualizado com sucesso!", ephemeral=True)
        # Opcional: remover o botão depois do clique
        for item in view.children:
            item.disabled = True
        await interaction.message.edit(view=view)

    botao.callback = callback
    view.add_item(botao)
    return view

def pode_produzir(produto, quantidade, estoque):
    ingredientes_necessarios = produtos[produto]['ingredientes']

    produtos_especiais = ['🍔 X-Tudo', '🥗 X-Salada', '🥪 X-Burguer','🥩 Hambúrguer','🌾 Farinha de Trigo']

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

        producoes_stock.setdefault(user_id, {})
        estoque_final = producoes_stock[user_id]  # Defina aqui

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

            producoes_stock.setdefault(user_id, {})
            estoque_final_cb = producoes_stock[user_id]

            produtos_produzidos_cb = {
                k: v for k, v in producoes_usuario.get(user_id, {}).items()
                if k not in ['quantidade_temp', 'quantidade_msg', 'producoes_msg']
            }

            produtos_especiais_cb = ['🍔 X-Tudo', '🥗 X-Salada', '🥪 X-Burguer', '🥩 Hambúrguer', '🌾 Farinha de Trigo']

            # Verifica e atualiza ingredientes e produtos no estoque
            for produto_, qtd_ in produtos_produzidos_cb.items():
                divisor = 2 if produto_ in produtos_especiais_cb else 1
                porcoes = qtd_ // divisor if divisor else qtd_

                for ing, qtd_receita in produtos[produto_]['ingredientes'].items():
                    total_ingrediente = qtd_receita * porcoes

                    estoque_atual = estoque_final_cb.get(ing, 0)
                    if estoque_atual < total_ingrediente:
                        await interaction.response.send_message(
                            f"❌ Ingrediente insuficiente: {ing} (Necessário: {total_ingrediente}, Disponível: {estoque_atual})",
                            ephemeral=True
                        )
                        return

                    estoque_final_cb[ing] = estoque_atual - total_ingrediente
                    if estoque_final_cb[ing] < 0:
                        estoque_final_cb[ing] = 0

            for produto_, qtd_ in produtos_produzidos_cb.items():
                estoque_final_cb[produto_] = estoque_final_cb.get(produto_, 0) + qtd_

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

def criar_view_ingredientes(user_id):
    view = View(timeout=None)

    # Botões para produzir comida ou bebida
    botao_comida = Button(label="🍽️ Produzir Comida", style=discord.ButtonStyle.primary)
    botao_bebida = Button(label="🥤 Produzir Bebida", style=discord.ButtonStyle.primary)

    # Botão para cancelar a operação (vermelho)
    botao_cancelar = Button(label="❌ Cancelar", style=discord.ButtonStyle.danger)
    # Botão para produzir (verde)
    botao_produzir = Button(label="✅ Produzir", style=discord.ButtonStyle.success)

    async def callback_comida(interaction):
        if interaction.user.id != user_id:
            await interaction.channel.send("Esse botão não é para você.", ephemeral=True)
            return

        await interaction.response.defer()

        producoes_usuario[user_id]['categoria_selecionada'] = 'comida'  # Armazena a categoria

        # Exibir os botões de ingredientes para comida
        view_comida = View(timeout=None)
        for ingrediente in ingredientes['comida']:  # Usando o dicionário de ingredientes para comida

            botao_ingrediente = Button(label=ingrediente, style=discord.ButtonStyle.primary)

            async def ingrediente_callback(interaction, ingrediente=ingrediente):
                if interaction.user.id != user_id:
                    await interaction.channel.send("Esse botão não é para você.", ephemeral=True)
                    return

                await interaction.response.defer()

                # Pega a quantidade digitada no chat
                qtd = producoes_usuario[user_id].get('quantidade_temp')

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
        if interaction.user.id != user_id:
            await interaction.channel.send("Esse botão não é para você.", ephemeral=True)
            return

        await interaction.response.defer()

        producoes_usuario[user_id]['categoria_selecionada'] = 'bebida'  # Armazena a categoria

        # Exibir os botões de ingredientes para bebida
        view_bebida = View(timeout=None)
        for ingrediente in ingredientes['bebida']:  # Usando o dicionário de ingredientes para bebida

            botao_ingrediente = Button(label=ingrediente, style=discord.ButtonStyle.primary)

            async def ingrediente_callback(interaction, ingrediente=ingrediente):
                if interaction.user.id != user_id:
                    await interaction.channel.send("Esse botão não é para você.", ephemeral=True)
                    return

                await interaction.response.defer()

                # Pega a quantidade digitada no chat
                qtd = producoes_usuario[user_id].get('quantidade_temp')

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
        if interaction.user.id != user_id:
            await interaction.channel.send("Esse botão não é para você.", ephemeral=True)
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
        if interaction.user.id != user_id:
            await interaction.channel.send("Esse botão não é para você.", ephemeral=True)
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
                if interaction.user.id != user_id:
                    await interaction.channel.send("Esse botão não é para você.", ephemeral=True)
                    return

                await interaction.response.defer()

                quantidade = estoque.get('quantidade_temp')
                if quantidade is None:
                    await interaction.channel.send("❌ Digite a quantidade no chat antes de escolher o produto.", ephemeral=True)
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
            if interaction.user.id != user_id:
                await interaction.channel.send("Esse botão não é para você.", ephemeral=True)
                return

            await interaction.response.defer()

            # Apagar todas as mensagens anteriores do canal, exceto a mensagem fixada
            async for msg in interaction.channel.history(limit=100):
                if not msg.pinned and msg.author.bot:
                    try:
                        await msg.delete()
                    except discord.Forbidden:
                        pass

            producoes_stock.setdefault(user_id, {})
            estoque_final = producoes_stock[user_id]


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
                if interacao.user.id != user_id:
                    await interacao.response.send_message("Este botão não é para você.", ephemeral=True)
                    return

                producoes_stock.setdefault(user_id, {})
                estoque_final = producoes_stock[user_id]

                produtos_especiais = ['🍔 X-Tudo', '🥗 X-Salada', '🥪 X-Burguer', '🥩 Hambúrguer', '🌾 Farinha de Trigo']
                for produto_, qtd_ in produtos_produzidos.items():
                    divisor = 2 if produto_ in produtos_especiais else 1
                    porcoes = qtd_ // divisor if divisor else qtd_

                    for ing, qtd_receita in produtos[produto_]['ingredientes'].items():
                        total = qtd_receita * porcoes
                        estoque_final[ing] = estoque_final.get(ing, 0) - total
                        if estoque_final[ing] < 0:
                            estoque_final[ing] = 0

                for produto_, qtd_ in produtos_produzidos.items():
                    estoque_final[produto_] = estoque_final.get(produto_, 0) + qtd_

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
            if interaction.user.id != user_id:
                await interaction.channel.send("Esse botão não é para você.", ephemeral=True)
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
        view_ingredientes = criar_view_ingredientes(user_id)
        await interaction.message.edit(content="Escolha o ingrediente que você deseja produzir.", view=view_ingredientes)

    async def callback_stock(interaction):
        if interaction.user.id != user_id:
            await interaction.channel.send("Esse botão não é para você.", ephemeral=True)
            return

        await interaction.response.defer()
        await interaction.message.delete()

        # Enviar a mensagem com os botões de produtos
        view_stock = criar_view_stock(user_id)
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

def criar_view_stock(user_id: int) -> View:
    view = View(timeout=None)


    # ---------- helpers ----------
    produtos_ingredientes = ['🥩 Hambúrguer', '🍞 Pão de Hambúrguer', '🌾 Farinha de Trigo']

    def adicionar(user_id: int, item: str, qtd: int):
        producoes_stock.setdefault(user_id, {})
        atual = producoes_stock[user_id].get(item, 0)
        producoes_stock[user_id][item] = atual + qtd

        # Se for produto-ingrediente, sincroniza ambos
        if item in produtos_ingredientes:
            # Garante que o mesmo valor esteja sincronizado (soma igual)
            # Na prática, mantém o valor mais alto (pode ser atualizado para o mesmo)
            producoes_stock[user_id][item] = atual + qtd

        salvar_estoque(producoes_stock)
        return f"✅ Adicionado {qtd}x **{item}** ao estoque."

    def remover(user_id: int, item: str, qtd: int):
        if user_id not in producoes_stock or item not in producoes_stock[user_id]:
            return
        atual = producoes_stock[user_id][item]
        novo = max(0, atual - qtd)
        producoes_stock[user_id][item] = novo

        # Se for produto-ingrediente, sincroniza ambos
        if item in produtos_ingredientes:
            producoes_stock[user_id][item] = novo

        salvar_estoque(producoes_stock)
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

    # ---------- MENU PRINCIPAL ----------
    async def volta_menu(inter):
        await limpa_quantidade_msg(user_id)
        await limpa_acao_msg(user_id)
        await apagar_stock_antigo()
        await inter.message.delete()
        await inter.channel.send(
            "Escolha uma opção:", view=criar_view_stock(user_id)
        )

    # ---------- SUB‑MENUS ----------
    async def abre_submenu(inter, colecao, titulo):
        await limpa_quantidade_msg(user_id)
        await limpa_acao_msg(user_id)
        await apagar_stock_antigo()
        await inter.message.delete()

        nova = View(timeout=None)
        for item in colecao:
            rotulo = item.replace('_', ' ').title()
            bot = Button(label=rotulo, style=discord.ButtonStyle.primary)

            async def item_cb(i, produto=item, nome=rotulo):
                await limpa_quantidade_msg(user_id)
                await limpa_acao_msg(user_id)
                qtd = producoes_usuario.get(user_id, {}).get("quantidade_temp")
                if not isinstance(qtd, int) or qtd <= 0:
                    await pede_quantidade(i, nome)
                    return

                # view Adicionar / Remover
                acao = View(timeout=None)
                bt_add = Button(label="✅ Adicionar", style=discord.ButtonStyle.success)
                bt_rem = Button(label="❌ Remover",  style=discord.ButtonStyle.danger)

                async def add_cb(inter, prod=produto):
                    await limpa_quantidade_msg(user_id)
                    await limpa_acao_msg(user_id)
                    if inter.user.id != user_id:
                        await inter.response.send_message(
                            "Esse botão não é para você.", ephemeral=True
                        )
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
                    await limpa_quantidade_msg(user_id)
                    await limpa_acao_msg(user_id)
                    if inter.user.id != user_id:
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

    async def stock_main_cb(inter):
        await limpa_quantidade_msg(user_id)
        await limpa_acao_msg(user_id)
        if inter.user.id != user_id:
            await inter.response.send_message("Esse botão não é para você.", ephemeral=True)
            return

        # Carrega os dados do estoque do JSON
        estoque_atual = carregar_estoque()

        # Atualiza apenas os dados do usuário atual

        await apagar_stock_antigo()

        col_nome = 28
        col_q    = 4
        col_kg   = 7

        stock = producoes_stock.get(user_id, {})
        ingr_linhas, prod_linhas = [], []

        for ing in ingredientes["comida"] + ingredientes["bebida"]:
            q  = stock.get(ing, 0)
            kg = peso_item(ing) * q         
            ingr_linhas.append(
                f"{ing:<{col_nome}} | {q:<{col_q}} | {kg:>{col_kg}.2f}kg"
            )

        for produto_nome in produtos:  # Itera sobre todos os produtos possíveis
            q = stock.get(produto_nome, 0)  # Pega quantidade no estoque ou zero se não existir
            kg = peso_item(produto_nome) * q
            prod_linhas.append(
                f"{produto_nome:<{col_nome}} | {q:<{col_q}} | {kg:>{col_kg}.2f}kg"
            )

        tam = max(len(ingr_linhas), len(prod_linhas))
        ingr_linhas += [" " * (col_nome + col_q + col_kg + 6)] * (tam - len(ingr_linhas))
        prod_linhas += [""] * (tam - len(prod_linhas))

        header  = "📦 **Stock Atual**\n"
        titles  = f"{'Ingredientes':<{col_nome}} | {'Q.':<{col_q}} | {'Kg':>{col_kg}} │ "
        titles += f"{'Produtos':<{col_nome}} | {'Q.':<{col_q}} | {'Kg':>{col_kg}}"
        sep = "─" * len(titles)

        linhas = []
        for esq, dir_ in zip(ingr_linhas, prod_linhas):
            linhas.append(f"{esq} │ {dir_}")

        bloco = "```diff\n"
        limite = 1900
        primeiro = True
        atual = bloco
        mensagens = []
        for ln in [titles, sep] + linhas:
            if len(atual) + len(ln) + 1 > limite:
                atual += "```"
                msg = await inter.channel.send((header if primeiro else "") + atual)
                mensagens.append(msg)
                primeiro = False
                atual = bloco
            atual += ln + "\n"
        if atual != bloco:
            atual += "```"
            msg = await inter.channel.send((header if primeiro else "") + atual)
            mensagens.append(msg)

        mensagens_stock[user_id] = mensagens

    bt_stock_main.callback = stock_main_cb

    for b in (bt_prod, bt_beb, bt_com, bt_stock_main):
        view.add_item(b)

    return view

async def limpa_acao_msg(uid: int):
    """Apaga (se existir) a mensagem '✅ …' ou '❌ …'."""
    ref = producoes_stock.get(uid, {}).pop("acao_msg", None)
    if ref:
        try:
            await ref.delete()
        except (discord.Forbidden, discord.NotFound):
            pass   

def salvar_estoque(dados: dict[int, dict]):
    filtrado: dict[str, dict] = {}

    for uid_int, user_data in dados.items():
        # filtra só campos simples
        limpo = {
            k: v for k, v in user_data.items()
            if k != "quantidade_temp" and not k.endswith("_msg")
               and isinstance(v, (numbers.Number, str, list, dict))
        }
        # sempre grava usando a **mesma** chave‑string
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

    if 'produção' not in ctx.channel.name:
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send("❌ Este comando não está disponível nesta sala.", ephemeral=True)
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

    # Limpa outras mensagens de bot, exceto fixadas
    async for msg in ctx.channel.history(limit=100):
        if not msg.pinned and msg.author.bot:
            try:
                await msg.delete()
            except:
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
    channel_name = f'Produção - {member.name.lower()}'
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if existing_channel:
        await existing_channel.send(f"🔄 {member.mention}, você já possui um canal de produção.")
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

    # ------------------ Tratamento de comandos com erros -------------------
    comandos_alias = {
        "!iniciar": ["!iniciar", "!inicar", "!inicair", "!inicir", "!inciar"],
        "!produzir": ["!produzir", "!prodizur", "!pruduzir", "!prod", "!prodzir"],
    }

    if any(content == alias for alias in comandos_alias["!iniciar"]):
        await bot.get_command("iniciar").callback(await bot.get_context(message))
        return

    if any(content == alias for alias in comandos_alias["!produzir"]):
        await bot.get_command("produzir").callback(await bot.get_context(message))
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