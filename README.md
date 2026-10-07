# ♟️ Python Chess Engine

> A chess engine built from scratch in Python, focusing on understanding board representation, piece movement, and chess move generation.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Status](https://img.shields.io/badge/Status-In%20Development-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 🧠 About

This project is a **chess engine written from scratch in Python**.

The main goal is to understand how a chess engine works internally — from representing pieces on an 8×8 board to generating possible moves and handling special chess rules.

The project is intentionally being built step-by-step rather than relying on an existing chess library.

---

## ✨ Current Focus

The engine currently focuses on **board representation and pseudo-legal move generation**.

Implemented / being developed:

* ♟️ 8×8 board representation
* ♔ Piece and color encoding
* ♙ Pawn movement
* ♞ Knight movement
* ♗ Bishop movement
* ♖ Rook movement
* ♕ Queen movement
* ♔ King movement
* 👑 Pawn promotion
* 🏰 Castling
* 🫥 En passant
* 🔄 Move representation

More advanced chess rules will be added as the project develops.

---

# 📂 Project Structure

The project intentionally keeps a simple structure:

```text
PyChess/
│
├── board.py        # Board class and move generation
├── move.py         # Move class
├── constants.py    # Piece and color constants
├── test.py         # Testing and demo script
└── README.md       # Project documentation
```

### `constants.py`

Contains the basic piece and color definitions.

```python
EMPTY = 0

PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6

WHITE = 8
BLACK = 16
```

---

### `move.py`

Contains the `Move` class.

A move stores information such as:

```text
Source square
Destination square
Promotion piece
Castling
En passant
```

Example:

```python
Move(1, 4, 3, 4)
```

represents:

```text
e2 → e4
```

Moves can also be represented using coordinate notation:

```text
e2e4
g1f3
e7e8q
```

---

### `board.py`

Contains the main `Board` class.

Responsibilities include:

* Creating the board
* Setting up the initial position
* Tracking game state
* Reading pieces from squares
* Generating pawn moves
* Generating knight moves
* Generating sliding-piece moves
* Generating king moves
* Handling special-move information
* Generating pseudo-legal moves

The board is represented as an 8×8 matrix:

```python
self.board[row][col]
```

---

### `test.py`

Used for testing and demonstrating the engine while development is ongoing.

This file will be used to verify individual components such as:

```text
Board initialization
Piece placement
Move generation
Pawn promotion
Castling
En passant
```

---

# ♟️ Board Representation

The engine uses a simple **8×8 Python list**:

```python
self.board = [[EMPTY for _ in range(8)] for _ in range(8)]
```

The coordinate system is:

```text
        a   b   c   d   e   f   g   h
      +---+---+---+---+---+---+---+---+
  8   |   |   |   |   |   |   |   |   |
      +---+---+---+---+---+---+---+---+
  7   |   |   |   |   |   |   |   |   |
      +---+---+---+---+---+---+---+---+
  6   |   |   |   |   |   |   |   |   |
      +---+---+---+---+---+---+---+---+
  5   |   |   |   |   |   |   |   |   |
      +---+---+---+---+---+---+---+---+
  4   |   |   |   |   |   |   |   |   |
      +---+---+---+---+---+---+---+---+
  3   |   |   |   |   |   |   |   |   |
      +---+---+---+---+---+---+---+---+
  2   |   |   |   |   |   |   |   |   |
      +---+---+---+---+---+---+---+---+
  1   |   |   |   |   |   |   |   |   |
      +---+---+---+---+---+---+---+---+
```

Internally:

```text
row 0 → rank 1
row 7 → rank 8

col 0 → file a
col 7 → file h
```

Therefore:

```text
board[0][0] → a1
board[0][4] → e1
board[1][4] → e2
board[7][4] → e8
```

---

# 🔢 Piece Encoding

Pieces are represented using integers rather than strings.

### Piece Types

```python
EMPTY  = 0
PAWN   = 1
KNIGHT = 2
BISHOP = 3
ROOK   = 4
QUEEN  = 5
KING   = 6
```

### Colors

```python
WHITE = 8
BLACK = 16
```

A piece is created by combining its color and type:

```python
WHITE | PAWN
```

which produces:

```text
9
```

For example:

```python
WHITE | QUEEN
```

produces:

```text
13
```

while:

```python
BLACK | KING
```

produces:

```text
22
```

---

# 🧩 Bitwise Piece Information

Because color and piece type are encoded into the same integer, bitwise operations can retrieve them.

### Get Piece Type

```python
piece_type = piece & 7
```

### Get Color

```python
color = piece & 24
```

For example:

```python
piece = WHITE | QUEEN

piece_type = piece & 7
color = piece & 24
```

Results:

```text
piece_type → QUEEN
color      → WHITE
```

This provides a compact way of storing chess pieces.

---

# ♟️ Move Generation

Move generation is divided by piece type.

```text
Pawn
 ↓
generate_pawn_moves()

Knight
 ↓
generate_knight_moves()

Bishop
 ↓
generate_bishop_moves()

Rook
 ↓
generate_rook_moves()

Queen
 ↓
generate_queen_moves()

King
 ↓
generate_king_moves()
```

Sliding pieces use a shared movement function:

```python
generate_sliding_moves()
```

This is used by:

```text
♗ Bishop
♖ Rook
♕ Queen
```

because all three pieces move along one or more straight-line directions until they encounter another piece.

---

# 🐇 Pawn Movement

Pawn move generation includes:

### Single Push

```text
e2 → e3
```

### Double Push

```text
e2 → e4
```

### Captures

```text
e4 × d5
```

### Promotion

When a pawn reaches the final rank, the engine generates possible promotions:

```text
♕ Queen
♖ Rook
♗ Bishop
♘ Knight
```

For example:

```text
e7 → e8q
e7 → e8r
e7 → e8b
e7 → e8n
```

---

# 🏰 Special Moves

The board maintains information required for special chess moves.

### Castling Rights

```python
self.castling_rights = {
    'K': True,
    'Q': True,
    'k': True,
    'q': True
}
```

Where:

```text
K → White kingside
Q → White queenside
k → Black kingside
q → Black queenside
```

### En Passant

The current en-passant target square is tracked using:

```python
self.en_passant_square
```

---

# 🔄 Pseudo-Legal Moves

The current move generator is designed around **pseudo-legal moves**.

A pseudo-legal move follows the movement rules of the piece but does not necessarily guarantee that the player's king remains safe.

Eventually, the engine will need to filter these moves:

```text
Pseudo-legal moves
        │
        ▼
    Make move
        │
        ▼
Check king safety
        │
        ▼
   Undo move
        │
        ▼
  Legal moves
```

This will eventually allow the engine to correctly handle:

* Check
* Checkmate
* Stalemate
* Pins
* Discovered attacks
* Legal castling

---

# 🗺️ Roadmap

## Phase 1 — Board

* [x] 8×8 board
* [x] Piece constants
* [x] Color encoding
* [x] Initial position
* [x] Piece lookup

## Phase 2 — Move Generation

* [x] Pawn movement
* [x] Pawn captures
* [x] Double pawn push
* [x] Knight movement
* [x] Bishop movement
* [x] Rook movement
* [x] Queen movement
* [x] King movement
* [x] Promotion generation
* [ ] Fully validated castling
* [ ] Fully validated en passant

## Phase 3 — Legal Chess

* [ ] Move execution
* [ ] Undo moves
* [ ] Attack detection
* [ ] King location
* [ ] Check detection
* [ ] Legal move filtering
* [ ] Checkmate
* [ ] Stalemate
* [ ] Draw detection

## Phase 4 — Notation & Position Handling

* [ ] FEN parsing
* [ ] FEN generation
* [ ] Algebraic notation
* [ ] PGN support

## Phase 5 — Chess Engine

* [ ] Position evaluation
* [ ] Material evaluation
* [ ] Minimax
* [ ] Alpha-Beta pruning
* [ ] Move ordering
* [ ] Quiescence search
* [ ] Transposition tables

## Phase 6 — Interface

* [ ] Command-line interface
* [ ] Interactive chess game
* [ ] GUI
* [ ] Human vs AI
* [ ] Engine vs Engine
* [ ] UCI support

---

# 🧪 Running the Project

Clone the repository:

```bash
git clone https://github.com/Subhodip57/PyChess.git
cd PyChess
```

Run the test/demo script:

```bash
python test.py
```

---

# 🎯 Philosophy

This project is being built **one concept at a time**.

Instead of immediately using a chess library or implementing a complete engine, the goal is to understand what actually happens underneath:

```text
Board
  ↓
Pieces
  ↓
Moves
  ↓
Legal Moves
  ↓
Game State
  ↓
Position Evaluation
  ↓
Search
  ↓
Chess Engine
```

The final objective is to turn a simple Python board into a functioning chess engine.

---

# 📊 Project Status

```text
███████░░░░░░░░░░░░░  Early Development
```

🚧 **The engine is actively being developed.**

The current implementation is focused primarily on the fundamentals of board representation and move generation.

---

## 👨‍💻 Author

**Subhodip Laha**

Built from scratch with Python ♟️

> *One move at a time.*
