# Bingo Card Generator

## :warning: Experimental and very nightly version

This Python script generates bingo cards with customizable grids, titles, and text content. The cards are saved as images with a professional layout, making them ideal for events or games. For the meme and having fun at christmas lunch.


## Disclaimer
This script is intended for educational purposes and fun activities. It is not intended for commercial use or professional applications. The script may contain bugs or limitations due to its experimental nature. 

Due the goliardic nature of the script, the author is not responsible for any misuse or misinterpretation of the generated bingo cards. Use at your own risk.

All documentation is AI-generated. Dude, is for the meme, not a serious project. Enjoy! :smile:


---

## Overview

### Features:
- Reads questions from a text file.
- Automatically arranges questions into an optimal grid layout.
- Dynamically adjusts font size to fit text within cells.
- Creates visually appealing bingo cards with a title and grid.
- Supports multiple bingo cards generation in a single run.

### Libraries Used:
- `pillow`: For image creation and drawing.
- Standard library: `argparse`, `math`, `pathlib`, `random`, `textwrap`.

---

## Functions

- `load_questions(path)`: reads a UTF-8 file, one question per line, skipping empty lines.
- `get_questions(questions, k=25)`: picks `k` distinct random questions without mutating the pool.
- `best_rectangle_shape(n)`: returns the `(rows, cols)` grid closest to a square for `n` cells.
- `find_optimal_font_size(text, max_width, max_height, ...)`: largest font size that fits the wrapped text; returns `(font, lines)`.
- `draw_question(image, question, x_offset, y_offset, cell_size, ...)`: draws a question centered in a cell.
- `draw_card(path, questions, title, padding)`: renders a card and saves it to `path`.
- `bingo(questions, name, count, title)`: generates `count` cards in `generated_bingocards/`.

---

## How to Use

1. **Prepare the Questions:**
   - Create a text file named `questions.txt` in the same directory as the script.
   - Add one question per line.

2. **Run the Script:**
   - Install dependencies and run with [uv](https://docs.astral.sh/uv/):
     ```bash
     uv sync
     uv run main.py --count 4 --title "Christmas Bingo"
     ```
   - Options: `-q/--questions` (file, default `questions.txt`), `-n/--count` (default 2), `-t/--title`, `--name` (output base name).

3. **Locate the Output:**
   - Generated bingo cards are saved in the `generated_bingocards` folder.

---

## Customization
- Change the constants at the top of `main.py` (`CELL_SIZE`, `NUM_QUESTIONS`, `FONT_PATH`, ...) for personalized designs.
- Point `FONT_PATH` to a different font. Ensure the `.ttf` file is available locally.

