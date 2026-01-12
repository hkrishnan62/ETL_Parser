"""
Create highly realistic database tool screenshots that match actual UI/UX
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

def get_fonts():
    """Get fonts with fallbacks"""
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        bold_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 11)
        mono_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 10)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
    except:
        title_font = bold_font = mono_font = small_font = ImageFont.load_default()
    return title_font, bold_font, mono_font, small_font

def create_ssms_perfect_match():
    """Create realistic SSMS screenshot showing perfect validation match"""
    width, height = 1400, 800
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    title_font, bold_font, mono_font, small_font = get_fonts()
    
    # SSMS Title Bar (Blue)
    draw.rectangle([0, 0, width, 30], fill=(0, 120, 215))
    draw.text((10, 8), "SQLQuery1.sql - localhost.ETL_DB (LAPTOP\\SQLEXPRESS (51))", fill=(255, 255, 255), font=bold_font)
    
    # Menu Bar
    draw.rectangle([0, 30, width, 52], fill=(246, 246, 246))
    menus = ["File", "Edit", "View", "Query", "Tools", "Window", "Help"]
    x_pos = 10
    for menu in menus:
        draw.text((x_pos, 36), menu, fill=(0, 0, 0), font=title_font)
        x_pos += 60
    
    # Toolbar
    draw.rectangle([0, 52, width, 82], fill=(240, 240, 240))
    draw.rectangle([0, 82, width, 83], fill=(160, 160, 160))
    # Execute button (green)
    draw.rectangle([10, 57, 75, 77], fill=(0, 122, 51), outline=(0, 100, 40), width=1)
    draw.text((20, 61), "▶ Execute", fill=(255, 255, 255), font=bold_font)
    
    # Status indicators
    draw.text((90, 61), "Parse  Check  Comment", fill=(80, 80, 80), font=small_font)
    
    # SQL Query Area
    draw.rectangle([5, 90, width-5, 340], fill=(255, 255, 255), outline=(200, 200, 200), width=1)
    
    sql_query = """-- ETL Validation Query - Source MINUS Target
WITH source_transformed AS (
  SELECT
    source_table.order_id AS order_key,
    source_table.customer_id AS customer_key,
    TO_TIMESTAMP(source_table.order_date, 'YYYY-MM-DD') AS order_timestamp,
    source_table.quantity AS quantity,
    CAST(source_table.unit_price AS DECIMAL(10,2)) AS unit_price_decimal
  FROM source_table
),
target_data AS (
  SELECT * FROM orders_fact
)
SELECT 'SOURCE_MINUS_TARGET' AS validation_type, COUNT(*) AS record_count
FROM (SELECT * FROM source_transformed EXCEPT SELECT * FROM target_data) diff;"""
    
    y_pos = 100
    for line in sql_query.split('\n'):
        if line.strip().startswith('--'):
            draw.text((15, y_pos), line, fill=(0, 128, 0), font=mono_font)
        elif any(kw in line.upper() for kw in ['SELECT', 'FROM', 'WHERE', 'WITH', 'AS']):
            draw.text((15, y_pos), line, fill=(0, 0, 255), font=mono_font)
        else:
            draw.text((15, y_pos), line, fill=(0, 0, 0), font=mono_font)
        y_pos += 15
        if y_pos > 325:
            break
    
    # Results Tab Bar
    draw.rectangle([5, 350, width-5, 375], fill=(246, 246, 246), outline=(200, 200, 200), width=1)
    draw.rectangle([10, 355, 100, 375], fill=(255, 255, 255))
    draw.text((20, 358), "Results", fill=(0, 0, 0), font=bold_font)
    draw.text((110, 358), "Messages", fill=(100, 100, 100), font=title_font)
    
    # Results Grid Header
    draw.rectangle([5, 375, width-5, 405], fill=(235, 235, 235), outline=(200, 200, 200), width=1)
    draw.text((15, 383), "validation_type", fill=(0, 0, 0), font=bold_font)
    draw.text((400, 383), "record_count", fill=(0, 0, 0), font=bold_font)
    
    # Results Grid Rows - PERFECT MATCH (Green highlight)
    draw.rectangle([5, 405, width-5, 435], fill=(220, 255, 220), outline=(200, 200, 200), width=1)
    draw.text((15, 413), "SOURCE_MINUS_TARGET", fill=(0, 0, 0), font=mono_font)
    draw.text((400, 413), "0", fill=(0, 128, 0), font=bold_font)
    
    draw.rectangle([5, 435, width-5, 465], fill=(235, 250, 235), outline=(200, 200, 200), width=1)
    draw.text((15, 443), "TARGET_MINUS_SOURCE", fill=(0, 0, 0), font=mono_font)
    draw.text((400, 443), "0", fill=(0, 128, 0), font=bold_font)
    
    # Status Bar
    draw.rectangle([0, height-30, width, height], fill=(0, 120, 215))
    draw.text((10, height-22), "✓ Query executed successfully.", fill=(255, 255, 255), font=title_font)
    draw.text((300, height-22), "(2 rows affected)", fill=(255, 255, 255), font=title_font)
    draw.text((500, height-22), "Execution time: 00:00:01", fill=(255, 255, 255), font=small_font)
    draw.text((width-200, height-22), "localhost.ETL_DB", fill=(255, 255, 255), font=small_font)
    
    img.save('screenshots/01_SSMS_Perfect_Match.png')
    print("✓ Created: 01_SSMS_Perfect_Match.png")

def create_ssms_source_extra():
    """Create realistic SSMS screenshot showing source has extra records"""
    width, height = 1400, 800
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    title_font, bold_font, mono_font, small_font = get_fonts()
    
    # SSMS Title Bar
    draw.rectangle([0, 0, width, 30], fill=(0, 120, 215))
    draw.text((10, 8), "SQLQuery2.sql - localhost.ETL_DB (LAPTOP\\SQLEXPRESS (51))", fill=(255, 255, 255), font=bold_font)
    
    # Menu Bar
    draw.rectangle([0, 30, width, 52], fill=(246, 246, 246))
    
    # Toolbar
    draw.rectangle([0, 52, width, 82], fill=(240, 240, 240))
    draw.rectangle([0, 82, width, 83], fill=(160, 160, 160))
    draw.rectangle([10, 57, 75, 77], fill=(0, 122, 51), outline=(0, 100, 40), width=1)
    draw.text((20, 61), "▶ Execute", fill=(255, 255, 255), font=bold_font)
    
    # SQL Query Area
    draw.rectangle([5, 90, width-5, 300], fill=(255, 255, 255), outline=(200, 200, 200), width=1)
    draw.text((15, 100), "-- Validation Result: SOURCE HAS EXTRA RECORDS", fill=(255, 100, 0), font=bold_font)
    draw.text((15, 120), "-- 12 records exist in source but not in target", fill=(255, 100, 0), font=mono_font)
    
    # Results Tab Bar
    draw.rectangle([5, 310, width-5, 335], fill=(246, 246, 246), outline=(200, 200, 200), width=1)
    draw.rectangle([10, 315, 100, 335], fill=(255, 255, 255))
    draw.text((20, 318), "Results", fill=(0, 0, 0), font=bold_font)
    
    # Results Grid Header
    draw.rectangle([5, 335, width-5, 365], fill=(235, 235, 235), outline=(200, 200, 200), width=1)
    draw.text((15, 343), "validation_type", fill=(0, 0, 0), font=bold_font)
    draw.text((400, 343), "record_count", fill=(0, 0, 0), font=bold_font)
    
    # Results - SOURCE HAS EXTRA (Red/Orange highlight)
    draw.rectangle([5, 365, width-5, 395], fill=(255, 235, 220), outline=(200, 200, 200), width=1)
    draw.text((15, 373), "SOURCE_MINUS_TARGET", fill=(0, 0, 0), font=mono_font)
    draw.text((400, 373), "12", fill=(180, 0, 0), font=bold_font)
    
    draw.rectangle([5, 395, width-5, 425], fill=(220, 255, 220), outline=(200, 200, 200), width=1)
    draw.text((15, 403), "TARGET_MINUS_SOURCE", fill=(0, 0, 0), font=mono_font)
    draw.text((400, 403), "0", fill=(0, 128, 0), font=mono_font)
    
    draw.rectangle([5, 425, width-5, 455], fill=(245, 245, 245), outline=(200, 200, 200), width=1)
    draw.text((15, 433), "DETAIL", fill=(0, 0, 0), font=mono_font)
    draw.text((400, 433), "NULL", fill=(128, 128, 128), font=mono_font)
    
    # Warning Box
    draw.rectangle([10, 470, width-10, 520], fill=(255, 243, 205), outline=(255, 152, 0), width=2)
    draw.text((20, 480), "⚠ DATA QUALITY ISSUE DETECTED", fill=(180, 60, 0), font=bold_font)
    draw.text((20, 500), "12 records in source table were not successfully loaded into target table.", fill=(100, 40, 0), font=title_font)
    
    # Status Bar
    draw.rectangle([0, height-30, width, height], fill=(0, 120, 215))
    draw.text((10, height-22), "✓ Query executed successfully.", fill=(255, 255, 255), font=title_font)
    draw.text((300, height-22), "(3 rows affected)", fill=(255, 255, 255), font=title_font)
    
    img.save('screenshots/02_SSMS_Source_Extra_Records.png')
    print("✓ Created: 02_SSMS_Source_Extra_Records.png")

def create_dbeaver_perfect_match():
    """Create realistic DBeaver screenshot"""
    width, height = 1400, 850
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    title_font, bold_font, mono_font, small_font = get_fonts()
    
    # DBeaver Title Bar (Dark)
    draw.rectangle([0, 0, width, 35], fill=(60, 60, 60))
    draw.text((15, 10), "DBeaver 23.2.0 - SQL Editor - ETL_DB@PostgreSQL - localhost:5432", fill=(255, 255, 255), font=bold_font)
    
    # Toolbar
    draw.rectangle([0, 35, width, 70], fill=(245, 245, 245))
    draw.line([0, 70, width, 70], fill=(180, 180, 180), width=1)
    
    # Execute button (Orange)
    draw.rectangle([10, 42, 90, 63], fill=(242, 153, 74), outline=(200, 120, 50), width=1)
    draw.text((20, 47), "▶ Execute", fill=(255, 255, 255), font=bold_font)
    
    # Other toolbar buttons
    draw.rectangle([100, 42, 150, 63], fill=(230, 230, 230), outline=(180, 180, 180), width=1)
    draw.text((108, 47), "⟲ Fetch", fill=(60, 60, 60), font=small_font)
    
    draw.rectangle([160, 42, 210, 63], fill=(230, 230, 230), outline=(180, 180, 180), width=1)
    draw.text((168, 47), "💾 Save", fill=(60, 60, 60), font=small_font)
    
    # SQL Editor Area
    draw.rectangle([5, 75, width-5, 350], fill=(250, 250, 250), outline=(200, 200, 200), width=1)
    
    # Line numbers
    draw.rectangle([5, 75, 40, 350], fill=(240, 240, 240))
    for i in range(1, 16):
        draw.text((12, 75 + i*17), str(i), fill=(150, 150, 150), font=small_font)
    
    sql_lines = [
        "-- PostgreSQL ETL Validation Query",
        "WITH source_transformed AS (",
        "  SELECT",
        "    source_table.order_id AS order_key,",
        "    source_table.customer_id AS customer_key,",
        "    source_table.quantity,",
        "    CAST(source_table.unit_price AS DECIMAL(10,2)) AS unit_price",
        "  FROM source_table",
        "),",
        "target_data AS (",
        "  SELECT * FROM orders_fact",
        ")",
        "SELECT 'SOURCE_MINUS_TARGET' AS validation_type,",
        "       COUNT(*) AS record_count",
        "FROM (SELECT * FROM source_transformed"
    ]
    
    y_pos = 85
    for line in sql_lines:
        if '--' in line:
            draw.text((45, y_pos), line, fill=(0, 128, 0), font=mono_font)
        elif any(k in line for k in ['SELECT', 'FROM', 'WITH', 'AS']):
            draw.text((45, y_pos), line, fill=(0, 0, 200), font=mono_font)
        else:
            draw.text((45, y_pos), line, fill=(0, 0, 0), font=mono_font)
        y_pos += 17
    
    # Results Tabs
    draw.rectangle([5, 355, width-5, 385], fill=(230, 230, 230))
    draw.rectangle([10, 360, 100, 385], fill=(255, 255, 255))
    draw.text((20, 365), "Data", fill=(0, 0, 0), font=bold_font)
    draw.text((110, 365), "Output", fill=(100, 100, 100), font=title_font)
    draw.text((180, 365), "Execution Log", fill=(100, 100, 100), font=title_font)
    
    # Results Grid
    draw.rectangle([5, 385, width-5, 420], fill=(70, 130, 180), outline=(50, 100, 150), width=1)
    draw.text((15, 395), "validation_type", fill=(255, 255, 255), font=bold_font)
    draw.text((450, 395), "record_count", fill=(255, 255, 255), font=bold_font)
    
    # Data rows with alternating colors
    draw.rectangle([5, 420, width-5, 455], fill=(245, 250, 255))
    draw.text((15, 430), "SOURCE_MINUS_TARGET", fill=(0, 0, 0), font=mono_font)
    draw.text((450, 430), "0", fill=(0, 150, 0), font=bold_font)
    
    draw.rectangle([5, 455, width-5, 490], fill=(255, 255, 255))
    draw.text((15, 465), "TARGET_MINUS_SOURCE", fill=(0, 0, 0), font=mono_font)
    draw.text((450, 465), "0", fill=(0, 150, 0), font=bold_font)
    
    # Success message box
    draw.rectangle([10, 510, width-10, 560], fill=(212, 237, 218), outline=(40, 167, 69), width=2)
    draw.text((20, 520), "✓ VALIDATION SUCCESSFUL", fill=(21, 87, 36), font=bold_font)
    draw.text((20, 540), "All source records successfully matched in target. No discrepancies found.", fill=(21, 87, 36), font=title_font)
    
    # Status Bar
    draw.rectangle([0, height-30, width, height], fill=(245, 245, 245))
    draw.line([0, height-30, width, height-30], fill=(180, 180, 180), width=1)
    draw.text((10, height-20), "✓ Query executed in 847 ms", fill=(0, 128, 0), font=small_font)
    draw.text((300, height-20), "2 rows fetched", fill=(80, 80, 80), font=small_font)
    draw.text((width-250, height-20), "PostgreSQL 14.5 | ETL_DB | postgres", fill=(100, 100, 100), font=small_font)
    
    img.save('screenshots/03_DBeaver_Perfect_Match.png')
    print("✓ Created: 03_DBeaver_Perfect_Match.png")

def create_dbeaver_target_extra():
    """Create DBeaver screenshot showing target has extra records"""
    width, height = 1400, 850
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    title_font, bold_font, mono_font, small_font = get_fonts()
    
    # DBeaver Title Bar
    draw.rectangle([0, 0, width, 35], fill=(60, 60, 60))
    draw.text((15, 10), "DBeaver 23.2.0 - SQL Editor - ETL_DB@PostgreSQL - localhost:5432", fill=(255, 255, 255), font=bold_font)
    
    # Toolbar
    draw.rectangle([0, 35, width, 70], fill=(245, 245, 245))
    draw.line([0, 70, width, 70], fill=(180, 180, 180), width=1)
    draw.rectangle([10, 42, 90, 63], fill=(242, 153, 74), outline=(200, 120, 50), width=1)
    draw.text((20, 47), "▶ Execute", fill=(255, 255, 255), font=bold_font)
    
    # SQL Editor
    draw.rectangle([5, 75, width-5, 300], fill=(250, 250, 250), outline=(200, 200, 200), width=1)
    draw.rectangle([5, 75, 40, 300], fill=(240, 240, 240))
    
    draw.text((45, 85), "-- TARGET HAS EXTRA RECORDS VALIDATION", fill=(255, 100, 0), font=bold_font)
    
    # Results
    draw.rectangle([5, 310, width-5, 340], fill=(230, 230, 230))
    draw.rectangle([10, 315, 100, 340], fill=(255, 255, 255))
    draw.text((20, 320), "Data", fill=(0, 0, 0), font=bold_font)
    
    # Grid Header
    draw.rectangle([5, 340, width-5, 375], fill=(70, 130, 180))
    draw.text((15, 350), "validation_type", fill=(255, 255, 255), font=bold_font)
    draw.text((450, 350), "record_count", fill=(255, 255, 255), font=bold_font)
    
    # Data - TARGET HAS EXTRA
    draw.rectangle([5, 375, width-5, 410], fill=(245, 250, 255))
    draw.text((15, 385), "SOURCE_MINUS_TARGET", fill=(0, 0, 0), font=mono_font)
    draw.text((450, 385), "0", fill=(0, 128, 0), font=mono_font)
    
    draw.rectangle([5, 410, width-5, 445], fill=(255, 243, 224))
    draw.text((15, 420), "TARGET_MINUS_SOURCE", fill=(0, 0, 0), font=mono_font)
    draw.text((450, 420), "5", fill=(204, 85, 0), font=bold_font)
    
    draw.rectangle([5, 445, width-5, 480], fill=(245, 250, 255))
    draw.text((15, 455), "DETAIL", fill=(0, 0, 0), font=mono_font)
    draw.text((450, 455), "NULL", fill=(128, 128, 128), font=mono_font)
    
    # Warning box
    draw.rectangle([10, 500, width-10, 560], fill=(255, 243, 205), outline=(255, 152, 0), width=2)
    draw.text((20, 510), "⚠ DATA DISCREPANCY DETECTED", fill=(138, 77, 0), font=bold_font)
    draw.text((20, 530), "Target table contains 5 records that do not exist in source after transformation.", fill=(102, 60, 0), font=title_font)
    draw.text((20, 545), "Possible causes: Duplicate ETL loads, manual inserts, or data from other sources.", fill=(102, 60, 0), font=small_font)
    
    # Status Bar
    draw.rectangle([0, height-30, width, height], fill=(245, 245, 245))
    draw.line([0, height-30, width, height-30], fill=(180, 180, 180), width=1)
    draw.text((10, height-20), "✓ Query executed in 1.2 sec", fill=(0, 128, 0), font=small_font)
    draw.text((300, height-20), "3 rows fetched", fill=(80, 80, 80), font=small_font)
    
    img.save('screenshots/04_DBeaver_Target_Extra_Records.png')
    print("✓ Created: 04_DBeaver_Target_Extra_Records.png")

def create_pgadmin_discrepancy_details():
    """Create pgAdmin screenshot showing detailed discrepancy records"""
    width, height = 1400, 900
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    title_font, bold_font, mono_font, small_font = get_fonts()
    
    # pgAdmin Title Bar (Teal)
    draw.rectangle([0, 0, width, 32], fill=(55, 90, 127))
    draw.text((15, 9), "pgAdmin 4 - Query Tool - ETL_DB on PostgreSQL 14.5", fill=(255, 255, 255), font=bold_font)
    
    # Menu bar
    draw.rectangle([0, 32, width, 55], fill=(240, 240, 240))
    draw.line([0, 55, width, 55], fill=(190, 190, 190), width=1)
    
    # Toolbar
    draw.rectangle([0, 55, width, 88], fill=(248, 248, 248))
    
    # Execute button (Green with play icon)
    draw.rectangle([10, 60, 80, 83], fill=(92, 184, 92), outline=(70, 150, 70), width=1)
    draw.text((20, 66), "▶ Execute", fill=(255, 255, 255), font=bold_font)
    
    # Other buttons
    draw.rectangle([90, 60, 150, 83], fill=(230, 230, 230), outline=(180, 180, 180), width=1)
    draw.text((98, 66), "⟲ Refresh", fill=(60, 60, 60), font=small_font)
    
    # SQL Editor Pane
    draw.rectangle([5, 95, width-5, 280], fill=(255, 255, 255), outline=(200, 200, 200), width=1)
    
    sql_text = """-- Query to show detailed discrepancy records
SELECT * FROM (
  SELECT * FROM source_transformed
  EXCEPT 
  SELECT * FROM target_data
) AS missing_records
LIMIT 100;"""
    
    y_pos = 105
    for line in sql_text.split('\n'):
        if '--' in line:
            draw.text((15, y_pos), line, fill=(128, 128, 128), font=mono_font)
        else:
            draw.text((15, y_pos), line, fill=(0, 0, 128), font=mono_font)
        y_pos += 16
    
    # Data Output Tab
    draw.rectangle([5, 285, width-5, 315], fill=(235, 235, 235))
    draw.rectangle([10, 290, 120, 315], fill=(255, 255, 255))
    draw.text((20, 295), "Data Output", fill=(0, 0, 0), font=bold_font)
    draw.text((130, 295), "Messages", fill=(100, 100, 100), font=title_font)
    draw.text((220, 295), "Notifications", fill=(100, 100, 100), font=title_font)
    
    # Results Grid Header
    col_headers = ["order_key", "customer_key", "order_date", "product_name", "quantity", "total_amount", "status"]
    col_widths = [120, 130, 120, 250, 100, 130, 120]
    
    x_pos = 5
    for i, (header, col_width) in enumerate(zip(col_headers, col_widths)):
        draw.rectangle([x_pos, 315, x_pos + col_width, 345], fill=(220, 230, 240), outline=(180, 180, 180), width=1)
        draw.text((x_pos + 8, 323), header, fill=(0, 0, 0), font=bold_font)
        x_pos += col_width
    
    # Sample discrepancy data rows
    data_rows = [
        ["10001", "C001", "2024-01-15", "LAPTOP DELL XPS 15", "1", "1299.99", "NEW"],
        ["10005", "C012", "2024-01-16", "WIRELESS MOUSE", "3", "89.97", "PROCESSING"],
        ["10008", "C008", "2024-01-17", "KEYBOARD MECHANICAL", "2", "249.98", "NEW"],
        ["10012", "C015", "2024-01-18", "MONITOR 27 INCH", "1", "399.00", "COMPLETED"],
        ["10019", "C023", "2024-01-19", "USB CABLE PACK", "5", "24.95", "NEW"],
        ["10024", "C029", "2024-01-20", "HDMI CABLE", "2", "15.98", "NEW"],
        ["10031", "C034", "2024-01-21", "LAPTOP BAG", "1", "49.99", "PROCESSING"],
        ["10037", "C041", "2024-01-22", "WEBCAM HD", "1", "79.99", "NEW"],
        ["10045", "C048", "2024-01-23", "HEADPHONES WIRELESS", "1", "149.99", "COMPLETED"],
        ["10052", "C055", "2024-01-24", "EXTERNAL SSD 1TB", "1", "129.99", "NEW"],
        ["10058", "C061", "2024-01-25", "SMARTPHONE CASE", "2", "39.98", "NEW"],
        ["10067", "C070", "2024-01-26", "POWER BANK", "1", "34.99", "PROCESSING"]
    ]
    
    y_pos = 345
    for row_idx, row_data in enumerate(data_rows):
        x_pos = 5
        bg_color = (255, 250, 240) if row_idx % 2 == 0 else (255, 255, 255)
        
        for col_idx, (value, col_width) in enumerate(zip(row_data, col_widths)):
            draw.rectangle([x_pos, y_pos, x_pos + col_width, y_pos + 28], fill=bg_color, outline=(220, 220, 220), width=1)
            draw.text((x_pos + 8, y_pos + 8), value, fill=(0, 0, 0), font=small_font)
            x_pos += col_width
        y_pos += 28
    
    # Row count indicator
    draw.rectangle([5, y_pos, width-5, y_pos + 30], fill=(245, 245, 245))
    draw.text((15, y_pos + 8), "Showing 12 of 12 rows", fill=(100, 100, 100), font=title_font)
    
    # Messages pane
    draw.rectangle([5, y_pos + 35, width-5, height-35], fill=(252, 252, 252), outline=(200, 200, 200), width=1)
    draw.text((15, y_pos + 45), "Query returned successfully in 1 secs 234 msec.", fill=(0, 100, 0), font=title_font)
    draw.text((15, y_pos + 65), "Total rows: 12", fill=(0, 0, 0), font=title_font)
    draw.text((15, y_pos + 85), "⚠ These 12 records exist in source but are missing from target table.", fill=(200, 100, 0), font=bold_font)
    
    # Status bar
    draw.rectangle([0, height-30, width, height], fill=(55, 90, 127))
    draw.text((10, height-18), "✓ Connected to ETL_DB", fill=(255, 255, 255), font=small_font)
    draw.text((200, height-18), "|", fill=(150, 180, 200), font=small_font)
    draw.text((210, height-18), "postgres@localhost:5432", fill=(255, 255, 255), font=small_font)
    
    img.save('screenshots/05_pgAdmin_Discrepancy_Details.png')
    print("✓ Created: 05_pgAdmin_Discrepancy_Details.png")

def main():
    os.makedirs('screenshots', exist_ok=True)
    print("\n🎨 Creating realistic database tool screenshots...\n")
    
    create_ssms_perfect_match()
    create_ssms_source_extra()
    create_dbeaver_perfect_match()
    create_dbeaver_target_extra()
    create_pgadmin_discrepancy_details()
    
    print("\n✅ All realistic screenshots created successfully!")
    print("📁 Saved in: screenshots/")
    print("\nScreenshots created:")
    print("  1. SSMS - Perfect Match (0 discrepancies)")
    print("  2. SSMS - Source Has 12 Extra Records")
    print("  3. DBeaver - Perfect Match")
    print("  4. DBeaver - Target Has 5 Extra Records")
    print("  5. pgAdmin - Detailed Discrepancy Records (12 rows)")

if __name__ == '__main__':
    main()
