"""
Flask Web Application for ETL Mapping Validator with AI Enhancement
"""
import os
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from src.etl_validator import ETLValidator
from src.ai_enhanced_validator import AIEnhancedValidator
from src.ai_agent import get_ai_agent
import traceback

app = Flask(__name__, static_folder='static', static_url_path='')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'xlsx', 'xls'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and generate queries"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload a CSV or Excel file.'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get form parameters
        # Extract source_table dynamically from transformations or use default
        target_table = request.form.get('target_table', 'target_table')
        source_table = 'source_table'  # Will be extracted from transformations
        source_schema = request.form.get('source_schema', '').strip() or None
        target_schema = request.form.get('target_schema', '').strip() or None
        query_type = request.form.get('query_type', 'both')
        use_ai = request.form.get('use_ai', 'false').lower() == 'true'
        database_type = request.form.get('database_type', 'generic')
        
        # Use AI-enhanced validator if requested
        if use_ai:
            validator = AIEnhancedValidator(filepath)
        else:
            validator = ETLValidator(filepath)
        
        validator.load_mappings()
        
        # Get detected source tables from transformations
        summary = validator.get_mapping_summary()
        detected_tables = summary.get('detected_source_tables', [])
        
        # Use first detected source table or default
        if detected_tables:
            source_table = detected_tables[0]
        else:
            source_table = 'source_table'
        
        # Generate queries
        if use_ai and isinstance(validator, AIEnhancedValidator):
            result = validator.generate_with_optimization(
                source_table=source_table,
                target_table=target_table,
                source_schema=source_schema,
                target_schema=target_schema,
                database_type=database_type,
                query_type=query_type
            )
            queries = result.get('optimized_queries', result.get('original_queries'))
            ai_analysis = {
                'optimization_notes': result.get('optimization_notes', {}),
                'ai_available': result.get('ai_available', False)
            }
        else:
            queries = validator.generate_validation_queries(
                source_table=source_table,
                target_table=target_table,
                source_schema=source_schema,
                target_schema=target_schema,
                query_type=query_type
            )
            ai_analysis = {'ai_available': False}
        
        # Get mapping summary
        summary = validator.get_mapping_summary()
        
        return jsonify({
            'success': True,
            'queries': queries,
            'summary': summary,
            'ai_analysis': ai_analysis
        })
        
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error processing file: {error_trace}")
        return jsonify({
            'error': f'Error processing file: {str(e)}',
            'traceback': error_trace
        }), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    ai_agent = get_ai_agent()
    return jsonify({
        'status': 'healthy',
        'ai_available': ai_agent.is_available()
    })


@app.route('/ai/suggest-transformation', methods=['POST'])
def ai_suggest_transformation():
    """AI endpoint for transformation suggestions"""
    try:
        data = request.json
        source_column = data.get('source_column')
        target_column = data.get('target_column')
        source_type = data.get('source_type')
        target_type = data.get('target_type')
        
        if not source_column or not target_column:
            return jsonify({'error': 'source_column and target_column required'}), 400
        
        validator = AIEnhancedValidator()
        suggestion = validator.suggest_transformation(
            source_column, target_column, source_type, target_type
        )
        
        return jsonify(suggestion)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/ai/generate-from-description', methods=['POST'])
def ai_generate_from_description():
    """Generate mapping from natural language description"""
    try:
        data = request.json
        description = data.get('description')
        
        if not description:
            return jsonify({'error': 'description required'}), 400
        
        validator = AIEnhancedValidator()
        mappings = validator.generate_from_description(description)
        
        return jsonify({
            'success': True,
            'mappings': mappings
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/ai/analyze-mapping', methods=['POST'])
def ai_analyze_mapping():
    """Analyze uploaded mapping quality"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        database_type = request.form.get('database_type', 'generic')
        
        # Analyze with AI
        validator = AIEnhancedValidator(filepath)
        validator.load_mappings()
        
        analysis = validator.get_comprehensive_analysis(database_type)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
