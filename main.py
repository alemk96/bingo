from PIL import Image, ImageDraw, ImageFont
import numpy as np
import textwrap
import random
import os

def get_questions() -> list[str]:
    """
    Retrieves the array of questions.

    Returns:
        np.array: An array of questions.
    """
    with open('questions.txt', 'r') as file:
        questions: list[str] = list(map(lambda x : x.replace("Ã","à").replace("àˆ","È").replace("\xa0","").replace("à¨",""), file.read().splitlines()))

    random.shuffle(questions)
    return questions

def best_rectangle_shape(n: int) -> tuple[int, int]:
    """
    Finds the best rectangular grid shape (rows, cols) for n elements.
    The shape minimizes the difference between rows and columns.

    Args:
        n (int): Total number of elements.

    Returns:
        tuple: A tuple (rows, cols) representing the optimal grid shape.
    """
    # Find all factor pairs of n
    factors: list[int] = [(i, n // i) for i in range(1, int(np.sqrt(n)) + 1) if n % i == 0]

    # Select the pair with the smallest difference between rows and columns
    return min(factors, key=lambda x: abs(x[0] - x[1]))

def find_optimal_font_size(draw: ImageDraw, text: str, max_width: int, max_height: int, font_path: str ="arial.ttf", start_size: int=24) -> tuple[ImageFont, list[str]]: # type: ignore
    """
    Determines the largest font size that fits the text within specified dimensions.

    Args:
        draw (ImageDraw): The ImageDraw instance for text measurement.
        text (str): The text to measure.
        max_width (int): Maximum width for the text.
        max_height (int): Maximum height for the text.
        font_path (str): Path to the font file.
        start_size (int): Initial font size to test.

    Returns:
        tuple: The optimal font and the wrapped text lines.
    """
    font_size: str = start_size
    font: ImageFont = ImageFont.truetype(font_path, font_size)

    while True:
        # Wrap text and calculate its dimensions
        lines: textwrap = textwrap.wrap(text, width=20)
        text_height: int = len(lines) * (font.getbbox("A")[3] - font.getbbox("A")[1])
        text_width: int = max([font.getbbox(line)[2] - font.getbbox(line)[0] for line in lines])

        # Check if the text fits within the specified dimensions
        if text_width <= max_width and text_height <= max_height:
            return font, lines

        # Reduce font size and re-test
        font_size -= 1
        if font_size < 8:  # Minimum font size to avoid infinite loop
            break
        font: ImageFont = ImageFont.truetype(font_path, font_size)

    return font, lines

def draw_question(image: ImageDraw, question: str, x_offset: int, y_offset: int, cell_size: int, font_path: str="roboto.ttf") -> None:
    """
    Draws a question centered within a specified square cell.

    Args:
        image (Image): The image on which to draw the question.
        question (str): The question text to draw.
        x_offset (int): The x-coordinate of the cell's top-left corner.
        y_offset (int): The y-coordinate of the cell's top-left corner.
        cell_size (int): The size (width and height) of the square cell.
        font_path (str): Path to the font file.
    """
    draw: ImageDraw = ImageDraw.Draw(image)
    font, lines = find_optimal_font_size(draw, question, cell_size - 10, cell_size - 10, font_path)
    line_height: int = font.getbbox("A")[3] - font.getbbox("A")[1]
    total_height: int = len(lines) * line_height

    # Calculate vertical starting position for centering
    y_start: int = y_offset + (cell_size - total_height) // 2
    for line in lines:
        # Calculate horizontal starting position for centering
        line_width: int = font.getbbox(line)[2] - font.getbbox(line)[0]
        x_start: int = x_offset + (cell_size - line_width) // 2
        draw.text((x_start, y_start), line, font=font, fill=(0, 0, 0))
        y_start += line_height

def draw_card(name: str, questions: list[str], title: str = "Bingo Card", padding: int = 20, count: int = 1) -> None:
    """
    Draws a bingo card with a grid layout, title, and padding, and saves it as an image file.

    Args:
        name (str): The name of the output image file (without extension).
        questions (list[str]): The array of questions to display in the grid.
        title (str): The title to display at the top of the bingo card.
        padding (int): Padding around the title and grid.
    """
    # Determine grid dimensions
    num_rows, num_cols = best_rectangle_shape(len(questions))
    cell_size: int = 150  # Fixed size for each square cell
    title_height: int = 100  # Reserved height for the title
    image_width: int = cell_size * num_cols + 2 * padding
    image_height: int = cell_size * num_rows + title_height + 2 * padding

    # Create a blank white image
    image: Image = Image.new('RGBA', (image_width, image_height), (255, 255, 255, 255))
    draw: ImageDraw = ImageDraw.Draw(image)

    # Draw the title
    font_path = "roboto.ttf"  # Change to a valid font path on your system
    try:
        font: ImageFont = ImageFont.truetype(font_path, 36)
    except IOError:
        font = ImageFont.load_default()

    # Measure the title dimensions using textbbox
    bbox = draw.textbbox((0, 0), title, font=font)  # Returns (left, top, right, bottom)
    title_width = bbox[2] - bbox[0]
    title_text_height = bbox[3] - bbox[1]

    title_x: int = (image_width - title_width) // 2
    title_y: int = padding + (title_height - title_text_height) // 2
    draw.text((title_x, title_y), title, font=font, fill="black")

    # Draw grid lines
    for x in range(num_cols + 1):
        draw.line([(x * cell_size + padding, title_height + padding), 
                   (x * cell_size + padding, image_height - padding)], fill="black", width=2)
    for y in range(num_rows + 1):
        draw.line([(padding, y * cell_size + title_height + padding), 
                   (image_width - padding, y * cell_size + title_height + padding)], fill="black", width=2)

    # Calculate top-left corner positions for each question cell
    question_positions = [
        (x * cell_size + padding, y * cell_size + title_height + padding)
        for y in range(num_rows)
        for x in range(num_cols)
    ]

    # Draw each question in its respective cell
    for i, question in enumerate(questions):
        if i < len(question_positions):
            x_offset, y_offset = question_positions[i]
            draw_question(image, question, x_offset, y_offset, cell_size)

    # Save the bingo card image
    os.makedirs('generated_bingocards', exist_ok=True)
    
    image.save(f'generated_bingocards/{name}{f"_{count}" if count !=0 else ""}.png')

def bingo(name: str,count: int=1)-> None:
    """
    Generates a bingo card with the provided questions and saves it as an image file.

    Args:
        name (str): The name of the output image file (without extension).
    """
    for i in range(count):
        questions: list[str] = get_questions()
        draw_card(name, questions, title = "Christmas Bingo", count = i )

if __name__ == "__main__":
    bingo('card_bingo',1)
