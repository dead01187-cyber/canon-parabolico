# 🔀 Flujo de trabajo con ramas

Aquí explico cómo voy a organizar el trabajo en las ramas durante el curso, para que cualquiera que entre al repo entienda qué hay en cada una.

## Las ramas

```
main ──────────────●──────────────●────────── (estable)
                   ↑              ↑
v01 ───●─────●─────●──────●───────●────────── (trabajo / integración)
       ↑     ↑
actividad_uno    actividad_dos
```

- **`main`** — Es la versión estable del proyecto. Nunca trabajo directo aquí. Solo recibe merges desde `v01` cuando ya probé que todo corre sin errores. Si alguien clona el repo y corre `main`, tiene que funcionar.

- **`v01`** — Es mi rama de trabajo. Aquí junto los avances de las actividades, los pruebo juntos y los voy acomodando. Cuando algo queda listo lo paso a `main` con un merge. Más adelante, cuando el proyecto cambie mucho, puedo abrir `v02`, `v03`, etc.

- **`actividad_uno`** — Plantilla base de Pygame: ventana, game loop, manejo del evento `QUIT` y control de FPS. Es el punto de partida de todo.

- **`actividad_dos`** — Primer avance del simulador de tiro parabólico: el cañón, el objetivo aleatorio y los controles de ángulo y velocidad.

Si más adelante hago una `actividad_tres`, sigue la misma lógica: una rama por actividad con el avance de esa sesión.

## El ciclo que sigo

1. Creo una rama para la actividad o el cambio que voy a hacer.
   ```bash
   git checkout -b actividad_tres v01
   ```
2. Trabajo ahí y hago commits chicos y frecuentes, con mensajes que digan qué cambió:
   ```bash
   git commit -m "Agrega cálculo de trayectoria con seno y coseno"
   ```
3. Cuando el avance funciona, lo integro a `v01`:
   ```bash
   git checkout v01
   git merge actividad_tres
   ```
4. Corro el juego en `v01` y confirmo que no se rompió nada.
   ```bash
   python main.py
   ```
5. Si todo bien, paso `v01` a `main`:
   ```bash
   git checkout main
   git merge v01
   git push --all origin
   ```

## Reglas que me puse

- **No trabajo directo en `main`.** Siempre paso por `v01`.
- **Pruebo antes de hacer merge.** Si en `v01` algo falla, lo arreglo ahí antes de tocar `main`.
- **Mensajes de commit descriptivos.** "Agrega sprite del jugador" sí; "cambios" o "fix" no.
- **Si hay conflicto**, no borro ramas. Lo resuelvo con calma o lo documento y lo pregunto en clase.
- **No borro las ramas de actividades** después del merge, porque son la evidencia de cada sesión.

## Para ver el grafo

```bash
git log --oneline --graph --all --decorate
```

O en GitHub: pestaña **Insights → Network**.
