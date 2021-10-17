from flask import Flask, request, jsonify

from PIL import Image, ImageDraw


app = Flask(__name__)

@app.route("/")
def hello_world():
    return \
    """
    <p>Hello, world!</p>
    <img src="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png"/>
    <img src="/static/myimg.png"/>
    """


@app.route('/test/image', methods=['POST'])
def request_image():
    print("request")
    json = request.get_json()
    width = int(json.get('width'))
    height = int(json.get('height'))
    transform_window = Window2D(int(json.get('min_x')), int(json.get('max_x')),
        int(json.get('min_y')), int(json.get('max_y')))
    
    image_render_request(width, height, transform_window)
    return jsonify(None)

# window_map = Window2D(-2, 0.5, -1.15, 1.15)
def image_render_request(pixel_width, pixel_height, cartesian_window):
    
    img = Image.new('RGB', (pixel_width, pixel_height), color='black')
    pixels = img.load()
    print(img.size)
    print(img.size[0])
    for row in range(img.size[1]-1):
        for col in range(img.size[0]-1):
            (x, y) = pixel_to_cartesian(col, row, cartesian_window, pixel_width, pixel_height)
            value = fast_converge(x, y)
            pixels[col, row] = (80, value*2, value*2)
    
    img.save('static/myimg.png')

class Window2D:
    def __init__(self, min_x, max_x, min_y, max_y):
        if min_x >= max_x or min_y >= max_y:
            raise IndexError("Window must have a size, and minimums must be less than maximums.")
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.width = max_x - min_x
        self.height = max_y - min_y

def pixel_to_cartesian(px, py, window, pixel_width, pixel_height):
    scale_x = window.width/pixel_width
    scale_y = window.height/pixel_height
    # x = window.min_x + px*window.width
    # y = window.min_y + py*window.height
    # scale_x = 1
    # scale_y = 1
    x = px*scale_x + window.min_x #- pixel_width/2
    y = -py*scale_y - window.min_y
    return (x, y)

def test_plot():
    pixel_width = 800
    pixel_height = 400
    img = Image.new('RGB', (pixel_width, pixel_height), color='black')
    pixels = img.load()
    window_map = Window2D(-2.5, 1, -2, 2)
    print(img.size)
    print(img.size[0])
    for row in range(img.size[1]-1):
        for col in range(img.size[0]-1):
            if pixel_to_cartesian(col, row, window_map, pixel_width, pixel_height)[0] <= 0:
                pixels[col, row] = (255, 0, 0)
            if pixel_to_cartesian(col, row, window_map, pixel_width, pixel_height)[1] >= 0:
                pixels[col, row] = (0, 0, 255)
    
    img.save('static/myimg.png')

def fast_converge(x0, y0):
    i = 0
    max_iter = 100
    x = x0
    y = y0
    while (x*x + y*y <= 2*2 and i < max_iter):
        x_temp = x*x - y*y + x0
        y = 2*x*y + y0
        x = x_temp
        i += 1

    return max_iter - i

def test2():
    pixel_width = 940
    pixel_height = 540
    img = Image.new('RGB', (pixel_width, pixel_height), color='black')
    pixels = img.load()
    window_map = Window2D(-2, 0.5, -1.15, 1.15)
    print(img.size)
    print(img.size[0])
    for row in range(img.size[1]-1):
        for col in range(img.size[0]-1):
            (x, y) = pixel_to_cartesian(col, row, window_map, pixel_width, pixel_height)
            value = fast_converge(x, y)
            pixels[col, row] = (80, value*2, value*2)
    
    img.save('static/myimg.png')