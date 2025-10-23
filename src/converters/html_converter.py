"""
HTML Converter for CDD files using XSLT transformation
"""
import os
import logging
from lxml import etree
from pathlib import Path

logger = logging.getLogger(__name__)

class HTMLConverter:
    """Convert CDD data to HTML using XSLT transformation"""
    
    def __init__(self):
        self.xslt_path = "cdd_to_html_minimal.xsl"
        
    def convert(self, cdd_file_path, output_file):
        """
        Convert CDD file to HTML using XSLT transformation
        
        Args:
            cdd_file_path (str): Path to input CDD file
            output_file (str): Path to output HTML file
            
        Returns:
            bool: True if conversion successful, False otherwise
        """
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Load XSLT stylesheet
            if not os.path.exists(self.xslt_path):
                logger.error(f"XSLT stylesheet not found: {self.xslt_path}")
                return False
                
            with open(self.xslt_path, 'r', encoding='utf-8') as f:
                xslt_content = f.read()
            
            xslt_doc = etree.fromstring(xslt_content.encode('utf-8'))
            transform = etree.XSLT(xslt_doc)
            
            # Load and parse CDD file
            logger.info(f"Converting CDD file: {cdd_file_path}")
            
            # Parse CDD XML with error handling
            parser = etree.XMLParser(recover=True, encoding='utf-8')
            with open(cdd_file_path, 'r', encoding='utf-8') as f:
                cdd_content = f.read()
            
            # Clean up potential DTD issues
            if '<!DOCTYPE' in cdd_content:
                # Remove DTD declaration to avoid external file issues
                start = cdd_content.find('<!DOCTYPE')
                end = cdd_content.find('>', start) + 1
                cdd_content = cdd_content[:start] + cdd_content[end:]
            
            cdd_doc = etree.fromstring(cdd_content.encode('utf-8'), parser)
            
            # Transform to HTML
            result = transform(cdd_doc)
            
            # Write result to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(str(result))
            
            logger.info(f"HTML conversion completed: {output_file}")
            return True
            
        except etree.XSLTApplyError as e:
            logger.error(f"XSLT transformation error: {e}")
            return False
        except etree.XMLSyntaxError as e:
            logger.error(f"XML parsing error: {e}")
            return False
        except Exception as e:
            logger.error(f"HTML conversion failed: {e}")
            return False

    def convert_from_parsed_data(self, cdd_data, output_file):
        """
        Convert parsed CDD data to HTML (alternative approach)
        
        Args:
            cdd_data (dict): Parsed CDD data from enhanced parser
            output_file (str): Path to output HTML file
            
        Returns:
            bool: True if conversion successful, False otherwise
        """
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Generate HTML from parsed data
            html_content = self._generate_html_from_data(cdd_data)
            
            # Write HTML file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"HTML generated from parsed data: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"HTML generation from parsed data failed: {e}")
            return False

    def _generate_html_from_data(self, cdd_data):
        """
        Generate HTML content from parsed CDD data
        
        Args:
            cdd_data (dict): Dictionary containing protocol_services and dids
            
        Returns:
            str: Generated HTML content
        """
        protocol_services = cdd_data.get('protocol_services', [])
        dids = cdd_data.get('dids', [])
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CDD File Analysis Report</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background-color: #f5f5f5; 
            line-height: 1.6;
        }}
        .header {{
            background: linear-gradient(135deg, #B70032, #E31837);
            color: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{ 
            margin: 0; 
            font-size: 2.5em; 
            font-weight: 300;
        }}
        .header p {{ 
            margin: 10px 0 0 0; 
            font-size: 1.1em; 
            opacity: 0.9;
        }}
        .container {{ 
            max-width: 1200px; 
            margin: 0 auto; 
        }}
        .summary {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }}
        .summary-card {{
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .summary-card h3 {{
            margin: 0 0 10px 0;
            color: #B70032;
            font-size: 1.2em;
        }}
        .summary-card .number {{
            font-size: 3em;
            font-weight: bold;
            color: #333;
            margin: 10px 0;
        }}
        .section {{
            background: white;
            margin-bottom: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .section-header {{
            background: #B70032;
            color: white;
            padding: 20px;
            font-size: 1.3em;
            font-weight: 500;
        }}
        .section-content {{
            padding: 25px;
        }}
        .service-item, .did-item {{
            border-left: 4px solid #B70032;
            padding: 15px;
            margin-bottom: 15px;
            background: #f9f9f9;
            border-radius: 0 4px 4px 0;
        }}
        .service-item h4, .did-item h4 {{
            margin: 0 0 10px 0;
            color: #B70032;
            font-size: 1.1em;
        }}
        .service-item p, .did-item p {{
            margin: 5px 0;
            color: #666;
        }}
        .service-item strong, .did-item strong {{
            color: #333;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
            margin-top: 40px;
        }}
        @media (max-width: 768px) {{
            .summary {{ grid-template-columns: 1fr; }}
            .container {{ padding: 10px; }}
            .header {{ padding: 20px; }}
            .header h1 {{ font-size: 2em; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>CDD Analysis Report</h1>
            <p>Comprehensive overview of CANdela database content</p>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <h3>Protocol Services</h3>
                <div class="number">{len(protocol_services)}</div>
                <p>UDS diagnostic services</p>
            </div>
            <div class="summary-card">
                <h3>Data Identifiers</h3>
                <div class="number">{len(dids)}</div>
                <p>Available DIDs</p>
            </div>
        </div>
        
        <div class="section">
            <div class="section-header">Protocol Services</div>
            <div class="section-content">
"""

        if protocol_services:
            html_content += '<div class="grid">'
            for service in protocol_services:
                html_content += f"""
                <div class="service-item">
                    <h4>Service ID: {getattr(service, 'service_id', 'N/A')}</h4>
                    <p><strong>Name:</strong> {getattr(service, 'name', 'N/A')}</p>
                    <p><strong>Type:</strong> {getattr(service, 'service_type', 'N/A')}</p>
                    <p><strong>Description:</strong> {getattr(service, 'description', 'No description available')}</p>
                </div>"""
            html_content += '</div>'
        else:
            html_content += '<p>No protocol services found in the CDD file.</p>'

        html_content += f"""
            </div>
        </div>
        
        <div class="section">
            <div class="section-header">Data Identifiers (DIDs)</div>
            <div class="section-content">
"""

        if dids:
            html_content += '<div class="grid">'
            for did in dids:
                html_content += f"""
                <div class="did-item">
                    <h4>DID: {getattr(did, 'did_id', 'N/A')}</h4>
                    <p><strong>Name:</strong> {getattr(did, 'name', 'N/A')}</p>
                    <p><strong>Type:</strong> {getattr(did, 'data_type', 'N/A')}</p>
                    <p><strong>Length:</strong> {getattr(did, 'length', 'N/A')} bytes</p>
                    <p><strong>Description:</strong> {getattr(did, 'description', 'No description available')}</p>
                </div>"""
            html_content += '</div>'
        else:
            html_content += '<p>No data identifiers found in the CDD file.</p>'

        html_content += """
            </div>
        </div>
        
        <div class="footer">
            <p>Generated by CDD Converter Tool - Vector/Bosch Automotive Solutions</p>
        </div>
    </div>
</body>
</html>"""

        return html_content