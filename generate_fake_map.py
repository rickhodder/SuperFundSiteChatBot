"""
Generate a fake map image for demo purposes.
Shows a green dot (policy location) and red dots (SuperFund sites).
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Create image
width, height = 800, 600
img = Image.new('RGB', (width, height), color='#E8F4F8')  # Light blue background

draw = ImageDraw.Draw(img)

# Draw grid lines to simulate map
grid_color = '#D0E8F0'
for x in range(0, width, 50):
    draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
for y in range(0, height, 50):
    draw.line([(0, y), (width, y)], fill=grid_color, width=1)

# Draw "roads"
road_color = '#FFFFFF'
draw.line([(100, 0), (100, height)], fill=road_color, width=3)
draw.line([(0, 200), (width, 200)], fill=road_color, width=3)
draw.line([(400, 0), (400, height)], fill=road_color, width=4)
draw.line([(0, 400), (width, 400)], fill=road_color, width=4)

# Policy location (green dot) - center
policy_x, policy_y = 400, 300
draw.ellipse([policy_x-15, policy_y-15, policy_x+15, policy_y+15], 
             fill='#00FF00', outline='#006600', width=3)

# SuperFund sites (red dots) - around the policy
sites = [
    (250, 200),  # Northwest
    (550, 250),  # Northeast
    (350, 450),  # South
]

for site_x, site_y in sites:
    draw.ellipse([site_x-12, site_y-12, site_x+12, site_y+12], 
                 fill='#FF0000', outline='#880000', width=2)
    # Draw radius circle around site
    draw.ellipse([site_x-40, site_y-40, site_x+40, site_y+40], 
                 outline='#FF0000', width=1)

# Draw 50-mile radius circle around policy
radius = 150
draw.ellipse([policy_x-radius, policy_y-radius, policy_x+radius, policy_y+radius], 
             outline='#00AA00', width=2)

# Add labels
try:
    # Try to use a default font, fall back to basic if not available
    try:
        font = ImageFont.truetype("arial.ttf", 14)
        font_small = ImageFont.truetype("arial.ttf", 10)
    except:
        font = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Policy label
    draw.text((policy_x + 20, policy_y - 20), "Policy Location", 
              fill='#006600', font=font)
    
    # Site labels
    draw.text((sites[0][0] + 15, sites[0][1] - 15), "Site 1", 
              fill='#880000', font=font_small)
    draw.text((sites[1][0] + 15, sites[1][1] - 15), "Site 2", 
              fill='#880000', font=font_small)
    draw.text((sites[2][0] + 15, sites[2][1] - 15), "Site 3", 
              fill='#880000', font=font_small)
    
    # Radius label
    draw.text((policy_x + radius - 50, policy_y - 10), "50 mi", 
              fill='#00AA00', font=font_small)
    
    # Legend
    legend_x, legend_y = 20, 20
    draw.rectangle([legend_x-5, legend_y-5, legend_x+180, legend_y+65], 
                   fill='#FFFFFF', outline='#888888', width=2)
    draw.ellipse([legend_x, legend_y, legend_x+12, legend_y+12], 
                 fill='#00FF00', outline='#006600', width=2)
    draw.text((legend_x + 20, legend_y - 2), "Policy Location", 
              fill='#000000', font=font_small)
    
    draw.ellipse([legend_x, legend_y+25, legend_x+12, legend_y+37], 
                 fill='#FF0000', outline='#880000', width=2)
    draw.text((legend_x + 20, legend_y + 23), "SuperFund Site", 
              fill='#000000', font=font_small)
    
    draw.line([(legend_x, legend_y+55), (legend_x+30, legend_y+55)], 
              fill='#00AA00', width=2)
    draw.text((legend_x + 35, legend_y + 48), "50-mile radius", 
              fill='#000000', font=font_small)

except Exception as e:
    print(f"Note: Could not add text labels: {e}")

# Save image
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "demo_map.png")
img.save(output_path)
print(f"✓ Generated fake map image: {output_path}")
print(f"  - Image size: {width}x{height}")
print(f"  - Green dot: Policy location")
print(f"  - Red dots: 3 SuperFund sites")
print(f"  - Green circle: 50-mile radius")
