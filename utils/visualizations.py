from PIL import Image
import base64
from io import BytesIO

def create_pixel_merchant_icon(color='cyan'):
    """
    Create a pixel art merchant icon.
    
    Args:
        color (str): Color name for the icon ('cyan', 'pink', 'green', 'yellow', 'orange', 'red')
        
    Returns:
        str: Base64 encoded image data URI
    """
    colors = {
        'cyan': (1, 237, 237),
        'pink': (255, 53, 94),
        'green': (80, 252, 0),
        'yellow': (255, 218, 0),
        'orange': (255, 153, 51),
        'red': (255, 0, 0),
    }
    
    rgb_color = colors.get(color, colors['cyan'])
    
    # Create a 16x16 image with transparent background
    img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    pixels = img.load()
    
    # Draw a simple store/shop icon
    # Roof
    for x in range(3, 13):
        pixels[x, 3] = rgb_color
    for x in range(2, 14):
        pixels[x, 4] = rgb_color
    
    # Building
    for y in range(5, 13):
        for x in range(4, 12):
            pixels[x, y] = rgb_color
    
    # Door
    for y in range(9, 13):
        for x in range(6, 10):
            pixels[x, y] = (0, 0, 0, 255)
    
    # Door handle
    pixels[8, 11] = (255, 255, 255, 255)
    
    # Convert to base64 for HTML display
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

def create_pixel_chart(data, color='cyan', height=100, width=200):
    """
    Create a pixelated line chart from data.
    
    Args:
        data (list): List of data points to visualize
        color (str): Color name for the chart ('cyan', 'pink', 'green', 'yellow', 'orange', 'red')
        height (int): Height of the output image
        width (int): Width of the output image
        
    Returns:
        str: Base64 encoded image data URI
    """
    # Create an empty image
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    pixels = img.load()
    
    # Normalize data to fit the height
    max_val = max(data)
    min_val = min(data)
    range_val = max_val - min_val
    
    if range_val == 0:  # Handle flat data
        normalized = [height // 2 for _ in data]
    else:
        normalized = [int((height - 10) * (1 - (val - min_val) / range_val)) + 5 for val in data]
    
    # Get RGB color
    colors = {
        'cyan': (1, 237, 237),
        'pink': (255, 53, 94),
        'green': (80, 252, 0),
        'yellow': (255, 218, 0),
        'orange': (255, 153, 51),
        'red': (255, 0, 0),
    }
    
    rgb_color = colors.get(color, colors['cyan'])
    
    # Draw the line
    step = width / (len(data) - 1) if len(data) > 1 else width
    
    for i in range(len(data) - 1):
        x1, y1 = int(i * step), normalized[i]
        x2, y2 = int((i + 1) * step), normalized[i + 1]
        
        # Draw a thick pixel line
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        while x1 != x2 or y1 != y2:
            # Draw a 2x2 pixel at this point
            for ox in range(2):
                for oy in range(2):
                    if 0 <= x1+ox < width and 0 <= y1+oy < height:
                        pixels[x1+ox, y1+oy] = rgb_color
            
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
                
        # Draw the endpoint
        for ox in range(2):
            for oy in range(2):
                if 0 <= x2+ox < width and 0 <= y2+oy < height:
                    pixels[x2+ox, y2+oy] = rgb_color
    
    # Convert to base64 for HTML display
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

def apply_retro_styling():
    """
    Returns CSS styling for retro gaming aesthetic.
    
    Returns:
        str: CSS styling for Streamlit
    """
    return """
    <style>
    /* Main theme colors */
    :root {
        --primary: #FF355E;        /* Hot pink */
        --secondary: #01EDED;      /* Cyan */
        --tertiary: #50FC00;       /* Bright green */
        --dark: #120458;           /* Dark blue */
        --light: #F5F5F5;          /* White-ish */
        --warning: #FF9933;        /* Orange */
        --danger: #FF0000;         /* Red */
        --background: #FFDD00;     /* Bright yellow */
    }
    
    /* Fonts */
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono&display=swap');
    
    /* Base styles */
    .main {
        background-color: var(--background);
        color: var(--dark);
    }
    
    /* Override Streamlit's default background */
    .stApp {
        background-color: var(--background);
    }
    
    h1, h2, h3 {
        font-family: 'Press Start 2P', cursive;
        text-transform: uppercase;
        color: var(--secondary);
        text-shadow: 3px 3px 0 var(--dark);
        margin: 1.5rem 0;
    }
    
    h1 {
        color: var(--primary);
        font-size: 2.5rem;
        letter-spacing: 2px;
        text-align: center;
        padding: 20px 0;
        border-bottom: 4px solid var(--primary);
        margin-bottom: 30px;
    }
    
    .stDataFrame {
        border: 4px solid var(--secondary);
        box-shadow: 8px 8px 0 var(--dark);
    }
    
    /* Metric cards */
    .metric-card {
        background-color: var(--dark);
        border: 3px solid var(--secondary);
        border-radius: 0;
        padding: 10px;
        text-align: center;
        margin: 5px;
        box-shadow: 5px 5px 0 rgba(0,0,0,0.5);
        transition: all 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 7px 7px 0 rgba(0,0,0,0.5);
    }
    
    .metric-value {
        font-family: 'Press Start 2P', cursive;
        font-size: 2rem;
        margin: 10px 0;
    }
    
    .metric-label {
        font-family: 'VT323', monospace;
        font-size: 1.3rem;
        color: var(--light);
    }
    
    /* Risk levels */
    .high-risk {
        color: var(--danger);
        font-weight: bold;
    }
    
    .medium-risk {
        color: var(--warning);
        font-weight: bold;
    }
    
    .low-risk {
        color: var(--tertiary);
        font-weight: bold;
    }
    
    /* Button styles */
    .stButton button {
        font-family: 'Press Start 2P', cursive;
        background-color: var(--secondary);
        color: var(--dark);
        border: 3px solid var(--dark);
        border-radius: 0;
        box-shadow: 5px 5px 0 rgba(0,0,0,0.5);
        transition: all 0.2s;
        text-transform: uppercase;
        padding: 10px 20px;
        margin: 10px 0;
    }
    
    .stButton button:hover {
        background-color: var(--primary);
        color: white;
        transform: translateY(-2px);
        box-shadow: 7px 7px 0 rgba(0,0,0,0.5);
    }
    
    /* Select box styling */
    .stSelectbox div[data-baseweb="select"] > div {
        font-family: 'VT323', monospace;
        background-color: var(--dark);
        border: 3px solid var(--secondary);
        border-radius: 0;
        color: white;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: var(--dark);
        border-right: 4px solid var(--secondary);
    }
    
    [data-testid="stSidebar"] {
        background-color: var(--dark);
    }
    
    .sidebar h2 {
        font-size: 1.5rem;
        color: var(--primary);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Press Start 2P', cursive;
        font-size: 0.8rem;
        background-color: var(--dark);
        border: 2px solid var(--secondary);
        border-radius: 0;
        color: var(--light);
        padding: 10px;
        box-shadow: 3px 3px 0 rgba(0,0,0,0.5);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--secondary);
        color: var(--dark);
    }
    
    /* Dataframe styling */
    .dataframe {
        font-family: 'Space Mono', monospace;
    }
    
    /* Footer */
    .footer {
        font-family: 'VT323', monospace;
        text-align: center;
        color: var(--dark);
        padding: 20px 0;
        border-top: 2px solid var(--primary);
        margin-top: 50px;
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background-color: var(--primary);
    }
    
    /* Arcade marquee effect */
    .marquee {
        background-color: var(--dark);
        overflow: hidden;
        position: relative;
        border: 3px solid var(--primary);
        box-shadow: 0 0 10px var(--primary);
        margin: 20px 0;
        padding: 10px;
    }
    
    .marquee-content {
        font-family: 'Press Start 2P', cursive;
        font-size: 1.2rem;
        color: var(--primary);
        white-space: nowrap;
        animation: marquee 15s linear infinite;
    }
    
    @keyframes marquee {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    
    /* High-score table style */
    .high-score {
        font-family: 'VT323', monospace;
        font-size: 1.2rem;
        margin-bottom: 10px;
    }
    
    .high-score-name {
        color: var(--secondary);
        display: inline-block;
        width: 70%;
    }
    
    .high-score-value {
        color: var(--tertiary);
        display: inline-block;
        width: 30%;
        text-align: right;
    }
    </style>
    """