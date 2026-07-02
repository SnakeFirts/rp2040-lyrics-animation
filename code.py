import time
import board
import busio
import adafruit_ssd1306

# ---------- Configuración de hardware ----------
WIDTH = 128
HEIGHT = 64

i2c = busio.I2C(board.GP1, board.GP0)  # SCL, SDA
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

CHAR_WIDTH = 6
LINE_TEXT_HEIGHT = 8  # alto de una línea de texto con la fuente 5x8

# ---------- Tu letra va aquí ----------
# Cada linea es: (texto, segundos que tarda en caer de arriba a abajo)
# Ajusta el tiempo de caída para que combine con el ritmo de tu canción.
LYRICS = [
    ("Primera linea de ejemplo", 2.5),
    ("Segunda linea aqui", 2.5),
    ("Tercera linea de la cancion", 3.0),
    ("Cuarta linea final", 2.0),
]

MAX_CHARS_PER_LINE = WIDTH // CHAR_WIDTH


def wrap_text(text, max_chars=MAX_CHARS_PER_LINE):
    words = text.split(" ")
    lines = []
    current = ""
    for w in words:
        if len(current) + len(w) + 1 <= max_chars:
            current = (current + " " + w).strip()
        else:
            lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def fall_line(text, fall_seconds, fps=30):
    text_px = len(text) * CHAR_WIDTH
    x = max(0, (WIDTH - text_px) // 2)

    y_start = -LINE_TEXT_HEIGHT
    y_end = HEIGHT
    total_distance = y_end - y_start

    steps = max(1, int(fall_seconds * fps))
    delay = fall_seconds / steps

    for step in range(steps + 1):
        y = y_start + int((total_distance * step) / steps)
        oled.fill(0)
        oled.text(text, x, y, 1)
        oled.show()
        time.sleep(delay)

    # asegura pantalla limpia antes de la siguiente línea
    oled.fill(0)
    oled.show()


def play_lyrics_fall(lyrics):
    for text, fall_seconds in lyrics:
        for wrapped in wrap_text(text):
            fall_line(wrapped, fall_seconds)


# ---------- Main ----------
oled.fill(0)
oled.show()
play_lyrics_fall(LYRICS)
