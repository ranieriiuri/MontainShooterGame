import sys
from datetime import datetime

import pygame
from pygame import Surface, Rect, KEYDOWN, K_RETURN, K_BACKSPACE, K_ESCAPE
from pygame.font import Font

from code.Const import C_YELLOW, SCORE_POS, MENU_OPTION, C_WHITE
from code.DBProxy import DBProxy


class Score:
    def __init__(self, window: Surface):
        self.window = window
        self.surf = pygame.image.load('./asset/ScoreBg.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)
        pass

    def save(self, game_mode: str, player_score: list[int]):
        pygame.mixer_music.load('./asset/Score.mp3')
        pygame.mixer_music.play(-1)
        # cria o db chamando a class do proxy
        db_proxy = DBProxy('DBScore')
        name = ''
        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            #ao finalizar o jogo seta o nome do vencedor
            self.score_text(48, 'YOU WIN!!', C_YELLOW, SCORE_POS['Title'])
            # pede o nome da pessoa q ganhou com o P1
            text = 'Enter Player 1 name (4 characters):'
            score = player_score[0] #seta o essa var com o param score recebido pelo metodo

            #se for modo normal (1 player)
            if game_mode == MENU_OPTION[0]:
                score = player_score[0]
            #se cooperative
            if game_mode == MENU_OPTION[1]:
                score = (player_score[0] + player_score[1]) / 2
                text = 'Enter Team name (4 characters):'
            #se competitive...
            if game_mode == MENU_OPTION[2]:
                #se P1 score maior q P2, salva o do P1
                if player_score[0] >= player_score[1]:
                    score = player_score[0]
                #senao, salva o do P2
                else:
                    score = player_score[1]
                    text = 'Enter Player 2 name (4 characters):'
            #printa a descricao do score
            self.score_text(20, text, C_WHITE, SCORE_POS['EnterName'])

            for event in pygame.event.get():
                # p conseguir fechar a janela no icone de fechar
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #se o evento for qlqr tecla pressionada...
                elif event.type == KEYDOWN:
                    #se for enter e o tam. do nome for de 4 carac, chama o proxy e salva e mostra
                    if event.key == K_RETURN and len(name) == 4:
                        db_proxy.save({'name': name, 'score': score, 'date': get_formatted_date()})
                        self.show() #func criada abaixo, para mostrar a tela de score geral
                        return #esse return possibilita voltar à tela de menu principal com um ESC após salvar e mostrar score. Pq na função show tem um return q volta pra tela de salvamento e esse daqui, tendo cumprido todo seu percurso, quando identificado, volta pro menu principal!

                    #se o backspace for pressionado, decrementa o nome escrito até então
                    elif event.key == K_BACKSPACE:
                        name = name[:-1]
                    #se nem enter nem bckspace...
                    else:
                        #enquanto o nome ainda for menor q 4
                        if len(name) < 4:
                            #vai incrementando os carac à var 'name'
                            name += event.unicode
            #printa o text de score da name construída, inclusive sua score position correta
            self.score_text(20, name, C_WHITE, SCORE_POS['Name'])

            #OBS SOBRE ALINHA ABAIXO: O pygame trabalha com um buffer duplo! Os elementos (sprites, textos, fundos e etc) ficam em um buffer oculto, enquanto o buffer visível é o ultimo alterado por essa linha. Então quando criamos essa l inha 'pygame.display.flip()', o Pygame atualiza a tela com tudo que foi desenhado desde o último frame.
            pygame.display.flip()
            pass

    def show(self):
        #setamos o fundo, a musica e construímos a descricao da tela de score
        pygame.mixer_music.load('./asset/Score.mp3')
        pygame.mixer_music.play(-1)
        self.window.blit(source=self.surf, dest=self.rect)
        self.score_text(48, 'TOP 10 SCORE', C_YELLOW, SCORE_POS['Title'])
        self.score_text(20, 'NAME     SCORE           DATE      ', C_YELLOW, SCORE_POS['Label'])
        #acessa o db e busca os 10 ultimos (recentes) pelo metodo criado no proxy e após, fecha-o
        db_proxy = DBProxy('DBScore')
        list_score = db_proxy.retrieve_top10()
        db_proxy.close()

        #laço que apresenta os dados-score dos players trazidos pelo metodo do proxy
        for player_score in list_score:
            # usando desestruturação p pegar cada dado dos players em 'list_score' já em uma var diferente, p formatar abaixo como queremos q cada uma apareça qnd chamados no método 'score_text'
            id_, name, score, date = player_score
            self.score_text(20, f'{name}     {int(score):05d}     {date}', C_YELLOW,
                            SCORE_POS[list_score.index(player_score)])
        #se fechar a janela no x, fecha, se enter
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #se houver uma tecla pressionada e for o ESC, retorna
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
            pygame.display.flip() #atualiza o buffer

    #metodo q formata o texto do score
    def score_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)

#func q pega a data atual para usar na 'save' acima
def get_formatted_date():
    current_datetime = datetime.now()
    current_time = current_datetime.strftime("%H:%M")
    current_date = current_datetime.strftime("%d/%m/%y")
    return f"{current_time} - {current_date}"
