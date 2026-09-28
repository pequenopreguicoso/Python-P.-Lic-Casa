###EcoBot — Python 3.10 ou superior.

###COMO USAR

###Comandos: !ajuda, !materiais, !material papel, !reciclar, !quiz.
###O quiz tem cinco perguntas, explicações e pontuação individual por partida.
###As regras de coleta variam conforme o município e a cooperativa.


import asyncio
import random
import unicodedata

import discord
from discord.ext import commands


def normalizar(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto.lower().strip())
                   if unicodedata.category(c) != 'Mn')


MATERIAIS = {
    'papel': ('Papel e papelão',
              'São materiais feitos principalmente de fibras de celulose, geralmente obtidas da madeira. '
              'Exemplos: jornais, folhas e caixas. Separe secos e sem restos de comida. '
              'Papel higiênico usado e guardanapos engordurados não vão na coleta de papel. '
              'Na coleta por cores, a referência é azul.'),
    'plastico': ('Plástico',
                 'É um material formado por polímeros, que são longas cadeias de moléculas. '
                 'Exemplos: garrafas PET e potes. Retire o conteúdo e os resíduos antes de separar. '
                 'Existem vários tipos de plástico; nem todos são aceitos na coleta local. '
                 'Na coleta por cores, a referência é vermelho.'),
    'vidro': ('Vidro',
              'É um material produzido pela fusão de matérias-primas como areia, barrilha e calcário. '
              'Garrafas e potes podem ser reciclados conforme a coleta local. '
              'Espelhos, cerâmicas e lâmpadas não devem ser misturados às embalagens de vidro. '
              'Proteja e identifique vidro quebrado e confirme como entregá-lo. '
              'Na coleta por cores, a referência é verde.'),
    'metal': ('Metal',
              'É uma categoria de materiais que inclui alumínio, ferro e aço. '
              'Exemplos recicláveis: latas de bebidas e de alimentos, vazias e sem resíduos. '
              'Não perfure embalagens pressurizadas: consulte um ponto de recebimento. '
              'Na coleta por cores, a referência é amarelo.'),
    'organico': ('Resíduo orgânico',
                 'É um resíduo de origem biológica, como cascas de frutas, restos vegetais e folhas. '
                 'Cascas e restos vegetais podem virar adubo por compostagem. '
                 'Em composteiras domésticas simples, evite carnes, gorduras e laticínios. '
                 'Não misture orgânicos aos recicláveis secos. A referência de cor é marrom.'),
    'eletronico': ('Resíduo eletrônico',
                   'É um equipamento elétrico ou eletrônico descartado, como celular ou computador. '
                   'Ele reúne materiais como metais, plásticos e vidro e exige tratamento próprio. '
                   'Entregue em pontos de recebimento de eletrônicos; pilhas e baterias também '
                   'precisam de pontos específicos. Não coloque na coleta comum de recicláveis.'),
    'rejeito': ('Rejeito',
                'É aquilo para o qual se esgotaram as opções viáveis de recuperação ou tratamento. '
                'Na separação doméstica, exemplos comuns são papel higiênico usado e fraldas descartáveis. '
                'Embale e encaminhe conforme a coleta comum local. Reduzir o consumo ajuda a gerar menos rejeitos.'),
}

# Pergunta, alternativas, índice correto, explicação.
PERGUNTAS = [
    ('Qual é a principal fibra do papel?', ['Celulose', 'Alumínio', 'Areia'], 0,
     'O papel é feito principalmente de fibras de celulose.'),
    ('Onde separar uma garrafa PET vazia, se aceita pela coleta local?',
     ['Vidro', 'Plástico', 'Orgânico'], 1, 'PET é um tipo de plástico.'),
    ('O que fazer antes de separar uma lata de alimento?',
     ['Deixar a comida dentro', 'Misturar com fraldas', 'Retirar restos de alimento'], 2,
     'Resíduos de comida contaminam os materiais e dificultam a reciclagem.'),
    ('Qual item pode ir para uma composteira doméstica simples?',
     ['Pilha', 'Cascas de banana', 'Garrafa PET'], 1,
     'Cascas de frutas são resíduos orgânicos que podem virar adubo.'),
    ('Como descartar um celular velho?',
     ['Em ponto de recebimento de eletrônicos', 'Na lixeira de papel', 'Na rua'], 0,
     'Eletrônicos precisam de coleta e tratamento específicos.'),
    ('Qual item NÃO deve ser misturado às garrafas de vidro?',
     ['Pote de conserva vazio', 'Garrafa de suco vazia', 'Espelho'], 2,
     'Espelhos têm composição e revestimentos que exigem outro encaminhamento.'),
    ('Na coleta por cores, qual cor representa papel?',
     ['Verde', 'Azul', 'Amarelo'], 1, 'Azul representa papel; verde, vidro; amarelo, metal.'),
    ('Todo plástico é aceito em qualquer coleta seletiva?',
     ['Sim', 'Só quando é vermelho', 'Não; depende do tipo e da coleta local'], 2,
     'Consulte o município ou a cooperativa sobre os materiais aceitos.'),
    ('O que fazer com papel higiênico usado?',
     ['Separar como rejeito na coleta comum', 'Misturar com papel limpo', 'Colocar com metais'], 0,
     'Papel higiênico usado não deve entrar na coleta de papel reciclável.'),
    ('Qual atitude ajuda a diminuir a geração de resíduos?',
     ['Comprar mais descartáveis', 'Reduzir o consumo e reutilizar objetos', 'Misturar todo o lixo'], 1,
     'Reduzir e reutilizar evitam resíduos antes mesmo da reciclagem.'),
]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None,
                   case_insensitive=True, allowed_mentions=discord.AllowedMentions.none())
partidas = set()


@bot.event
async def on_ready():
    print(('ReciclaBot ligado como ' + str(bot.user) + '! Use !ajuda no Discord.'))


@bot.command(name='ajuda')
async def ajuda(ctx):
    await ctx.send('**ReciclaBot**\n'
                   '`!materiais` — mostra os materiais disponíveis.\n'
                   '`!material papel` — explica um material e seu descarte.\n'
                   '`!reciclar` — ensina a separar os resíduos.\n'
                   '`!quiz` — começa 5 perguntas com pontuação e explicações.\n'
                   'No quiz, responda A, B ou C; escreva `sair` para encerrar.')


@bot.command(name='materiais')
async def materiais(ctx):
    await ctx.send('**Materiais:** ' + ', '.join(MATERIAIS)
                   + '\nExemplo: `!material plástico`')


@bot.command(name='material')
async def material(ctx, *, nome=''):
    chave = normalizar(nome)
    chave = {'papelao': 'papel', 'organicos': 'organico', 'eletronicos': 'eletronico',
             'metais': 'metal', 'aluminio': 'metal', 'pet': 'plastico'}.get(chave, chave)
    if chave not in MATERIAIS:
        await ctx.send('Escolha: ' + ', '.join(MATERIAIS) + '. Exemplo: `!material vidro`')
        return
    titulo, texto = MATERIAIS[chave]
    await ctx.send(('**' + str(titulo) + '**\n' + str(texto)))


@bot.command(name='reciclar')
async def reciclar(ctx):
    await ctx.send('**Como separar os resíduos**\n'
                   '1. Reduza o consumo e reutilize o que puder.\n'
                   '2. Separe recicláveis secos de orgânicos e rejeitos.\n'
                   '3. Esvazie embalagens e retire restos, evitando desperdício de água.\n'
                   '4. Mantenha papel e papelão secos.\n'
                   '5. Leve pilhas, baterias e eletrônicos a pontos de recebimento próprios.\n'
                   '6. Confira os materiais aceitos e os dias da coleta no seu município.\n'
                   'Use `!material nome` para aprender mais!')


@bot.command(name='quiz')
async def quiz(ctx):
    chave = (ctx.channel.id, ctx.author.id)
    if chave in partidas:
        await ctx.send('Você já tem um quiz neste canal. Responda ou escreva `sair`.')
        return
    partidas.add(chave)
    pontos = 0
    try:
        await ctx.send(('**Quiz de ' + str(ctx.author.display_name) + '**: 5 perguntas. Responda A, B ou C em até 60 segundos por pergunta. Para parar: `sair`.'))
        for numero, (pergunta, opcoes, correta, explicacao) in enumerate(random.sample(PERGUNTAS, 5), 1):
            def check(m):
                return (m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
                        and m.content.strip().lower() in ('a', 'b', 'c', 'sair'))

            # Registra a espera antes de enviar para não perder respostas rápidas.
            espera = asyncio.create_task(bot.wait_for('message', check=check, timeout=60))
            await asyncio.sleep(0)
            try:
                alternativas = '\n'.join((str(letra) + ') ' + str(opcao)) for letra, opcao in zip('ABC', opcoes))
                await ctx.send(('**' + str(ctx.author.display_name) + ' — ' + str(numero) + '/5: ' + str(pergunta) + '**\n' + str(alternativas)))
                resposta = await espera
            except asyncio.TimeoutError:
                await ctx.send(('Tempo esgotado! Quiz encerrado com ' + str(pontos) + ' ponto(s).'))
                return
            finally:
                if not espera.done():
                    espera.cancel()
                    try:
                        await espera
                    except asyncio.CancelledError:
                        pass
            letra = resposta.content.strip().lower()
            if letra == 'sair':
                await ctx.send(('Quiz encerrado. Você fez ' + str(pontos) + ' ponto(s).'))
                return
            acertou = letra == 'abc'[correta]
            pontos += int(acertou)
            resultado = 'Acertou!' if acertou else ('A resposta é ' + str('ABC'[correta]) + '.')
            await ctx.send((str(resultado) + ' ' + str(explicacao)))
        await ctx.send(('**' + str(ctx.author.display_name) + ': ' + str(pontos) + '/5 pontos!** Continue aprendendo com `!materiais` ou jogue novamente com `!quiz`.'))
    finally:
        partidas.discard(chave)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Comando desconhecido. Use `!ajuda`.')
    else:
        print(('Erro no comando: ' + str(type(error).__name__)))
        await ctx.send('Não consegui concluir o comando. Verifique minhas permissões e tente novamente.')


if __name__ == '__main__':
    # Cole o token do seu bot entre as aspas abaixo.
    token = "COLOQUE_SEU_TOKEN_AQUI"
    if not token.strip() or token == "COLOQUE_SEU_TOKEN_AQUI":
        raise SystemExit("Preencha o token no final do código antes de executar.")
    try:
        bot.run(token.strip())
    except discord.LoginFailure:
        print('Token inválido. Confira o token na seção Bot do portal do Discord.')
    except discord.PrivilegedIntentsRequired:
        print('Ative Message Content Intent na seção Bot do portal do Discord.')
