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
- `numpy`: For mathematical calculations.
- `textwrap`: For text wrapping.
- `random`: For shuffling questions.
- `os`: For directory and file handling.

---

## Functions

### 1. **`get_questions`**
```python
def get_questions() -> list[str]:
```
Reads questions from `questions.txt`, replaces unwanted characters, shuffles the questions, and returns them as a list.

- **Returns:** `list[str]` - List of cleaned and shuffled questions.

---

### 2. **`best_rectangle_shape`**
```python
def best_rectangle_shape(n: int) -> tuple[int, int]:
```
Determines the optimal rectangular grid shape (rows, columns) for a given number of elements to minimize the difference between rows and columns.

- **Parameters:**
  - `n (int)`: Total number of elements.
- **Returns:** `tuple[int, int]` - Optimal `(rows, cols)` grid shape.

---

### 3. **`find_optimal_font_size`**
```python
def find_optimal_font_size(draw: ImageDraw, text: str, max_width: int, max_height: int, font_path: str ="arial.ttf", start_size: int=24) -> tuple[ImageFont, list[str]]:
```
Finds the largest font size that fits the given text within specified dimensions, wrapping text as necessary.

- **Parameters:**
  - `draw (ImageDraw)`: Instance used for text measurement.
  - `text (str)`: The text to be displayed.
  - `max_width (int)`: Maximum allowed width for the text.
  - `max_height (int)`: Maximum allowed height for the text.
  - `font_path (str)`: Path to the font file.
  - `start_size (int)`: Initial font size to test.
- **Returns:** 
  - `ImageFont`: Font object with the optimal size.
  - `list[str]`: Wrapped lines of text.

---

### 4. **`draw_question`**
```python
def draw_question(image: ImageDraw, question: str, x_offset: int, y_offset: int, cell_size: int, font_path: str="roboto.ttf") -> None:
```
Draws a question centered within a square cell on the image.

- **Parameters:**
  - `image (Image)`: The image canvas for drawing.
  - `question (str)`: Text to display.
  - `x_offset (int)`: X-coordinate of the cell's top-left corner.
  - `y_offset (int)`: Y-coordinate of the cell's top-left corner.
  - `cell_size (int)`: Size of the square cell.
  - `font_path (str)`: Path to the font file.

---

### 5. **`draw_card`**
```python
def draw_card(name: str, questions: list[str], title: str = "Bingo Card", padding: int = 20, count: int = 1) -> None:
```
Creates a bingo card image with a title and a grid layout of questions.

- **Parameters:**
  - `name (str)`: Name of the output image file (without extension).
  - `questions (list[str])`: List of questions to populate the grid.
  - `title (str)`: Title displayed at the top of the card.
  - `padding (int)`: Padding around the title and grid.
  - `count (int)`: Card count identifier for saving multiple images.

---

### 6. **`bingo`**
```python
def bingo(name: str, count: int=1) -> None:
```
Generates one or more bingo cards with questions fetched from the text file.

- **Parameters:**
  - `name (str)`: Name of the output image file (without extension).
  - `count (int)`: Number of bingo cards to generate.

---

## How to Use

1. **Prepare the Questions:**
   - Create a text file named `questions.txt` in the same directory as the script.
   - Add one question per line.

2. **Run the Script:**
   - Execute the script from the command line or an IDE:
     ```bash
     python bingo_card_generator.py
     ```
   - By default, it generates one card. Modify the `count` argument in the `bingo` function to create multiple cards.

3. **Locate the Output:**
   - Generated bingo cards are saved in the `generated_bingocards` folder.

---

## Customization
- Change `cell_size`, `title`, and `padding` in the `draw_card` function for personalized designs.
- Modify `font_path` to use different fonts. Ensure the `.ttf` file is available locally.

