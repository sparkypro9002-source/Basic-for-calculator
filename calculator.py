import pygame
import sys
pygame.init()
WIDTH, HEIGHT = 400, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Perfect Pygame Calculator")
clock = pygame.time.Clock()
BG_COLOR, DISPLAY_COLOR = (0, 0, 0), (30, 30, 30)
NUM_COLOR, OP_COLOR = (0, 0, 255), (255, 0, 0)
FN_COLOR, EQ_COLOR = (255, 255, 0), (0, 255, 0)
TEXT_LIGHT, TEXT_DARK = (255, 255, 255), (0, 0, 0)
try:
    FONT_DISPLAY = pygame.font.SysFont("Arial", 40, bold=True)
    FONT_BUTTON = pygame.font.SysFont("Arial", 26, bold=True)
except:
    FONT_DISPLAY = pygame.font.Font(None, 40)
    FONT_BUTTON = pygame.font.Font(None, 26)
expression = ""
BUTTON_MAP = [
    ("C", 0, 0, 1, 1, "fn"),    ("+/-", 1, 0, 1, 1, "fn"), ("%", 2, 0, 1, 1, "fn"), ("/", 3, 0, 1, 1, "op"),
    ("7", 0, 1, 1, 1, "num"),   ("8", 1, 1, 1, 1, "num"),  ("9", 2, 1, 1, 1, "num"), ("*", 3, 1, 1, 1, "op"),
    ("4", 0, 2, 1, 1, "num"),   ("5", 1, 2, 1, 1, "num"),  ("6", 2, 2, 1, 1, "num"), ("-", 3, 2, 1, 1, "op"),
    ("1", 0, 3, 1, 1, "num"),   ("2", 1, 3, 1, 1, "num"),  ("3", 2, 3, 1, 1, "num"), ("+", 3, 3, 1, 1, "op"),
    ("0", 0, 4, 1, 1, "num"),   (".", 1, 4, 1, 1, "num"),   ("DEL", 2, 4, 1, 1, "fn"), ("=", 3, 4, 1, 1, "eq")
]
PADDING, GRID_START_Y = 12, 160
BLOCK_W = (WIDTH - (PADDING * 5)) // 4
BLOCK_H = (HEIGHT - GRID_START_Y - (PADDING * 6)) // 5
def get_button_rect(grid_x, grid_y, w_blocks, h_blocks):
    x = PADDING + grid_x * (BLOCK_W + PADDING)
    y = GRID_START_Y + PADDING + grid_y * (BLOCK_H + PADDING)
    w = w_blocks * BLOCK_W + (w_blocks - 1) * PADDING
    h = h_blocks * BLOCK_H + (h_blocks - 1) * PADDING
    return pygame.Rect(x, y, w, h)
def evaluate_expression(expr):
    if not expr: return ""
    try:
        clean_expr = expr.replace(" ", "")
        if any(c.isalpha() for c in clean_expr): return "Error"
        result = eval(clean_expr)
        if isinstance(result, float) and result.is_integer(): return str(int(result))
        res_str = str(round(result, 14))
        return res_str[:16] if len(res_str) > 16 else res_str
    except ZeroDivisionError: return "Error: Div by 0"
    except: return "Error"
def get_current_number(expr):
    """Extract the current number being typed (after the last operator)"""
    for op in ["+", "-", "*", "/"]:
        expr = expr.replace(op, "|")
    return expr.split("|")[-1]
while True:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for label, gx, gy, wb, hb, b_type in BUTTON_MAP:
                if get_button_rect(gx, gy, wb, hb).collidepoint(mouse_pos):
                    if label == "C": expression = ""
                    elif label == "DEL": expression = "" if expression in ["Error", "Error: Div by 0"] else expression[:-1]
                    elif label == "=": expression = evaluate_expression(expression)
                    elif label == "+/-":
                        if expression and expression not in ["Error", "Error: Div by 0"]:
                            expression = expression[1:] if expression.startswith("-") else ("-" + expression if len(expression) < 16 else expression)
                    elif label == "%":
                        if expression and expression not in ["Error", "Error: Div by 0"]:
                            try: expression = str(float(expression) / 100)
                            except: expression = "Error"
                    else:
                        # BUG FIX #3: Prevent multiple decimal points in the current number
                        if label == ".":
                            current_number = get_current_number(expression)
                            if "." in current_number:
                                continue  # Skip adding another decimal point
                        if expression in ["Error", "Error: Div by 0"]: expression = ""
                        if len(expression) < 16: expression += label
    screen.fill(BG_COLOR)
    display_rect = pygame.Rect(PADDING, PADDING, WIDTH - (PADDING * 2), GRID_START_Y - PADDING)
    
    # Rounded main numerical result text card window overlay
    pygame.draw.rect(screen, DISPLAY_COLOR, display_rect, border_radius=15)
    
    disp_text = expression if expression else "0"
    text_surface = FONT_DISPLAY.render(disp_text, True, TEXT_LIGHT)
    text_rect = text_surface.get_rect(right=display_rect.right - 20, centery=display_rect.centery)
    if text_rect.left < display_rect.left + 20:
        text_surface = FONT_DISPLAY.render(disp_text[:16], True, TEXT_LIGHT)
        text_rect = text_surface.get_rect(right=display_rect.right - 20, centery=display_rect.centery)
    screen.blit(text_surface, text_rect)
    for label, gx, gy, wb, hb, b_type in BUTTON_MAP:
        rect = get_button_rect(gx, gy, wb, hb)
        if b_type == "num": 
            base_color = NUM_COLOR
            text_color = TEXT_LIGHT
        elif b_type == "op": 
            base_color = OP_COLOR
            text_color = TEXT_LIGHT
        elif b_type == "eq": 
            base_color = EQ_COLOR
            text_color = TEXT_LIGHT
        else: 
            base_color = FN_COLOR
            text_color = TEXT_DARK
            
        # FIXED: Added border_radius=20 parameter down below to generate curved pill shapes
        pygame.draw.rect(screen, base_color, rect, border_radius=20)
        
        lbl_surface = FONT_BUTTON.render(label, True, text_color)
        screen.blit(lbl_surface, lbl_surface.get_rect(center=rect.center))
    pygame.display.flip()
    clock.tick(60)
