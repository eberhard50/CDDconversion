#!/usr/bin/env python3
"""
Simple CDD Converter Web Application
Using existing simple_cdd_to_odx.py converter with Flask frontend
"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename

# Import our comprehensive converters
from comprehensive_odx_generator import ComprehensiveODXGenerator
from enhanced_cdd_parser import EnhancedCDDParser

# Import PDF converter
import sys
sys.path.append('src/converters')
from comprehensive_pdf_converter import create_comprehensive_pdf
from html_converter import HTMLConverter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cdd-converter-secret-key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configure upload and output folders
UPLOAD_FOLDER = Path('uploads')
OUTPUT_FOLDER = Path('outputs')
ALLOWED_EXTENSIONS = {'cdd', 'xml'}

# Create directories if they don't exist
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page with upload form"""
    return render_template('simple_index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and conversion"""
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(request.url)
    
    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload a .cdd or .xml file', 'error')
        return redirect(request.url)
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        session_id = str(uuid.uuid4())[:8]
        upload_path = UPLOAD_FOLDER / f"{session_id}_{filename}"
        file.save(upload_path)
        
        # Get ECU name from filename
        ecu_name = filename.rsplit('.', 1)[0]
        
        # Parse CDD file for comprehensive data
        parser = EnhancedCDDParser()
        cdd_document = parser.parse_file(str(upload_path))
        
        # Convert to comprehensive ODX-D using ALL CDD information
        generator = ComprehensiveODXGenerator()
        odx_content = generator.generate_complete_odx(str(upload_path), ecu_name)
        
        # Save ODX file
        odx_filename = f"{ecu_name}.odx-d"
        odx_path = OUTPUT_FOLDER / f"{session_id}_{odx_filename}"
        
        with open(odx_path, 'w', encoding='utf-8') as f:
            f.write(odx_content)
        
        # Generate comprehensive PDF documentation
        pdf_filename = f"{ecu_name}_Documentation.pdf"
        pdf_path = OUTPUT_FOLDER / f"{session_id}_{pdf_filename}"
        
        # Prepare data for PDF generation
        pdf_data = {
            'name': ecu_name,
            'source_file': filename,
            'services': cdd_document.protocol_services,
            'dids': cdd_document.dids
        }
        
        create_comprehensive_pdf(pdf_data, str(pdf_path))
        
        # Generate HTML documentation
        html_filename = f"{ecu_name}_Overview.html"
        html_path = OUTPUT_FOLDER / f"{session_id}_{html_filename}"
        
        html_converter = HTMLConverter()
        html_success = html_converter.convert_from_parsed_data(
            {
                'protocol_services': cdd_document.protocol_services,
                'dids': cdd_document.dids
            },
            str(html_path)
        )
        
        if not html_success:
            print("Warning: HTML generation failed, but continuing with other formats")
        
        # Prepare results
        results = {
            'success': True,
            'odx_filename': odx_filename,
            'pdf_filename': pdf_filename,
            'html_filename': html_filename,
            'session_id': session_id,
            'ecu_name': ecu_name,
            'original_filename': filename,
            'odx_file_size': f"{odx_path.stat().st_size} bytes",
            'pdf_file_size': f"{pdf_path.stat().st_size} bytes",
            'html_file_size': f"{html_path.stat().st_size} bytes" if html_success else "N/A",
            'services_count': len(cdd_document.protocol_services),
            'dids_count': len(cdd_document.dids),
            'html_success': html_success
        }
        
        return render_template('simple_results.html', results=results)
        
    except Exception as e:
        flash(f'Error processing file: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download/<session_id>/<filename>')
def download_file(session_id, filename):
    """Download converted file"""
    try:
        file_path = OUTPUT_FOLDER / f"{session_id}_{filename}"
        if file_path.exists():
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            flash('File not found or expired', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Download error: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/status')
def api_status():
    """API endpoint for application status"""
    return {
        'status': 'running',
        'version': '1.0.0',
        'supported_formats': ['odx-d', 'pdf', 'html'],
        'max_file_size': '16MB'
    }

if __name__ == '__main__':
    print("🚀 Starting CDD Converter Web Application...")
    print("📁 Upload folder:", UPLOAD_FOLDER.absolute())
    print("📤 Output folder:", OUTPUT_FOLDER.absolute())
    print("🌐 Open your browser and go to: http://127.0.0.1:5000")
    print("=" * 60)
    
    app.run(debug=True, host='127.0.0.1', port=5000)