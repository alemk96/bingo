import argparse
import math
import random
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

NUM_QUESTIONS = 25
CELL_SIZE = 150
TITLE_HEIGHT = 100
TITLE_FONT_SIZE = 36
WRAP_WIDTH = 20
MIN_FONT_SIZE = 8
START_FONT_SIZE = 30
FONT_PATH = Path(__file__).parent / "roboto.ttf"
OUTPUT_DIR = Path("generated_bingocards")


def load_questions(path: Path) -> list[str]:
    """
    Reads questions from a UTF-8 text file, one per line.

    Args:
        path (Path): Path of the questions file.

    Returns:
        list[str]: Cleaned, non-empty questions.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    cleaned = (line.replace("\xa0", "").strip() for line in lines)
    return [line for line in cleaned if line]


def get_questions(questions: list[str], k: int = NUM_QUESTIONS) -> list[str]:
    """
    Randomly selects k distinct questions without altering the input list.

    Args:
        questions (list[str]): Pool of available questions.
        k (int): Number of questions to select.

    Returns:
        list[str]: The selected questions.
    """
    return random.sample(questions, min(k, len(questions)))


def best_rectangle_shape(n: int) -> tuple[int, int]:
    """
    Finds the best rectangular grid shape (rows, cols) for n elements.
    The shape minimizes the difference between rows and columns.

    Args:
        n (int): Total number of elements.

    Returns:
        tuple: A tuple (rows, cols) representing the optimal grid shape.
    """
    rows = max(i for i in range(1, math.isqrt(n) + 1) if n % i == 0)
    return rows, n // rows


def line_height(font: ImageFont.FreeTypeFont) -> int:
    """Returns the height of a single text line for the given font."""
    ascent, descent = font.getmetrics()
    return ascent + descent


def text_width(font: ImageFont.FreeTypeFont, text: str) -> int:
    """Returns the rendered width of text for the given font."""
    left, _, right, _ = font.getbbox(text)
    return right - left


def find_optimal_font_size(
    text: str,
    max_width: int,
    max_height: int,
    font_path: Path = FONT_PATH,
    start_size: int = START_FONT_SIZE,
) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    """
    Determines the largest font size that fits the text within specified dimensions.

    Args:
        text (str): The text to measure.
        max_width (int): Maximum width for the text.
        max_height (int): Maximum height for the text.
        font_path (Path): Path to the font file.
        start_size (int): Initial font size to test.

    Returns:
        tuple: The optimal font and the wrapped text lines.
    """
    lines = textwrap.wrap(text, width=WRAP_WIDTH)
    for size in range(start_size, MIN_FONT_SIZE - 1, -1):
        font = ImageFont.truetype(str(font_path), size)
        fits_height = len(lines) * line_height(font) <= max_height
        fits_width = max(text_width(font, line) for line in lines) <= max_width
        if fits_width and fits_height:
            break
    return font, lines


def draw_question(
    image: Image.Image,
    question: str,
    x_offset: int,
    y_offset: int,
    cell_size: int,
    font_path: Path = FONT_PATH,
) -> None:
    """
    Draws a question centered within a specified square cell.

    Args:
        image (Image.Image): The image on which to draw the question.
        question (str): The question text to draw.
        x_offset (int): The x-coordinate of the cell's top-left corner.
        y_offset (int): The y-coordinate of the cell's top-left corner.
        cell_size (int): The size (width and height) of the square cell.
        font_path (Path): Path to the font file.
    """
    draw = ImageDraw.Draw(image)
    font, lines = find_optimal_font_size(question, cell_size - 10, cell_size - 10, font_path)
    height = line_height(font)

    y = y_offset + (cell_size - len(lines) * height) // 2
    for line in lines:
        x = x_offset + (cell_size - text_width(font, line)) // 2
        draw.text((x, y), line, font=font, fill=(0, 0, 0))
        y += height


def draw_card(
    path: Path,
    questions: list[str],
    title: str = "Bingo Card",
    padding: int = 20,
) -> None:
    """
    Draws a bingo card with a grid layout, title, and padding, and saves it as an image file.

    Args:
        path (Path): Output image file path.
        questions (list[str]): The questions to display in the grid.
        title (str): The title to display at the top of the bingo card.
        padding (int): Padding around the title and grid.
    """
    num_rows, num_cols = best_rectangle_shape(len(questions))
    image_width = CELL_SIZE * num_cols + 2 * padding
    image_height = CELL_SIZE * num_rows + TITLE_HEIGHT + 2 * padding

    image = Image.new("RGBA", (image_width, image_height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)

    try:
        title_font = ImageFont.truetype(str(FONT_PATH), TITLE_FONT_SIZE)
    except OSError:
        title_font = ImageFont.load_default()

    left, top, right, bottom = draw.textbbox((0, 0), title, font=title_font)
    title_x = (image_width - (right - left)) // 2
    title_y = padding + (TITLE_HEIGHT - (bottom - top)) // 2
    draw.text((title_x, title_y), title, font=title_font, fill="black")

    grid_top = TITLE_HEIGHT + padding
    for col in range(num_cols + 1):
        x = col * CELL_SIZE + padding
        draw.line([(x, grid_top), (x, image_height - padding)], fill="black", width=2)
    for row in range(num_rows + 1):
        y = row * CELL_SIZE + grid_top
        draw.line([(padding, y), (image_width - padding, y)], fill="black", width=2)

    for i, question in enumerate(questions):
        row, col = divmod(i, num_cols)
        draw_question(image, question, col * CELL_SIZE + padding, row * CELL_SIZE + grid_top, CELL_SIZE)

    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def bingo(questions: list[str], name: str, count: int = 1, title: str = "Bingo Card") -> None:
    """
    Generates bingo cards from the question pool and saves them as image files.

    Args:
        questions (list[str]): Pool of available questions.
        name (str): Base name of the output image files (without extension).
        count (int): Number of bingo cards to generate.
        title (str): Title displayed on each card.
    """
    for index in range(1, count + 1):
        card_questions = get_questions(questions)
        draw_card(OUTPUT_DIR / f"{name}_{index}.png", card_questions, title=title)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate bingo cards from a list of questions.")
    parser.add_argument("-q", "--questions", type=Path, default=Path("questions.txt"), help="questions file")
    parser.add_argument("-n", "--count", type=int, default=2, help="number of cards to generate")
    parser.add_argument("-t", "--title", default="Christmas Bingo", help="card title")
    parser.add_argument("--name", default="card_bingo", help="base name of output files")
    args = parser.parse_args()

    bingo(load_questions(args.questions), args.name, args.count, args.title)


if __name__ == "__main__":
    main()
