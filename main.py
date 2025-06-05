# ID: 3135717
# Lab: 08

from tkinter.filedialog import askopenfilename, asksaveasfilename
from graphics import *

def is_inside(p, rect):
    '''Purpose: Checks if a point is inside a rectangle
       Parameters: p (Point), rect (Rectangle)
       Return Value: True if inside, False otherwise'''
    p1 = rect.getP1()
    p2 = rect.getP2()
    return p1.getX() <= p.getX() <= p2.getX() and p1.getY() <= p.getY() <= p2.getY()

def apply_grayscale(image, x1, y1, x2, y2):
    '''Purpose: Apply grayscale filter to selected region
       Parameters: image (Image), x1/y1/x2/y2 (int coords)
       Return: None'''
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            r, g, b = image.getPixel(x, y)
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            image.setPixel(x, y, color_rgb(gray, gray, gray))

def apply_negative(image, x1, y1, x2, y2):
    '''Purpose: Apply negative filter to selected region
       Parameters: image (Image), x1/y1/x2/y2 (int coords)
       Return: None'''
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            r, g, b = image.getPixel(x, y)
            image.setPixel(x, y, color_rgb(255 - r, 255 - g, 255 - b))

def main():
    win = GraphWin("Image Editor", 800, 600)
    win.setBackground("lightgray")

    button_labels = ["Load", "Select", "Grayscale", "Negative", "Save", "Quit"]
    buttons = []
    for i, label in enumerate(button_labels):
        btn = Rectangle(Point(10, 10 + i * 50), Point(110, 50 + i * 50))
        btn.setFill("white")
        btn.draw(win)
        txt = Text(btn.getCenter(), label)
        txt.draw(win)
        buttons.append((btn, txt))

    image = None
    image_obj = None
    selected_coords = None
    box_rect = None

    while True:
        click = win.getMouse()
        for btn, txt in buttons:
            if is_inside(click, btn):
                label = txt.getText()

                if label == "Load":
                    if image_obj:
                        image_obj.undraw()
                    file_path = askopenfilename(filetypes=[("PNG files", "*.png")])
                    if file_path:
                        image = Image(Point(400, 300), file_path)
                        image.draw(win)
                        image_obj = image
                        selected_coords = None
                        if box_rect:
                            box_rect.undraw()
                            box_rect = None

                elif label == "Select" and image_obj:
                    pt1 = win.getMouse()
                    pt2 = win.getMouse()

                    x1 = int(min(pt1.getX(), pt2.getX()))
                    y1 = int(min(pt1.getY(), pt2.getY()))
                    x2 = int(max(pt1.getX(), pt2.getX()))
                    y2 = int(max(pt1.getY(), pt2.getY()))
                    selected_coords = (x1, y1, x2, y2)

                    if box_rect:
                        box_rect.undraw()
                    box_rect = Rectangle(Point(x1, y1), Point(x2, y2))
                    box_rect.setOutline("red")
                    box_rect.draw(win)

                elif label == "Grayscale" and image and selected_coords:
                    x1, y1, x2, y2 = selected_coords
                    apply_grayscale(image, x1, y1, x2, y2)

                elif label == "Negative" and image and selected_coords:
                    x1, y1, x2, y2 = selected_coords
                    apply_negative(image, x1, y1, x2, y2)

                elif label == "Save" and image:
                    save_path = asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
                    if save_path:
                        image.save(save_path)

                elif label == "Quit":
                    win.close()
                    return

# Run the program
main()
