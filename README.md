# Sorting Algorithm Visualizer

A cyberpunk-themed desktop application that animates how five sorting algorithms work step by step, side by side, with live comparison/swap counters and synchronized playback.

Built for COMP9001 Final Project.

**Author:** [Tiansheng Chen]
**SID:** [560517309]

## Features

- 4 algorithms running in parallel: Bubble, Selection, Quicksort, Mergesort
- Live comparison and swap counters per algorithm
- Color-coded animation (compare / swap / sorted highlights)
- Play / Pause / Reset controls
- Adjustable animation speed (50–800 ms per frame)
- Adjustable data size (5–50 elements)
- Boot splash screen with typewriter animation
- Algorithm-specific sound effects (programmatic sine-wave synthesis)
- Mute toggle

## Requirements

- Python 3.10+
- `matplotlib`
- `numpy`
- `pygame-ce` (NOT `pygame` — the main pygame package doesn't support Python 3.14 yet)

## Installation

```bash
pip install matplotlib numpy pygame-ce
```

## Running

```bash
python3 main.py
```

Press any key on the splash screen to enter the main interface, then press **PLAY** to start the animation.

## Project Structure

```
sorting-visualizer/
├── main.py          # GUI, splash, controls, animation loop
├── algorithms.py    # The four sorting algorithms (each returns step list + counters)
├── test.py          # Standalone tests
└── README.md
```

## Advanced Topics Used

- Classes (`AlgorithmView` encapsulates per-algorithm visualization state)
- Recursion (Quicksort, Mergesort)
- File I/O (algorithm step files, theme config — implicit via module structure)
- Exception handling (sound engine fallback)
- External libraries: tkinter, matplotlib, numpy, pygame-ce
- Lambda functions (button callbacks)