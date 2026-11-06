# Cañón Parabólico - Simulador de tiro parabólico
# Flores Marcos - Lógica de Programación (CESUN)
#
# Controles:
#   Flecha arriba / abajo     -> cambia el ángulo del cañón
#   Flecha derecha / izquierda -> cambia la velocidad del disparo
#   Espacio                   -> dispara
#   R                         -> nuevo objetivo
#   Esc                       -> salir

import math
import random
import pygame

# ---------- Configuración (diccionario con los valores fijos) ----------
CONFIG = {
    "ancho": 1280,
    "alto": 720,
    "fps": 60,
    "gravedad": 9.8,
    "escala": 10,          # pixeles por metro, para que se vea bien en pantalla
    "suelo": 660,          # altura (en Y) donde está el piso
}

# ---------- Colores (tuplas RGB) ----------
COLOR_FONDO = (25, 28, 40)
COLOR_SUELO = (70, 90, 60)
COLOR_CANON = (200, 200, 210)
COLOR_BALA = (255, 200, 60)
COLOR_OBJETIVO = (220, 60, 60)
COLOR_TEXTO = (240, 240, 240)
COLOR_TRAYECTORIA = (120, 120, 140)

# ---------- Estado del juego (variables que cambian) ----------
POS_CANON = (120, CONFIG["suelo"])   # base del cañón
LARGO_CANON = 70


def nuevo_objetivo():
    """Regresa un objetivo en una posición aleatoria sobre el suelo."""
    x = random.randint(500, CONFIG["ancho"] - 80)
    radio = 25
    return {"x": x, "y": CONFIG["suelo"] - radio, "radio": radio}


def punta_canon(angulo):
    """Calcula dónde termina el tubo del cañón según el ángulo."""
    rad = math.radians(angulo)
    x = POS_CANON[0] + LARGO_CANON * math.cos(rad)
    y = POS_CANON[1] - LARGO_CANON * math.sin(rad)
    return (x, y)


def disparar(angulo, velocidad):
    """Crea un proyectil con su velocidad descompuesta en X y Y."""
    rad = math.radians(angulo)
    x, y = punta_canon(angulo)
    return {
        "x": x,
        "y": y,
        "vx": velocidad * math.cos(rad),
        "vy": -velocidad * math.sin(rad),   # negativo porque en pantalla Y crece hacia abajo
        "rastro": [],
    }


def actualizar_proyectil(bala, dt):
    """Mueve la bala un paso usando las fórmulas del tiro parabólico."""
    bala["vy"] += CONFIG["gravedad"] * dt
    bala["x"] += bala["vx"] * dt * CONFIG["escala"]
    bala["y"] += bala["vy"] * dt * CONFIG["escala"]
    bala["rastro"].append((int(bala["x"]), int(bala["y"])))


def hay_colision(bala, objetivo):
    """Checa si la bala tocó el objetivo (distancia entre centros)."""
    dx = bala["x"] - objetivo["x"]
    dy = bala["y"] - objetivo["y"]
    distancia = math.sqrt(dx * dx + dy * dy)
    return distancia <= objetivo["radio"] + 6


def fuera_de_pantalla(bala):
    return (bala["x"] > CONFIG["ancho"] + 50
            or bala["x"] < -50
            or bala["y"] > CONFIG["suelo"] + 10)


def dibujar_escena(screen, fuente, angulo, velocidad, objetivo, bala, puntos, disparos, mensaje):
    screen.fill(COLOR_FONDO)

    # suelo
    pygame.draw.rect(screen, COLOR_SUELO,
                     (0, CONFIG["suelo"], CONFIG["ancho"], CONFIG["alto"] - CONFIG["suelo"]))

    # objetivo
    pygame.draw.circle(screen, COLOR_OBJETIVO, (objetivo["x"], objetivo["y"]), objetivo["radio"])
    pygame.draw.circle(screen, COLOR_TEXTO, (objetivo["x"], objetivo["y"]), objetivo["radio"] // 2, 2)

    # cañón (base + tubo)
    pygame.draw.circle(screen, COLOR_CANON, POS_CANON, 22)
    pygame.draw.line(screen, COLOR_CANON, POS_CANON, punta_canon(angulo), 10)

    # trayectoria y bala
    if bala is not None:
        if len(bala["rastro"]) > 1:
            pygame.draw.lines(screen, COLOR_TRAYECTORIA, False, bala["rastro"], 2)
        pygame.draw.circle(screen, COLOR_BALA, (int(bala["x"]), int(bala["y"])), 7)

    # texto de info
    lineas = [
        f"Angulo: {angulo} grados   (flechas arriba/abajo)",
        f"Velocidad: {velocidad} m/s   (flechas izq/der)",
        f"Puntos: {puntos}   Disparos: {disparos}",
        "Espacio = disparar   R = nuevo objetivo   Esc = salir",
    ]
    y = 20
    for linea in lineas:
        texto = fuente.render(linea, True, COLOR_TEXTO)
        screen.blit(texto, (20, y))
        y += 30

    if mensaje:
        txt = fuente.render(mensaje, True, COLOR_BALA)
        screen.blit(txt, (CONFIG["ancho"] // 2 - txt.get_width() // 2, 160))


def main():
    pygame.init()
    screen = pygame.display.set_mode((CONFIG["ancho"], CONFIG["alto"]))
    pygame.display.set_caption("Cañón Parabólico")
    clock = pygame.time.Clock()
    fuente = pygame.font.SysFont(None, 28)

    angulo = 45
    velocidad = 60
    objetivo = nuevo_objetivo()
    bala = None
    puntos = 0
    disparos = 0
    mensaje = ""
    tiempo_mensaje = 0

    running = True
    while running:
        dt = clock.tick(CONFIG["fps"]) / 1000.0   # segundos que pasaron desde el frame anterior

        # ----- eventos -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE and bala is None:
                    bala = disparar(angulo, velocidad)
                    disparos += 1
                    mensaje = ""
                elif event.key == pygame.K_r:
                    objetivo = nuevo_objetivo()
                    bala = None
                    mensaje = ""

        # teclas mantenidas (para ajustar más rápido)
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]:
            angulo = min(angulo + 1, 89)
        if teclas[pygame.K_DOWN]:
            angulo = max(angulo - 1, 1)
        if teclas[pygame.K_RIGHT]:
            velocidad = min(velocidad + 1, 150)
        if teclas[pygame.K_LEFT]:
            velocidad = max(velocidad - 1, 10)

        # ----- lógica -----
        if bala is not None:
            actualizar_proyectil(bala, dt)

            if hay_colision(bala, objetivo):
                puntos += 1
                mensaje = "¡Le diste! Nuevo objetivo..."
                tiempo_mensaje = 90
                objetivo = nuevo_objetivo()
                bala = None
            elif fuera_de_pantalla(bala):
                mensaje = "Fallaste, ajusta y vuelve a intentar"
                tiempo_mensaje = 90
                bala = None

        if tiempo_mensaje > 0:
            tiempo_mensaje -= 1
            if tiempo_mensaje == 0:
                mensaje = ""

        # ----- dibujo -----
        dibujar_escena(screen, fuente, angulo, velocidad, objetivo, bala, puntos, disparos, mensaje)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
