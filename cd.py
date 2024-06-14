import pygame
import threading
import time
import random
import math

# Configurações do Jogo
NUM_FILOSOFOS = 5
LARGURA_TELA = 800
ALTURA_TELA = 600
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
RAIO_MESA = 200
RAIO_FILOSOFO = 50
FONT_SIZE = 32

# Inicializar Pygame
pygame.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption('Jantar dos Filósofos')
fonte = pygame.font.Font(None, FONT_SIZE)

# Inicialização dos garfos (semáforos)
garfos = [threading.Semaphore(1) for _ in range(NUM_FILOSOFOS)]
estados = ['pensando' for _ in range(NUM_FILOSOFOS)]
filosofos_posicoes = []

def filosofo(filosofo_id):
    while True:
        estados[filosofo_id] = 'pensando'
        time.sleep(random.uniform(1, 3))

        estados[filosofo_id] = 'com fome'
        while estados[filosofo_id] == 'com fome':
            time.sleep(0.1)

def pegar_garfos(filosofo_id):
    primeiro_garfo = filosofo_id
    segundo_garfo = (filosofo_id + 1) % NUM_FILOSOFOS

    if garfos[primeiro_garfo].acquire(blocking=False) and garfos[segundo_garfo].acquire(blocking=False):
        estados[filosofo_id] = 'comendo'
        time.sleep(random.uniform(1, 3))
        garfos[primeiro_garfo].release()
        garfos[segundo_garfo].release()
        estados[filosofo_id] = 'pensando'
    else:
        if garfos[primeiro_garfo].locked():
            garfos[primeiro_garfo].release()
        if garfos[segundo_garfo].locked():
            garfos[segundo_garfo].release()

def desenha_tela():
    tela.fill(BRANCO)
    centro_x = LARGURA_TELA // 2
    centro_y = ALTURA_TELA // 2

    pygame.draw.circle(tela, PRETO, (centro_x, centro_y), RAIO_MESA, 5)
    filosofos_posicoes.clear()

    for i in range(NUM_FILOSOFOS):
        angulo = 2 * math.pi * i / NUM_FILOSOFOS
        x = centro_x + int(RAIO_MESA * math.cos(angulo))
        y = centro_y + int(RAIO_MESA * math.sin(angulo))
        filosofos_posicoes.append((x, y))

        if estados[i] == 'pensando':
            cor = VERDE
        elif estados[i] == 'com fome':
            cor = VERMELHO
        elif estados[i] == 'comendo':
            cor = AZUL

        pygame.draw.circle(tela, cor, (x, y), RAIO_FILOSOFO)
        texto = fonte.render(f"F{i+1}", True, PRETO)
        tela.blit(texto, (x - 10, y - 10))

    pygame.display.update()

def mostrar_texto(texto, posicao):
    texto_surface = fonte.render(texto, True, PRETO)
    tela.blit(texto_surface, posicao)

def tela_inicial():
    tela.fill(BRANCO)
    mostrar_texto("Jantar dos Filósofos", (LARGURA_TELA // 2 - 150, ALTURA_TELA // 2 - 100))
    mostrar_texto("Clique para começar", (LARGURA_TELA // 2 - 130, ALTURA_TELA // 2))
    pygame.display.update()

def main():
    estado_jogo = 'inicial'

    clock = pygame.time.Clock()
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and estado_jogo == 'inicial':
                estado_jogo = 'jogando'
                filosofos_threads = [threading.Thread(target=filosofo, args=(i,)) for i in range(NUM_FILOSOFOS)]
                for t in filosofos_threads:
                    t.start()
            elif evento.type == pygame.MOUSEBUTTONDOWN and estado_jogo == 'jogando':
                pos = pygame.mouse.get_pos()
                for i, (x, y) in enumerate(filosofos_posicoes):
                    distancia = math.sqrt((x - pos[0]) * 2 + (y - pos[1]) * 2)
                    if distancia <= RAIO_FILOSOFO and estados[i] == 'com fome':
                        threading.Thread(target=pegar_garfos, args=(i,)).start()

        if estado_jogo == 'inicial':
            tela_inicial()
        elif estado_jogo == 'jogando':
            desenha_tela()
        clock.tick(30)

    pygame.quit()

if _name_ == '_main_':
    main()
