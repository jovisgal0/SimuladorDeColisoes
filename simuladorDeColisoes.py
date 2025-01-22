#    Autor: João Vitor Caldeira da Silva
#    Email: joao.170506@alunos.utfpr.edu.br
#    Engenharia da Computação - UTFPR 
import pygame
import random
import numpy as np
import pygame.gfxdraw

class Ambiente():
    def __init__(self, DIMENSOES, intervalo_tempo):
        self.DIMENSOES = DIMENSOES
        self.intervalo_tempo = intervalo_tempo
        self.particulas = []

    def atualizar(self):
        for p1 in self.particulas:
            p1.atualizarEstado()
            self.quicar(p1)
            for p2 in self.particulas:
                if p1 != p2:
                    self.colisaoElastica(p1, p2)

    def adicionarParticula(self, particula):
        self.particulas.append(particula)

    def quicar(self, particula):
        for i in range(len(particula.posicao[0])):
            if particula.posicao[0][i] > self.DIMENSOES[i] - particula.raio:
                distancia = particula.raio - (self.DIMENSOES[i] - particula.posicao[0][i])
                particula.adicionarPosicao([-distancia if i == 0 else 0, -distancia if i == 1 else 0])
                particula.velocidade[0][i] *= -1  # Inverte o eixo correspondente
            elif particula.posicao[0][i] < particula.raio:
                distancia = particula.raio - particula.posicao[0][i]
                particula.adicionarPosicao([distancia if i == 0 else 0, distancia if i == 1 else 0])
                particula.velocidade[0][i] *= -1  # Inverte o eixo correspondente

    def colisaoElastica(self, p1, p2):
        delta_posicao = p1.posicao - p2.posicao
        distancia = np.sqrt(np.sum(delta_posicao**2))
        if distancia < p1.raio + p2.raio:
            if distancia == 0:
                return
            deslocamento = distancia - (p1.raio + p2.raio)
            p1.adicionarPosicao((-delta_posicao / distancia) * deslocamento / 2)
            p2.adicionarPosicao((delta_posicao / distancia) * deslocamento / 2)
            massa_total = p1.massa + p2.massa
            delta_v1 = -2 * p2.massa / massa_total * np.inner(p1.velocidade - p2.velocidade, delta_posicao) / np.sum(delta_posicao**2) * delta_posicao
            delta_v2 = -2 * p1.massa / massa_total * np.inner(p2.velocidade - p1.velocidade, -delta_posicao) / np.sum(delta_posicao**2) * -delta_posicao
            p1.adicionarVelocidade(delta_v1)
            p2.adicionarVelocidade(delta_v2)

# Classe da partícula
class Particula():
    def __init__(self, ambiente, posicao, velocidade, raio, massa):
        self.ambiente = ambiente
        self.posicao = posicao
        self.velocidade = velocidade
        self.raio = raio
        self.massa = massa
        self.cor = tuple(random.randint(0, 255) for _ in range(3))  

    def adicionarVelocidade(self, velocidade):
        self.velocidade += velocidade

    def adicionarPosicao(self, posicao):
        self.posicao += posicao

    def atualizarEstado(self):
        self.posicao += self.velocidade * self.ambiente.intervalo_tempo

# Configurações iniciais
DIMENSOES = np.asarray([700,700])  # Dimensões da janela
intervalo_tempo = 0.01  
ambiente = Ambiente(DIMENSOES, intervalo_tempo)
try:
    numero_de_particulas = int(input("Digite o número de partículas: "))
    if numero_de_particulas <= 0:
        raise ValueError("O número de partículas deve ser maior que zero.")
except ValueError as e:
    print(f"Entrada inválida: {e}. Usando valor padrão de 50.")
    numero_de_particulas = 50

# Inicialização do pygame
pygame.init()
tela = pygame.display.set_mode((DIMENSOES[0], DIMENSOES[1]))
pygame.display.set_caption('Simulador de Colisões Elásticas')
relogio = pygame.time.Clock()

# Criação das partículas
for n in range(numero_de_particulas):
    raio = np.random.randint(10, 20)
    massa = raio**3
    posicao = np.random.rand(1, 2) * (DIMENSOES - 2 * raio) + raio
    velocidade = (np.random.rand(1, 2) - 0.5) * 150  # Velocidade inicial
    particula = Particula(ambiente, posicao, velocidade, raio, massa)
    ambiente.adicionarParticula(particula)

# Função para exibir as partículas
def exibir(ambiente):
    for particula in ambiente.particulas:
        pygame.gfxdraw.filled_circle(tela, int(particula.posicao[0][0]), int(particula.posicao[0][1]), particula.raio, particula.cor)

# Loop principal da simulação
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    tela.fill([255, 255, 255])  # Fundo branco
    ambiente.atualizar()
    exibir(ambiente)

    pygame.display.flip()
    relogio.tick(60)  # Limita a 60 FPS

pygame.quit()
