# Tic-Tac-Toe with AI — Python & Pygame

A desktop Tic-Tac-Toe (noughts and crosses) game built in Python using the **Pygame** library. Features a graphical user interface, player-versus-AI gameplay, customizable starting turns (play as `X` or `O`), and three selectable difficulty levels.

---

## 🧠 1. The Decision Tree (Minimax Algorithm)

The AI's intelligence is powered by a **Decision Tree** explored using the **Minimax Algorithm**, implemented in the `minimax` function.

### Tree Traversal & Recursion
The AI simulates all possible sequences of future turns:
- When it is the **AI's turn**, it acts as the **maximizing player** — trying to achieve the highest score.
- When it is the **human's turn**, it simulates the **minimizing player** — assuming the human will make the best move to lower the AI's score.

### Terminal Scores
When a simulation reaches a terminal game state (win, loss, or tie), it returns a static score adjusted by the current tree depth to favor **faster wins** and **slower losses**:

| Outcome | Score |
|---------|-------|
| AI Win | `+10 − depth` |
| Human Win | `depth − 10` |
| Tie | `0` |

### Depth Limits (Difficulty Modes)
Exploring the full decision tree is computationally feasible for Tic-Tac-Toe, but difficulty is controlled by **limiting the search depth**:

| Difficulty | Depth Cap | Behavior |
|------------|-----------|----------|
| 🟢 Easy (`Fácil`) | 3 levels | Very limited lookahead |
| 🟡 Medium (`Medio`) | 5 levels | Moderate lookahead |
| 🔴 Hard (`Difícil`) | No limit (`None`) | Perfect play — searches to the end of the game tree |

---

## 📐 2. Board Heuristics & Evaluation

When the AI's search reaches its **depth limit** before hitting a terminal state (e.g., in Easy or Medium modes), it uses a **Heuristic Evaluation Function** to estimate board quality instead of a definitive outcome.

### Board Assessment
The function `evaluar_heuristica_tablero` aggregates scores across all **8 winning lines** — 3 rows, 3 columns, and 2 diagonals — using `evaluar_linea`.

### Line Evaluation Heuristics

**Blocked lines** — if a line contains both AI and Human pieces, it cannot be won by either side and scores `0`.

**AI Dominance (positive points):**

| AI Pieces in Line | Score |
|-------------------|-------|
| 3 | `+3` |
| 2 | Random from `[-4, 0, 1]` *(introduces unpredictability at lower difficulties)* |
| 1 | `+0.2` |

**Human Threats (negative points):**

| Human Pieces in Line | Score |
|----------------------|-------|
| 3 | `−3` |
| 2 | Random from `[0, −0.5]` |
| 1 | `0` |

This heuristic allows the AI to **approximate board strength** and **block threats** even when it cannot calculate the final outcome of the game.

---

## 🎮 3. Graphics & GUI (Pygame Integration)

All visuals, mouse events, and state updates are managed by the **Pygame** framework.

### Custom Assets
The game loads the following graphical resources:

| Asset | File |
|-------|------|
| Game background | `fondo_rayas.jpg` |
| X token | `x.PNG` |
| O token | `o.PNG` |
| Difficulty buttons | `facil_medio_dificil.PNG` |
| Restart button | `reiniciar.PNG` |
| Exit button | `salir.PNG` |

Text is rendered using the **Broadway** font.

### State Machine Layout
The game loop cycles through three main screens, controlled by the `pantalla_actual` state variable:

```
menu → elegir_turno → jugando
```

| State | Description |
|-------|-------------|
| `menu` | Renders the difficulty selection panel |
| `elegir_turno` | Asks the player whether to go first (`X`) or second (`O`) |
| `jugando` | Draws the 3×3 grid via `graficar_tablero`, renders tokens at pre-defined coordinate bounds, and displays overlay screens for win/tie announcements along with **Exit** and **Restart** buttons |
