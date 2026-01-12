"""
Create database UI screenshot mockups for validation results
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_db_screenshot(title, data, filename, show_success=True):
    """Create a mockup screenshot of database query results"""
    
    # Image dimensions
    width = 1200
    row_height = 35
    header_height = 50
    title_height = 40
    margin = 20
    
    # Calculate height based on rows
    num_rows = len(data)
    height = title_height + header_height + (num_rows * row_height) + (margin * 2)
    
    # Create image with white background
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Colors
    title_bg = (45, 55, 72)  # Dark gray for title bar
    header_bg = (66, 153, 225)  # Blue for header
    success_bg = (72, 187, 120)  # Green for success rows
    warning_bg = (245, 158, 11)  # Orange for warning rows
    text_color = (45, 55, 72)
    white = (255, 255, 255)
    border_color = (203, 213, 224)
    
    # Try to use a font, fall back to default if not available
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        header_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
        cell_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    except:
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        cell_font = ImageFont.load_default()
    
    # Draw title bar
    draw.rectangle([0, 0, width, title_height], fill=title_bg)
    draw.text((margin, 10), title, fill=white, font=title_font)
    
    # Get column widths
    if data and len(data) > 0:
        num_cols = len(data[0])
        col_width = (width - (margin * 2)) // num_cols
        
        # Draw header
        y_pos = title_height
        draw.rectangle([margin, y_pos, width - margin, y_pos + header_height], fill=header_bg)
        
        for i, header in enumerate(data[0].keys()):
            x_pos = margin + (i * col_width)
            draw.text((x_pos + 10, y_pos + 15), str(header).upper(), fill=white, font=header_font)
        
        # Draw rows
        y_pos += header_height
        for row_idx, row in enumerate(data):
            # Determine row color
            if show_success:
                row_bg = success_bg if row_idx % 2 == 0 else (236, 253, 245)  # Alternating green shades
            else:
                row_bg = warning_bg if row_idx % 2 == 0 else (254, 243, 199)  # Alternating orange shades
            
            draw.rectangle([margin, y_pos, width - margin, y_pos + row_height], fill=row_bg)
            
            for col_idx, (key, value) in enumerate(row.items()):
                x_pos = margin + (col_idx * col_width)
                draw.text((x_pos + 10, y_pos + 10), str(value), fill=text_color, font=cell_font)
            
            # Draw horizontal line
            draw.line([margin, y_pos + row_height, width - margin, y_pos + row_height], fill=border_color, width=1)
            y_pos += row_height
        
        # Draw vertical lines
        for i in range(num_cols + 1):
            x_pos = margin + (i * col_width)
            draw.line([x_pos, title_height, x_pos, y_pos], fill=border_color, width=1)
    
    # Save image
    img.save(filename)
    print(f"✓ Created: {filename}")

def create_all_screenshots():
    """Create all database screenshot mockups"""
    
    os.makedirs('screenshots', exist_ok=True)
    
    # 1. Perfect Match - No Discrepancies
    print("\n1. Creating perfect match screenshot...")
    perfect_data = [
        {'validation_type': 'SOURCE_MINUS_TARGET', 'record_count': '0'},
        {'validation_type': 'TARGET_MINUS_SOURCE', 'record_count': '0'}
    ]
    create_db_screenshot(
        'PostgreSQL Query Result - Perfect Match ✓',
        perfect_data,
        'screenshots/01_perfect_match.png',
        show_success=True
    )
    
    # 2. Source Missing Records
    print("2. Creating source missing records screenshot...")
    source_missing = [
        {'validation_type': 'SOURCE_MINUS_TARGET', 'record_count': '0'},
        {'validation_type': 'TARGET_MINUS_SOURCE', 'record_count': '5'},
        {'validation_type': 'DETAIL', 'record_count': 'NULL'}
    ]
    create_db_screenshot(
        'PostgreSQL Query Result - Target Has Extra Records',
        source_missing,
        'screenshots/02_target_extra_records.png',
        show_success=False
    )
    
    # 3. Target Missing Records
    print("3. Creating target missing records screenshot...")
    target_missing = [
        {'validation_type': 'SOURCE_MINUS_TARGET', 'record_count': '12'},
        {'validation_type': 'TARGET_MINUS_SOURCE', 'record_count': '0'},
        {'validation_type': 'DETAIL', 'record_count': 'NULL'}
    ]
    create_db_screenshot(
        'PostgreSQL Query Result - Source Has Extra Records',
        target_missing,
        'screenshots/03_source_extra_records.png',
        show_success=False
    )
    
    # 4. Detailed Discrepancy View - Sample Records
    print("4. Creating detailed discrepancy view...")
    discrepancy_details = [
        {'order_key': '10001', 'customer_key': 'C001', 'order_date': '2024-01-15', 'total_amount': '150.00', 'status': 'NEW'},
        {'order_key': '10005', 'customer_key': 'C012', 'order_date': '2024-01-16', 'total_amount': '275.50', 'status': 'PROCESSING'},
        {'order_key': '10008', 'customer_key': 'C008', 'order_date': '2024-01-17', 'total_amount': '89.99', 'status': 'COMPLETED'}
    ]
    create_db_screenshot(
        'PostgreSQL Query Result - Detailed Discrepancy Records (First 3 of 12)',
        discrepancy_details,
        'screenshots/04_discrepancy_details.png',
        show_success=False
    )
    
    # 5. DBeaver Interface Mockup
    print("5. Creating DBeaver interface mockup...")
    
    # Create wider image for DBeaver
    width = 1400
    height = 400
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # DBeaver colors
    toolbar_bg = (240, 240, 240)
    border_color = (180, 180, 180)
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
        font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
    except:
        font = ImageFont.load_default()
        font_bold = ImageFont.load_default()
    
    # Draw toolbar
    draw.rectangle([0, 0, width, 40], fill=toolbar_bg)
    draw.text((10, 12), "📊 DBeaver - SQL Editor", fill=(60, 60, 60), font=font_bold)
    
    # Draw SQL text area
    draw.rectangle([5, 45, width-5, 150], fill=(250, 250, 250), outline=border_color, width=1)
    sql_text = "SELECT * FROM source_transformed\nEXCEPT\nSELECT * FROM target_data;"
    draw.text((15, 55), sql_text, fill=(0, 0, 100), font=font)
    
    # Draw execute button
    draw.rectangle([10, 160, 120, 190], fill=(76, 175, 80), outline=border_color, width=1)
    draw.text((30, 168), "▶ Execute", fill=(255, 255, 255), font=font_bold)
    
    # Draw results label
    draw.text((10, 200), "Query Results (3 rows)", fill=(60, 60, 60), font=font_bold)
    
    # Draw results table
    table_y = 230
    col_width = 270
    draw.rectangle([5, table_y, width-5, table_y + 150], outline=border_color, width=2)
    
    # Headers
    headers = ['order_key', 'order_timestamp', 'customer_key', 'product_name', 'total_amount']
    for i, header in enumerate(headers):
        x = 10 + (i * col_width)
        draw.rectangle([x, table_y, x + col_width, table_y + 30], fill=(230, 230, 230))
        draw.text((x + 5, table_y + 8), header, fill=(0, 0, 0), font=font_bold)
    
    img.save('screenshots/05_dbeaver_interface.png')
    print("✓ Created: screenshots/05_dbeaver_interface.png")
    
    # 6. SQL Server Management Studio Style
    print("6. Creating SSMS interface mockup...")
    width = 1400
    height = 350
    img = Image.new('RGB', (width, height), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    
    # SSMS colors
    title_bg = (0, 122, 204)
    grid_bg = (255, 255, 255)
    
    # Title bar
    draw.rectangle([0, 0, width, 35], fill=title_bg)
    draw.text((10, 8), "Microsoft SQL Server Management Studio - Query Results", fill=(255, 255, 255), font=font_bold)
    
    # Status bar
    draw.rectangle([5, 45, width-5, 75], fill=(255, 255, 230))
    draw.text((10, 52), "✓ Query executed successfully. Rows affected: 0", fill=(0, 100, 0), font=font)
    
    # Results grid
    draw.rectangle([5, 85, width-5, 320], fill=grid_bg, outline=(180, 180, 180), width=2)
    
    # Perfect match message
    draw.text((width//2 - 150, 150), "✓ VALIDATION PASSED", fill=(0, 150, 0), font=font_bold)
    draw.text((width//2 - 180, 180), "No discrepancies found between source and target", fill=(60, 60, 60), font=font)
    draw.text((width//2 - 120, 210), "All records match perfectly!", fill=(60, 60, 60), font=font)
    
    img.save('screenshots/06_ssms_success.png')
    print("✓ Created: screenshots/06_ssms_success.png")
    
    print("\n✅ All screenshots created successfully!")
    print(f"📁 Saved in: screenshots/")

if __name__ == '__main__':
    create_all_screenshots()
