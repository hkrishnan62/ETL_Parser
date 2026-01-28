"""
Flask Web Application for ETL Mapping Validator with AI Enhancement
"""
import os
import io
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from src.etl_validator import ETLValidator
from src.ai_enhanced_validator import AIEnhancedValidator
from src.ai_agent import get_ai_agent
from src.sql_playground import SQLPlayground
from src.test_case_generator import TestCaseGenerator
import traceback

app = Flask(__name__, static_folder='static', static_url_path='')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'xlsx', 'xls'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize SQL Playground
playground = SQLPlayground()


# SEO Headers Middleware
@app.after_request
def add_seo_headers(response):
    """Add SEO and security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # For HTML pages, prevent caching to always show latest version
    if response.content_type and 'text/html' in response.content_type:
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    # Don't override cache headers if already set (e.g., for robots.txt, static files)
    elif 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'public, max-age=3600'
    
    return response


def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/robots.txt')
def robots():
    """Serve robots.txt with appropriate headers for search engine crawling"""
    try:
        with open('static/robots.txt', 'r', encoding='utf-8') as f:
            robots_content = f.read()
        response = app.response_class(
            response=robots_content,
            status=200,
            mimetype='text/plain; charset=utf-8'
        )
        # Cache robots.txt for 24 hours but allow revalidation
        response.headers['Cache-Control'] = 'public, max-age=86400, must-revalidate'
        response.headers['Content-Type'] = 'text/plain; charset=utf-8'
        # Remove any no-cache directives that middleware might add
        if 'Pragma' in response.headers:
            del response.headers['Pragma']
        if 'Expires' in response.headers:
            del response.headers['Expires']
        return response
    except Exception as e:
        print(f"Error serving robots.txt: {str(e)}")
        return "robots.txt not found", 404


@app.route('/sitemap.xml')
def sitemap():
    """Serve sitemap.xml with correct content type"""
    try:
        with open('static/sitemap.xml', 'r', encoding='utf-8') as f:
            sitemap_content = f.read()
        response = app.response_class(
            response=sitemap_content,
            status=200,
            mimetype='application/xml; charset=utf-8'
        )
        response.headers['Content-Disposition'] = 'inline'
        return response
    except Exception as e:
        print(f"Error serving sitemap: {str(e)}")
        return "Sitemap not found", 404


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and generate queries"""
    try:
        print(f"=== Upload Request Received ===")
        print(f"Files in request: {list(request.files.keys())}")
        print(f"Form data: {dict(request.form)}")
        
        # Check if file is present
        if 'file' not in request.files:
            print("ERROR: No 'file' in request.files")
            return jsonify({'error': '❌ No file provided. Please upload a mapping file.'}), 400
        
        file = request.files['file']
        print(f"File received: {file.filename}, Content-Type: {file.content_type}")
        
        if file.filename == '':
            print("ERROR: Empty filename")
            return jsonify({'error': '❌ No file selected. Please choose a file to upload.'}), 400
        
        if not allowed_file(file.filename):
            print(f"ERROR: Invalid file type: {file.filename}")
            return jsonify({'error': '❌ Invalid file type. Please upload a CSV or Excel file (.csv, .xlsx, .xls).'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print(f"File saved to: {filepath}")
        
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
        
        # Load and validate mappings
        try:
            validator.load_mappings()
        except ValueError as ve:
            # Format validation errors with proper message
            error_msg = str(ve)
            print(f"Validation error: {error_msg}")
            return jsonify({'error': error_msg}), 400
        
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
        # Include mappings for test case generation
        summary['mappings'] = validator.mappings
        
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
            'error': f'❌ Error processing file: {str(e)}',
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


# ==================== SQL Playground Endpoints ====================

@app.route('/playground/execute', methods=['POST'])
def playground_execute():
    """Execute SQL query in playground"""
    try:
        data = request.json
        query = data.get('query', '')
        sample_data = data.get('sample_data')
        
        if not query.strip():
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        result = playground.execute_query(query, sample_data)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'rows': [],
            'columns': []
        }), 500


@app.route('/playground/share', methods=['POST'])
def playground_share():
    """Create shareable link for query"""
    try:
        data = request.json
        query = data.get('query', '')
        sample_data = data.get('sample_data')
        results = data.get('results')
        
        if not query.strip():
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        share_id = playground.create_share_link(query, sample_data, results)
        
        # Generate full URL
        base_url = request.host_url.rstrip('/')
        share_url = f"{base_url}/playground/{share_id}"
        
        return jsonify({
            'success': True,
            'share_id': share_id,
            'share_url': share_url
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/playground/')
def playground_home():
    """Render SQL playground page"""
    return render_template('playground.html', shared_data=None, share_id=None)


@app.route('/playground/<share_id>')
def playground_view_shared(share_id):
    """View shared query"""
    shared_data = playground.get_shared_query(share_id)
    
    if not shared_data:
        return "Shared query not found", 404
    
    return render_template('playground.html', shared_data=shared_data, share_id=share_id)


@app.route('/playground/samples')
def playground_samples():
    """Get sample queries"""
    return jsonify({
        'success': True,
        'samples': playground.get_sample_queries()
    })


@app.route('/playground/schema')
def playground_schema():
    """Get database schema"""
    return jsonify({
        'success': True,
        'schema': playground.get_database_schema()
    })


@app.route('/playground/profile/<table_name>')
def playground_profile(table_name):
    """Get data profiling for a table"""
    try:
        profile = playground.get_data_profile(table_name)
        return jsonify({
            'success': True,
            'profile': profile
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/playground/etl-test', methods=['POST'])
def playground_etl_test():
    """Run ETL validation test comparing source and target"""
    try:
        data = request.json
        source_query = data.get('source_query', '')
        target_query = data.get('target_query', '')
        
        if not source_query or not target_query:
            return jsonify({'error': 'Both source_query and target_query required'}), 400
        
        result = playground.run_etl_validation_test(source_query, target_query)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/playground/test-templates')
def playground_test_templates():
    """Get ETL test case templates"""
    return jsonify({
        'success': True,
        'templates': playground.get_etl_test_templates()
    })


@app.route('/generate-test-cases', methods=['POST'])
def generate_test_cases():
    """Generate test cases for mapping document"""
    try:
        data = request.json
        
        # Validate required data
        if not data.get('mappings') or not data.get('summary'):
            return jsonify({'error': 'Missing required data: mappings and summary'}), 400
        
        mappings = data.get('mappings')
        summary = data.get('summary')
        format_type = data.get('format', 'qtest').lower()
        test_type = data.get('test_type', 'all').lower()
        
        # Validate format type
        valid_formats = ['qtest', 'zephyr', 'testrail', 'ado', 'json']
        if format_type not in valid_formats:
            return jsonify({'error': f'Invalid format. Supported formats: {", ".join(valid_formats)}'}), 400
        
        # Validate test type
        valid_test_types = ['positive', 'negative', 'all']
        if test_type not in valid_test_types:
            return jsonify({'error': f'Invalid test type. Supported types: {", ".join(valid_test_types)}'}), 400
        
        # Generate test cases
        generator = TestCaseGenerator(mappings, summary)
        test_cases_data = generator.generate_all_test_cases()
        
        # Export in requested format
        exported_content = generator.export_test_cases(format_type, test_type)
        
        # Determine file extension
        file_extension = 'csv' if format_type != 'json' else 'json'
        filename = f'etl_test_cases_{format_type}_{test_type}.{file_extension}'
        
        # Create response based on format
        if format_type == 'json':
            return jsonify({
                'success': True,
                'content': exported_content,
                'filename': filename,
                'test_case_count': len(test_cases_data.get(test_type, test_cases_data['all'])),
                'format': format_type
            })
        else:
            # For CSV formats, return as downloadable file
            output = io.BytesIO()
            output.write(exported_content.encode('utf-8'))
            output.seek(0)
            
            return send_file(
                output,
                mimetype='text/csv',
                as_attachment=True,
                download_name=filename
            )
    
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error generating test cases: {error_trace}")
        return jsonify({
            'error': f'Error generating test cases: {str(e)}',
            'traceback': error_trace
        }), 500


@app.route('/preview-test-cases', methods=['POST'])
def preview_test_cases():
    """Preview test cases without downloading"""
    try:
        data = request.json
        
        # Validate required data
        if not data.get('mappings') or not data.get('summary'):
            return jsonify({'error': 'Missing required data: mappings and summary'}), 400
        
        mappings = data.get('mappings')
        summary = data.get('summary')
        test_type = data.get('test_type', 'all').lower()
        
        # Generate test cases
        generator = TestCaseGenerator(mappings, summary)
        test_cases_data = generator.generate_all_test_cases()
        
        # Get requested test cases
        selected_cases = test_cases_data.get(test_type, test_cases_data['all'])
        
        return jsonify({
            'success': True,
            'test_cases': selected_cases,
            'positive_count': len(test_cases_data['positive']),
            'negative_count': len(test_cases_data['negative']),
            'total_count': len(test_cases_data['all'])
        })
    
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error previewing test cases: {error_trace}")
        return jsonify({
            'error': f'Error previewing test cases: {str(e)}',
            'traceback': error_trace
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
