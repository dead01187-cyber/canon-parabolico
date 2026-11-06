# 🎯 Cañón Parabólico

Simulador de tiro parabólico hecho en Python con Pygame.

**Alumno:** Flores Marcos
**Materia:** Lógica de Programación — CESUN
**Librería:** Pygame

## ¿De qué va el juego?

Hay un cañón en la parte izquierda de la pantalla y un objetivo que aparece en una posición aleatoria. Yo ajusto el ángulo y la velocidad del disparo, lanzo el proyectil y veo si le doy. La bala sigue una trayectoria parabólica real, o sea, usa las fórmulas de física que ya conocemos (componentes en X y Y, gravedad, etc.).

## Objetivo general

Que el jugador pueda ajustar ángulo y velocidad de un cañón para acertar a un objetivo aleatorio, y de paso practicar los temas del curso: ciclos, eventos, funciones, condicionales y estructuras de datos, todo aplicado en algo que se ve en pantalla y se puede jugar.

## Cómo correrlo

```bash
python -m venv .venv
source .venv/bin/activate      # en Windows: .venv\Scripts\activate
pip install pygame
python main.py
```

## Ramas del repositorio

| Rama | Para qué sirve |
|------|----------------|
| `main` | Versión estable. Solo entra código que ya probé. |
| `v01` | Rama de trabajo. Aquí junto los avances y desde aquí hago merge a `main`. |
| `actividad_uno` | Plantilla base de Pygame (ventana, game loop, eventos). |
| `actividad_dos` | Primer avance del simulador de tiro parabólico. |

El detalle de cómo trabajo con las ramas está en [FLUJO.md](FLUJO.md).

---

## 📚 Investigación: Pygame

### ¿Qué es Pygame y para qué se utiliza?

Pygame es un conjunto de módulos de Python para hacer videojuegos y programas multimedia en 2D. Por debajo usa SDL, que es una librería en C que se encarga de hablar con el hardware: la ventana, el teclado, el mouse, el sonido, etc. Pygame lo que hace es envolver todo eso para que yo lo pueda usar desde Python sin meterme en cosas de bajo nivel.

Se usa sobre todo para:

- Juegos 2D (plataformas, arcade, puzzles, simuladores como el mío).
- Prototipos rápidos, porque con pocas líneas ya tienes una ventana con algo moviéndose.
- Enseñar programación, porque ves el resultado de inmediato en pantalla.
- Cosas que no son juegos pero necesitan gráficos: visualizaciones, simulaciones de física, etc.

Lo que me gusta es que no te obliga a usar un editor visual ni un motor pesado. Es puro código Python y tú decides cómo organizar todo.

### ¿Cómo se relaciona Pygame con los temas vistos en clase?

Esto es lo que más me sorprendió: básicamente todo lo que vimos en el curso aparece en un programa de Pygame.

**Ciclos.** El corazón de cualquier juego es el *game loop*, que es un `while running:` que se repite 60 veces por segundo. En cada vuelta se revisan los eventos, se actualiza la lógica y se dibuja todo de nuevo. Sin ciclos no hay juego.

**Eventos.** Pygame guarda en una cola todo lo que pasa (una tecla, un clic, cerrar la ventana). Con `for event in pygame.event.get():` recorro esa cola y con `if event.type == pygame.QUIT:` decido qué hacer. Son ciclos y condicionales trabajando juntos.

**Condicionales.** Las uso para todo: saber si el proyectil tocó el objetivo, si se salió de la pantalla, si el jugador presionó espacio, si el ángulo ya llegó al máximo, etc.

**Variables y operadores.** La posición, la velocidad, el ángulo, la gravedad, los puntos. En el tiro parabólico hay bastante matemática: descompongo la velocidad con seno y coseno y voy actualizando la posición en cada frame.

**Funciones.** En vez de tener todo en el ciclo principal, separo el código en funciones como `dibujar_canon()`, `calcular_posicion()` o `hay_colision()`. Así el loop queda limpio y cada parte se puede probar por separado.

**Estructuras de datos.** Las posiciones y colores son tuplas `(x, y)` o `(r, g, b)`. Si quiero varios proyectiles o varios objetivos uso listas. Para la configuración del juego (ancho, alto, FPS, gravedad) me conviene un diccionario.

**Módulos.** Pygame mismo está dividido en módulos (`pygame.display`, `pygame.draw`, `pygame.event`, `pygame.time`...) y eso me enseña a organizar mi propio código en archivos separados.

En resumen, Pygame no es un tema nuevo que se agrega al curso, es donde se juntan todos los temas y se ven en pantalla.

### ¿Qué significa que Pygame permite "tomar mucho o poco" de la librería?

Esto lo entendí leyendo la documentación oficial. Pygame es **modular**: tú eliges qué partes usar y cuáles no. No es un motor que te impone una estructura. La idea es que *tú controlas el ciclo principal* y tú llamas a las funciones de Pygame cuando las necesitas; Pygame nunca llama a tu código por su cuenta.

**Tomar poco** es usar solo lo mínimo. En mi simulador, por ejemplo, uso `pygame.display` para la ventana, `pygame.draw` para dibujar el cañón y el proyectil con figuras simples, `pygame.event` para leer el teclado, `pygame.time` para controlar los FPS y `pygame.font` para mostrar el ángulo y la velocidad. Toda la física la hago yo a mano con matemáticas, no uso ningún sistema de Pygame para eso.

**Tomar mucho** sería meterle más herramientas de la librería: `pygame.sprite` para manejar los objetos del juego con clases y grupos, `pygame.image` para cargar imágenes en lugar de dibujar figuras, `pygame.mixer` para sonidos y música, `pygame.mask` para colisiones precisas con la forma de la imagen, y así.

Lo bueno es que puedo empezar tomando poco y, conforme el proyecto crece, ir agregando módulos sin tener que reescribir todo. Incluso podría cambiar una parte por otra librería (por ejemplo usar otro sistema de sonido) y Pygame no se queja. Por eso se adapta tanto a un ejercicio de clase como a un juego completo.

### Fuentes

- Documentación oficial de Pygame: https://www.pygame.org/docs/
- Página "About" de Pygame: https://www.pygame.org/wiki/about
- Ejemplos y plantilla base vistos en clase.
