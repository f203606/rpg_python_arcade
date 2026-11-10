import random
import arcade

# B = parede
# . = chão
# E = inimigo
# P = posição inicial do Player

mapa_tiles = [
    'BBBBBBBBBBBBBBBBBBBB',
    'B..................B',
    'B.....E............B',
    'B............B.....B',
    'B..BBBBB.....B.....B',
    'B...B........B.....B',
    'B...B..............B',
    'B...B.......BBB....B',
    'B..................B',
    'B.....BBBB.........B',
    'B.......E..........B',
    'B.............P....B',
    'B..................B',
    'B.....E............B',
    'BBBBBBBBBBBBBBBBBBBB',
]

ICONE_JOGADOR = '@'

# Aula 13
TAMANHO_TILE = 32 #Define o tamanho do tile em pixels
ESCALA = 0.25 #Controla o tamanho das sprites
INTERVALO_MOVIMENTO_INIMIGO = 0.5 #Define o intervalo de movimento dos inimigos
DURACAO_FRAME_ANDANDO = 0.12 #Define o intervalo entre os frames de animação de caminhada do player
TEMPO_PARA_VOLTAR_AO_IDLE = 0.3 #Define o tempo necessário para resetar as animações do Player

CAMINHO_PAREDE = "imagens_arcade/parede_tile.png"
CAMINHO_CHAO = "imagens_arcade/chao.png"
CAMINHO_JOGADOR_IDLE = "imagens_arcade/player/idle1.png"
CAMINHO_JOGADOR_UP = "imagens_arcade/player/up1.png"
CAMINHOS_JOGADOR_ANDANDO = [f"imagens_arcade/player/direita{i}.png" for i in range(1, 4)]
CAMINHO_INIMIGO_PARADO = "imagens_arcade/inimigos/abobora/abobora1.png"
CAMINHO_INIMIGO_ANDANDO = "imagens_arcade/inimigos/abobora/abobora2.png"

# Aula 14 - Playtest 1: novos atributos
VIDA_BASE_JOGADOR = 40  # Vida máxima inicial do jogador
ATAQUE_BASE_JOGADOR = 6  # Ataque base do jogador
VIDA_BASE_INIMIGO = 30  # Vida máxima do inimigo (abóbora)  

class Mundo:
    def __init__(self):
        self.grade = [list(linha) for linha in mapa_tiles] #Preencha com o for de uma linha só
        self.jogador_x = 0
        self.jogador_y = 0
        self.inimigos = [] 

        for y, linha in enumerate(self.grade): #Preencha para obter posicao y e o valor da linha
            for x, celula in enumerate(linha):  #Preencha para obter posicao x e o valor da celula
                if celula == 'P':
                    self.jogador_x, self.jogador_y = x, y
                    self.grade[y][x] = '.' # Substitui o P por chão livre
                elif celula == 'E':
                    self.inimigos.append([x, y]) # Cada inimigo é representado por uma lista: 
                        # inimigo[0] → coordenada X (coluna). 
                        # inimigo[1] → coordenada Y (linha).
                    self.grade[y][x] = '.' # Substitui o E por chão livre   

    # Playtest 3
    def mover_jogador(self, dx, dy):
        #novo_x = self.jogador_x + dx
        #novo_y = self.jogador_y + dy
        #self.jogador_x, self.jogador_y = novo_x, novo_y

        # Playtest 9 - Movendo com colisões
        novo_x = self.jogador_x + dx
        novo_y = self.jogador_y + dy

        # Verifica se a nova posição está bloqueada.
        if self.esta_bloqueado(novo_x, novo_y):
            print("Você esbarra em uma parede.")
            return

        # Verifica se existe um inimigo na nova posição.
        inimigo = self.inimigo_em(novo_x, novo_y)
        if inimigo:
            print("Um inimigo bloqueia o caminho.")
            return

        # atualiza as coordenadas do Player.
        self.jogador_x, self.jogador_y = novo_x, novo_y

        # Aula 13 - Playtest 5
        return True

    # Playtest 7:
    def esta_bloqueado(self, x, y):
        if y < 0 or y >= len(self.grade):
            return True

        if x < 0 or x >= len(self.grade[0]):
            return True

        return self.grade[y][x] == "B"

    def inimigo_em(self, x, y):
        for inimigo in self.inimigos:
            if inimigo[0] == x and inimigo[1] == y:
                return inimigo
        return None

    def renderizar(self):

        # Percorre todas as linhas da matriz
        for y, linha in enumerate(self.grade):

            # Cria uma string vazia que receberá os caracteres daquela linha
            texto_linha = ""

            # Percorre todas as celulas da matriz
            for x, celula in enumerate(linha):

                # Verifica se a posição atual é a mesma posição do Player.
                if (x, y) == (self.jogador_x, self.jogador_y):
                    texto_linha += ICONE_JOGADOR # Renderizar o player
                elif self.inimigo_em(x, y):
                    texto_linha += "E" # Renderizar o inimigo
                else:
                    texto_linha += celula # Utilizar o conteúdo original da celula

            # Imprime a linha completa entre duas barras verticais.
            print("|" + texto_linha + "|")

        print("Movimento: W (cima) / S (baixo) / A (esquerda) / D (direita) / Q (sair)")

    # Playtest 8
    def vagar_inimigos(self):
        for inimigo in self.inimigos:   # Uma lista "de que" vai se mover?
            
            dx, dy = random.choice([
                (0, 0),   # Não se movimenta.
                (1, 0),   # Move uma posição para a direita.
                (-1, 0),  # Move uma posição para a esquerda.
                (0, 1),   # Move uma posição para baixo.
                (0, -1)  # Move uma posição para cima.
            ]) # DICA: Dê uma olhada na função executar

            nx, ny = inimigo[0] + dx, inimigo[1] + dy

            #O que bloquearia o movimento? Lembre-se que o inimigo não pode "atropelar" o Player.
            if not self.esta_bloqueado(nx, ny) and (nx, ny) != (self.jogador_x, self.jogador_y): 
                
                # Verifica se não existe outro inimigo na nova posição.
                if not self.inimigo_em(nx, ny):
                    inimigo[0], inimigo[1] = nx, ny

class JanelaJogo(arcade.Window):
    def __init__(self):
        super().__init__(640, 480, "RPG em Python")
        self.mundo = Mundo()
        self.sprites_cenario = arcade.SpriteList() # Aula 13 - Playtest 3 - Cenário
        self.sprites_jogador = arcade.SpriteList() # Aula 13 - Parte 4 - Personagens
        self.sprites_inimigos = arcade.SpriteList() # Aula 13 - Playtest 4 - Lista dos inimigos
        self.tempo_desde_ultimo_passo_inimigo = 0.0 # Aula 13 Playtest 6 - Movendo o inimigo 
        
        self.montar_cenario()
        self.montar_personagens() # Aula 13 - Parte 4 - Personagens

        # Aula 13 - Playtest 7 - Musica
        self.musica_fundo = arcade.Sound("songs/musica.mp3", streaming=True)    # Carrega a música em streaming
        self.player_musica = self.musica_fundo.play(volume=0.5, loop=True)      # Toca a música em loop com volume 0.5

        # Aula 14 - Playtest 1: novos atributos
        self.pos_inicial_jogador = (self.mundo.jogador_x, self.mundo.jogador_y)  # Guarda a posição inicial do jogador (para reset futuro)
        self.jogador_vida_max = VIDA_BASE_JOGADOR  # Vida máxima do jogador
        self.jogador_vida = self.jogador_vida_max  # Vida atual do jogador (começa cheia)
        self.jogador_ataque = ATAQUE_BASE_JOGADOR  # Valor de ataque do jogador

        self.em_batalha = False  # Flag que indica se o jogador está em batalha
        self.total_inimigos_derrotados = 0  # Contador de inimigos derrotados

        # Esses aqui serão úteis para a tela de batalha
        self.batalha_alvo_indice = None  # Índice do inimigo que está sendo enfrentado
        self.batalha_inimigo_vida = 0  # Vida atual do inimigo na batalha
        self.batalha_inimigo_vida_max = 0  # Vida máxima do inimigo na batalha
        self.batalha_inimigo_ataque = 0  # Valor de ataque do inimigo na batalha
        self.batalha_resultado = None  # Resultado da batalha ("vitoria", "derrota", "fuga" ou None)
        self.batalha_mensagem = ""  # Mensagem exibida na tela de batalha
        self.batalha_botoes = []  # Lista de botões da tela de batalha
        
    def on_draw(self):
        self.clear() # Limpa a tela
        self.sprites_cenario.draw() # Aula 13 - Playtest 3 - Cenário
        self.sprites_inimigos.draw() # Aula 13 - Playtest 4 - Inimigos
        self.sprites_jogador.draw() # Aula 13 - Parte 4 - Personagens

        # Aula 14 - Playtest 2 - HUD
        self.desenhar_hud()

        # Aula 14 - Playtest 5
        if self.em_batalha:
            self.desenhar_batalha()

    def para_tela_x(self, x):
        return x * TAMANHO_TILE + TAMANHO_TILE / 2

    def para_tela_y(self, y):
        num_linhas = len(self.mundo.grade)
        return (num_linhas - 1 - y) * TAMANHO_TILE + TAMANHO_TILE / 2

    def atualizar_posicao_sprite(self, sprite, grade_x, grade_y):
        sprite.center_x = self.para_tela_x(grade_x)
        sprite.center_y = self.para_tela_y(grade_y)

    def montar_cenario(self):
        for y, linha in enumerate(self.mundo.grade):
            for x, celula in enumerate(linha):
                caminho = CAMINHO_PAREDE if celula == 'B' else CAMINHO_CHAO
                sprite = arcade.Sprite(caminho, scale=ESCALA)
                self.atualizar_posicao_sprite(sprite, x, y)
                self.sprites_cenario.append(sprite)

    def montar_personagens(self): 
        self.sprite_jogador = arcade.Sprite(CAMINHO_JOGADOR_IDLE, scale=ESCALA) 
        self.atualizar_posicao_sprite(self.sprite_jogador, self.mundo.jogador_x, self.mundo.jogador_y) 
        self.sprites_jogador.append(self.sprite_jogador)

        # Aula 13 - Playtest 4
        for inimigo in self.mundo.inimigos:  # Percorre cada inimigo
            sprite = arcade.Sprite(CAMINHO_INIMIGO_PARADO, scale=ESCALA)  # Cria sprite do inimigo
            self.atualizar_posicao_sprite(sprite, inimigo[0], inimigo[1])  # Posiciona o inimigo
            self.sprites_inimigos.append(sprite)  # Adiciona à lista de inimigos 

    # Aula 14 - Playtest 3 - Refatoração 2
    def on_key_press(self, key, modifiers):
        if key == arcade.key.Q or key == arcade.key.ESCAPE:
            arcade.close_window()
            return
        
        if self.em_batalha:
            return
        
        if key in (arcade.key.W, arcade.key.UP):
            self.tentar_mover(0, -1, 'cima')
        elif key in (arcade.key.S, arcade.key.DOWN):
            self.tentar_mover(0, 1, 'baixo')
        elif key in (arcade.key.A, arcade.key.LEFT):
            self.tentar_mover(-1, 0, 'lateral')
        elif key in (arcade.key.D, arcade.key.RIGHT):
            self.tentar_mover(1, 0, 'lateral')

    # Aula 13 - Playtest 6 - Movimentando os inimigos
    def on_update(self, delta_time):
        self.tempo_desde_ultimo_passo_inimigo += delta_time
        if self.tempo_desde_ultimo_passo_inimigo >= INTERVALO_MOVIMENTO_INIMIGO:
            self.mundo.vagar_inimigos()

            for i, inimigo in enumerate(self.mundo.inimigos):
                sprite = self.sprites_inimigos[i]
                self.atualizar_posicao_sprite(sprite, inimigo[0], inimigo[1])
            self.tempo_desde_ultimo_passo_inimigo = 0

    def desenhar_hud(self):
        # Painel de fundo (pronto)
        arcade.draw_rect_filled(arcade.XYWH(100, 452, 190, 36), (20, 20, 30, 180))
        arcade.draw_rect_outline(arcade.XYWH(100, 452, 190, 36), arcade.color.WHITE, 1)
  
        # Barra de vida
        largura_barra = 160
        altura_barra = 14
        centro_x = 100
        y_barra = 452
        x_esquerda = centro_x - largura_barra / 2
        largura_atual = largura_barra * max(0.0, min(1.0, self.jogador_vida / self.jogador_vida_max))
 
        # Fundo da barra
        arcade.draw_rect_filled(
            arcade.XYWH(centro_x, y_barra, largura_barra, altura_barra), 
            arcade.color.DARK_RED
        )
 
        # Vida atual (complete aqui)
        arcade.draw_rect_filled(
            arcade.XYWH(x_esquerda + largura_atual / 2, y_barra, largura_atual, altura_barra),
            arcade.color.LIGHT_GREEN
        )
 
        # Contorno da barra (complete aqui)
        arcade.draw_rect_outline(
            arcade.XYWH(centro_x, y_barra, largura_barra, altura_barra),
            arcade.color.WHITE, 1
        )
        # Texto da vida. Observe com atenção, pois usaremos mais a frente novamente :)
        arcade.draw_text(
            f"{self.jogador_vida}/{self.jogador_vida_max}", 
            centro_x, y_barra, 
            arcade.color.WHITE, 10, 
            anchor_x="center", anchor_y="center"
        )

    # Aula 14 - Playtest 3 - Refatoração 1
    def tentar_mover(self, dx, dy, tipo):
        nx = self.mundo.jogador_x + dx
        ny = self.mundo.jogador_y + dy
 
        if not self.mundo.esta_bloqueado(nx, ny):
            inimigo = self.mundo.inimigo_em(nx, ny)
            if inimigo:
                indice = self.mundo.inimigos.index(inimigo)
                self.iniciar_batalha(indice)
                return
 
        moveu = self.mundo.mover_jogador(dx, dy)
        if moveu:
            if tipo == 'lateral':
                self.direcao_horizontal = 1 if dx > 0 else -1
            self.ultimo_tipo_movimento = tipo
            self.atualizar_posicao_sprite(
                self.sprite_jogador, 
                self.mundo.jogador_x,
                self.mundo.jogador_y
            )
            self.tempo_desde_ultimo_movimento_jogador = 0.0
            # self.atualizar_textura_jogador()
    
    # Aula 14 - Playtest 4
    def iniciar_batalha(self, indice_inimigo):
        self.em_batalha = True
        self.batalha_alvo_indice = indice_inimigo
        self.batalha_inimigo_vida_max = VIDA_BASE_INIMIGO
        self.batalha_inimigo_vida = self.batalha_inimigo_vida_max
        self.batalha_inimigo_ataque = random.randint(2, 10)
        self.batalha_resultado = None
        self.batalha_mensagem = "Uma abóbora selvagem apareceu!"
        self.montar_botoes_escolha()

    # Aula 14 - Playtest 4
    def montar_botoes_escolha(self):
        botoes = [
            {
                "x": 240, "y": 90, 
                "w": 130, "h": 50, 
                "texto": "Atacar", 
                # "acao": "Nada, por enquanto"
                "acao":self.atacar
            }
        ]

        # Adiciona o botão Fugir
        botoes.append({
            "x": 400, "y": 90,
            "w": 130, "h": 50,
            "texto": "Fugir",
            "acao": self.fugir
        })
        
        self.batalha_botoes = botoes

    # Aula 14 - Playtest 5
    def desenhar_batalha(self):
        
        # Painel e título (complete)
        arcade.draw_rect_filled(arcade.XYWH(320, 240, 560, 360), (20, 20, 30, 230))
        arcade.draw_text("Batalha!", 320, 400, arcade.color.WHITE, 22, anchor_x="center", bold=True)
        
        # Informações do jogador e do inimigo (prontas)
        arcade.draw_text(
            f"Jogador Vida: {self.jogador_vida}/{self.jogador_vida_max}",
            320, 360, arcade.color.LIGHT_GREEN, 14, anchor_x="center"
        )
        arcade.draw_text(
            f"Abóbora selvagem - Vida: {self.batalha_inimigo_vida}/{self.batalha_inimigo_vida_max}",
            320, 330, arcade.color.ORANGE, 14, anchor_x="center"
        )
        
        # Mensagem da batalha (pronta)
        if self.batalha_mensagem:
            arcade.draw_text(self.batalha_mensagem, 320, 240, arcade.color.WHITE, 14, width=520, align="center",anchor_x="center", multiline=True)
        
        # Botões (complete)
        for botao in self.batalha_botoes:
            retangulo = arcade.XYWH(botao["x"], botao["y"], botao["w"], botao["h"])
            arcade.draw_rect_filled(retangulo, arcade.color.DARK_SLATE_GRAY)
            arcade.draw_rect_outline(retangulo, arcade.color.WHITE, 2)
            arcade.draw_text(botao["texto"], botao["x"], botao["y"], arcade.color.WHITE, 16, anchor_x="center", anchor_y="center")

    # Aula 14 - Playtest 5
    def montar_botao_continuar(self):
        self.batalha_botoes = [
            {"x": 320, "y": 90, "w": 160, "h": 50, "texto": "Continuar",
             "acao": self.continuar_apos_batalha},
        ]

    # Aula 14 - Playtest 5
    def on_mouse_press(self, x, y, button, modifiers):
        if not self.em_batalha:
            return
        for botao in self.batalha_botoes:
            meio_w = botao["w"] / 2
            meio_h = botao["h"] / 2
            if botao["x"] - meio_w <= x <= botao["x"] + meio_w and \
               botao["y"] - meio_h <= y <= botao["y"] + meio_h:
                botao["acao"]()
                break

    # Aula 14 - Playtest 6 - dano e atacar
    def receber_dano(self, dano, mensagem):
        self.jogador_vida -= dano
        if self.jogador_vida <= 0:
            self.jogador_vida = 0
            mensagem += " Você foi derrotado..."
            self.batalha_resultado = "derrota"
            self.montar_botao_continuar()
        else:
            self.batalha_resultado = None
            self.montar_botoes_escolha()
        self.batalha_mensagem = mensagem

    def atacar(self):
        dano = max(1, random.randint(self.jogador_ataque - 2, self.jogador_ataque + 2))
        self.batalha_inimigo_vida -= dano
        mensagem = f"Você atacou e causou {dano} de dano!"
        if self.batalha_inimigo_vida <= 0:
            self.batalha_inimigo_vida = 0
            mensagem += " Você derrotou a abóbora!"
            self.batalha_resultado = "vitoria"
            self.batalha_mensagem = mensagem
            self.montar_botao_continuar()
        else:
            dano_recebido = max(1, random.randint(
                self.batalha_inimigo_ataque - 1, 
                self.batalha_inimigo_ataque + 1)
            )
            self.receber_dano(
                dano_recebido,
                mensagem + f" A abóbora revidou causando {dano_recebido} de dano!"
            )

    # Playtest 7: pós-batalha
    def continuar_apos_batalha(self):  # Continua o jogo após o fim da batalha
        if self.batalha_resultado == "vitoria":  # Se o jogador venceu
            self.total_inimigos_derrotados += 1  # Incrementa o contador de inimigos derrotados
            indice = self.batalha_alvo_indice  # Obtém o índice do inimigo derrotado
            if 0 <= indice < len(self.mundo.inimigos):  # Se o índice é válido
                del self.mundo.inimigos[indice]  # Remove o inimigo da lógica do mundo
                sprite = self.sprites_inimigos[indice]  # Obtém o sprite do inimigo
                sprite.remove_from_sprite_lists()  # Remove o sprite da tela

        elif self.batalha_resultado == "derrota":  # Se o jogador perdeu
            arcade.close_window()  # Fecha a janela do jogo
            return  # Encerra o método

        # Vitória e fuga: resetam as variáveis da batalha
        self.em_batalha = False  # Sai do modo de batalha
        self.batalha_resultado = None  # Reseta o resultado
        self.batalha_mensagem = ""  # Limpa a mensagem
        self.batalha_botoes = []  # Limpa os botões    

    # Playtest 8: fugir
    def fugir(self): # Ação de tentar fugir da batalha
        # 50% de chance de fugir
        if random.random() < 0.5: # Se o número aleatório for menor que 0.5 (50% de chance)
            self.batalha_mensagem = "Você fugiu com sucesso!" # Mensagem de fuga bem-sucedida
            self.batalha_resultado = "fuga" # Define o resultado como fuga
            self.montar_botao_continuar() # Mostra o botão "Continuar"
        else: # Se falhou na fuga
            # Falhou: a abóbora ataca com dano entre 1 e 5
            dano = random.randint(1, 5)  # Dano aleatório entre 1 e 5
            self.receber_dano(dano, f"Não conseguiu fugir! A abóbora causou {dano} de dano.")  # Aplica dano ao jogador 

janela = JanelaJogo()
arcade.run()

def executar():
    mundo = Mundo() # Crie aqui o objeto mundo
    rodando = True     

    while rodando:          # Colocando o projeto para rodar
        mundo.renderizar()  # Renderiza o projeto
        comando = input("\n> ").strip().lower()

        if comando == 'w':              # Comando para andar pra cima
            mundo.mover_jogador(0, -1)
        elif comando == 's':            # Andar para baixo. O que precisa mudar?
            mundo.mover_jogador(0, 1)   
        elif comando == 'a':            # E para a esquerda?
            mundo.mover_jogador(-1, 0)
        elif comando == 'd':            # E para a direita?
            mundo.mover_jogador(1, 0) 
        elif comando == 'q':            # Q para sair do jogo
            rodando = False
            continue
        else:
            print("Comando inválido.")
            continue

        # Faz com que os inimigos realizem seus movimentos.
        mundo.vagar_inimigos()

    print("Obrigado por jogar!")

# Chama a função executar() para iniciar o RPG.
# executar()