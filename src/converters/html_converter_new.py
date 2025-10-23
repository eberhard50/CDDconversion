"""
HTML Converter for CDD files using XSLT transformation and parsed data
"""
import os
import logging
from lxml import etree
from pathlib import Path

logger = logging.getLogger(__name__)

class HTMLConverter:
    """Convert CDD data to HTML using XSLT transformation or parsed data"""
    
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
        """Generate HTML content from parsed CDD data"""
        
        services = cdd_data.get('protocol_services', [])
        dids = cdd_data.get('dids', [])
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>CANdela CDD Overview</title>
    <style>
        body{{font:14px system-ui;padding:16px;max-width:1200px;margin:0 auto}}
        h1{{color:#005CA2;border-bottom:2px solid #005CA2}}
        h2{{color:#0074CC;margin-top:24px}}
        table{{border-collapse:collapse;width:100%;margin:16px 0;box-shadow:0 2px 4px rgba(0,0,0,0.1)}}
        th,td{{border:1px solid #ddd;padding:8px;text-align:left;vertical-align:top}}
        th{{background:#f8f9fa;font-weight:600;color:#333}}
        tr:nth-child(even){{background:#f8f9fa}}
        tr:hover{{background:#e3f2fd}}
        code{{background:#f0f0f0;padding:2px 6px;border-radius:4px;font-family:monospace;font-size:13px}}
        .sid{{background:#e8f5e8;color:#2e7d32;font-weight:bold}}
        .did{{background:#fff3e0;color:#f57c00;font-weight:bold}}
        .desc{{max-width:300px;word-wrap:break-word}}
        .center{{text-align:center}}
    </style>
</head>
<body>
    <h1>CANdela CDD Overview</h1>
    
    <p><strong>Document:</strong> Enhanced CDD Converter | <strong>Services:</strong> {len(services)} | <strong>DIDs:</strong> {len(dids)}</p>

    <h2>UDS Diagnostic Services</h2>
    <p>Total Services: <strong>{len(services)}</strong></p>
    <table>
        <tr>
            <th>SID</th>
            <th>Service Name</th>
            <th>Description</th>
            <th>Func</th>
            <th>Phys</th>
            <th>Multiple Response</th>
        </tr>"""
        
        # Add services to table
        for service in services[:50]:  # Limit to first 50 services
            uds_id = getattr(service, 'uds_service_id', None)
            service_name = getattr(service, 'name', 'Unknown Service')
            description = getattr(service, 'description', '')
            func = getattr(service, 'func', False)
            phys = getattr(service, 'phys', False)
            mresp = getattr(service, 'multiple_response', False)
            
            # Clean service name
            if service_name.startswith('($'):
                parts = service_name.split(') ', 1)
                if len(parts) > 1:
                    clean_name = parts[1]
                else:
                    clean_name = service_name
            else:
                clean_name = service_name
            
            # Format SID
            sid_str = f"0x{uds_id:02X}" if uds_id is not None else 'N/A'
            
            # Truncate description
            if len(description) > 100:
                description = description[:97] + "..."
            
            html += f"""
        <tr>
            <td class="center"><code class="sid">{sid_str}</code></td>
            <td>{clean_name}</td>
            <td class="desc">{description if description else '-'}</td>
            <td class="center">{'✓' if func else '✗'}</td>
            <td class="center">{'✓' if phys else '✗'}</td>
            <td class="center">{'✓' if mresp else '✗'}</td>
        </tr>"""
        
        html += f"""
    </table>

    <h2>Data Identifiers (DIDs)</h2>
    <p>Total DIDs: <strong>{len(dids)}</strong></p>
    <table>
        <tr>
            <th>DID</th>
            <th>Name</th>
            <th>Description</th>
            <th>Readable</th>
            <th>Writable</th>
        </tr>"""
        
        # Add DIDs to table
        for did in dids[:50]:  # Limit to first 50 DIDs
            did_id = getattr(did, 'did_id', None)
            if did_id is None:
                did_id = getattr(did, 'id', 0)
            
            did_name = getattr(did, 'name', 'Unknown DID')
            description = getattr(did, 'description', '')
            readable = getattr(did, 'readable', True)
            writable = getattr(did, 'writable', False)
            
            # Format DID ID
            if isinstance(did_id, str):
                try:
                    if did_id.startswith('0x'):
                        did_id = int(did_id, 16)
                    else:
                        did_id = int(did_id)
                except ValueError:
                    did_id = 0
            
            did_id_str = f"0x{did_id:04X}" if isinstance(did_id, int) else str(did_id)
            
            # Clean DID name
            if did_name.startswith('($'):
                parts = did_name.split(') ', 1)
                if len(parts) > 1:
                    clean_name = parts[1]
                else:
                    clean_name = did_name
            else:
                clean_name = did_name
            
            # Truncate description
            if len(description) > 100:
                description = description[:97] + "..."
            
            html += f"""
        <tr>
            <td class="center"><code class="did">{did_id_str}</code></td>
            <td>{clean_name}</td>
            <td class="desc">{description if description else '-'}</td>
            <td class="center">{'✓' if readable else '✗'}</td>
            <td class="center">{'✓' if writable else '✗'}</td>
        </tr>"""
        
        html += """
    </table>

    <hr style="margin-top:40px"/>
    <p style="text-align:center;color:#666;font-size:12px">
        Generated by Enhanced CDD Converter | Vector CANdela Format
    </p>

</body>
</html>"""
        
        return html


def create_html_report(cdd_file_path, output_file):
    """
    Standalone function to create HTML report from CDD file
    
    Args:
        cdd_file_path (str): Path to input CDD file
        output_file (str): Path to output HTML file
        
    Returns:
        bool: True if successful, False otherwise
    """
    converter = HTMLConverter()
    return converter.convert(cdd_file_path, output_file)