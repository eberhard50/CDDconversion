#!/usr/bin/env python3
"""
Comprehensive PDF Converter for CDD to Human-Readable Documentation
Creates professional PDF documentation with working links and detailed explanations
"""

import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, KeepTogether, Image, Frame, PageTemplate
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

class ComprehensivePDFConverter:
    """Creates comprehensive PDF documentation from CDD data"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        self.story = []
        self.toc = TableOfContents()
        
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for professional formatting"""
        # Clear existing styles and add custom ones
        
        # Title page style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#B70032'),  # Bosch red
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ), alias='CustomTitle')
        
        # Header styles - use different names to avoid conflicts
        self.styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=self.styles['Normal'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.HexColor('#333333'),
            backgroundColor=colors.HexColor('#DDDDDD'),
            leftIndent=0,
            rightIndent=0,
            fontName='Helvetica-Bold'
        ), alias='CustomHeading1')
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Normal'],
            fontSize=13,
            spaceAfter=10,
            spaceBefore=15,
            textColor=colors.HexColor('#444444'),
            fontName='Helvetica-Bold'
        ), alias='CustomHeading2')
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading3',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            spaceBefore=12,
            textColor=colors.HexColor('#555555'),
            fontName='Helvetica-Bold'
        ), alias='CustomHeading3')
        
        # Service description styles
        self.styles.add(ParagraphStyle(
            name='ServiceDescription',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=6,
            fontName='Helvetica-Oblique',
            textColor=colors.HexColor('#666666')
        ))
        
        # Code/hex styles
        self.styles.add(ParagraphStyle(
            name='CodeStyle',
            parent=self.styles['Normal'],
            fontSize=9,
            fontName='Courier',
            textColor=colors.HexColor('#000080'),
            backgroundColor=colors.HexColor('#F5F5F5'),
            leftIndent=10,
            rightIndent=10
        ))
        
        # Info box style
        self.styles.add(ParagraphStyle(
            name='InfoBox',
            parent=self.styles['Normal'],
            fontSize=8,
            backgroundColor=colors.HexColor('#E8F4FD'),
            borderColor=colors.HexColor('#0066CC'),
            borderWidth=1,
            leftIndent=15,
            rightIndent=15,
            spaceBefore=6,
            spaceAfter=6
        ))

    def convert_to_pdf(self, cdd_data, output_path):
        """Convert CDD data to comprehensive PDF documentation"""
        # Create PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=20*mm,
            leftMargin=20*mm,
            topMargin=25*mm,
            bottomMargin=25*mm
        )
        
        # Build document content
        self._build_title_page(cdd_data)
        self._build_table_of_contents()
        self._build_overview(cdd_data)
        self._build_communication_parameters(cdd_data)
        self._build_services_section(cdd_data)
        self._build_dids_section(cdd_data)
        self._build_appendix(cdd_data)
        
        # Build PDF
        doc.build(self.story)
        return output_path
    
    def _build_title_page(self, cdd_data):
        """Create professional title page"""
        # Main title
        title = f"UDS Diagnostic Specification<br/>{cdd_data.get('name', 'CDD Document')}"
        self.story.append(Paragraph(title, self.styles['CustomTitle']))
        self.story.append(Spacer(1, 20*mm))
        
        # Document info table
        doc_info = [
            ['Template:', 'Vector Reference 2.3.0'],
            ['Target Groups:', 'Development, Manufacturing, Service, Legislated'],
            ['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Source File:', cdd_data.get('source_file', 'Unknown')],
            ['Services Found:', str(len(cdd_data.get('services', [])))],
            ['DIDs Found:', str(len(cdd_data.get('dids', [])))]
        ]
        
        info_table = Table(doc_info, colWidths=[40*mm, 100*mm])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('RIGHTPADDING', (0, 0), (0, -1), 10),
            ('LEFTPADDING', (1, 0), (1, -1), 10),
        ]))
        
        self.story.append(info_table)
        self.story.append(Spacer(1, 15*mm))
        
        # Generation info
        gen_info = f"Generated by CDD Converter Tool, {datetime.now().strftime('%Y-%m-%d')}"
        self.story.append(Paragraph(gen_info, self.styles['ServiceDescription']))
        
        self.story.append(PageBreak())
    
    def _build_table_of_contents(self):
        """Build table of contents"""
        self.story.append(Paragraph("Table of Contents", self.styles['CustomHeading1']))
        self.story.append(Spacer(1, 12))
        
        # Manual TOC for now - in a full implementation, this would be auto-generated
        toc_entries = [
            "1. Conventions",
            "2. Overview", 
            "3. Communication Parameters",
            "4. UDS Protocol Services",
            "5. Data Identifiers (DIDs)",
            "6. Appendix"
        ]
        
        for entry in toc_entries:
            self.story.append(Paragraph(entry, self.styles['Normal']))
        
        self.story.append(PageBreak())
    
    def _build_overview(self, cdd_data):
        """Build overview section"""
        self.story.append(Paragraph("1. Overview", self.styles['CustomHeading1']))
        
        overview_text = f"""
        This document describes the UDS (Unified Diagnostic Services) implementation 
        for the {cdd_data.get('name', 'vehicle control unit')}. The specification includes 
        {len(cdd_data.get('services', []))} protocol services and {len(cdd_data.get('dids', []))} 
        data identifiers (DIDs).
        
        The diagnostic communication follows ISO 14229 standard and provides access to 
        vehicle diagnostic data, configuration parameters, and control functions.
        """
        
        self.story.append(Paragraph(overview_text, self.styles['Normal']))
        self.story.append(Spacer(1, 12))
    
    def _build_communication_parameters(self, cdd_data):
        """Build communication parameters section"""
        self.story.append(Paragraph("2. Communication Parameters", self.styles['CustomHeading1']))
        
        # Communication parameters table
        comm_params = [
            ['Parameter', 'Value', 'Description'],
            ['Protocol', 'UDS (ISO 14229)', 'Unified Diagnostic Services'],
            ['Transport', 'CAN-TP (ISO 15765-2)', 'CAN Transport Protocol'],
            ['Physical Request ID', '0x7E0', 'Diagnostic request identifier'],
            ['Physical Response ID', '0x7E8', 'Diagnostic response identifier'],
            ['P2 Timeout', '50 ms', 'Performance requirement timeout'],
            ['P2* Timeout', '5000 ms', 'Enhanced performance timeout'],
        ]
        
        params_table = Table(comm_params, colWidths=[40*mm, 30*mm, 70*mm])
        params_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8E8E8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        self.story.append(params_table)
        self.story.append(Spacer(1, 12))
    
    def _build_services_section(self, cdd_data):
        """Build UDS services section"""
        self.story.append(Paragraph("3. UDS Protocol Services", self.styles['CustomHeading1']))
        
        services = cdd_data.get('services', [])
        
        # Services overview table with better formatting and links
        service_overview = [['Service ID', 'Service Name', 'Support', 'Description']]
        
        for i, service in enumerate(services):
            # Get UDS service ID (0x10, 0x22, etc.)
            uds_id = getattr(service, 'uds_service_id', None)
            service_id_str = f"0x{uds_id:02X}" if uds_id is not None else 'N/A'
            
            # Get service name and clean it up
            service_name = getattr(service, 'name', 'Unknown Service')
            if service_name.startswith('($'):
                # Extract clean name from "($10) DiagnosticSessionControl" format
                parts = service_name.split(') ', 1)
                if len(parts) > 1:
                    service_name = parts[1]
            
            # Get description with proper text wrapping
            description = getattr(service, 'description', '')
            if not description or description == service_name:
                description = 'UDS diagnostic service'
            
            # Use simple service name without problematic links
            clean_service_name = service_name
            
            # Wrap text in Paragraph objects for better formatting
            description_para = Paragraph(description, self.styles['Normal'])
            service_name_para = Paragraph(clean_service_name, self.styles['Normal'])
            
            service_overview.append([
                service_id_str,
                service_name_para,
                '✓' if getattr(service, 'func', True) else '✗',
                description_para
            ])
        
        # Create table with better column widths and auto-sizing rows
        services_table = Table(service_overview, colWidths=[25*mm, 45*mm, 15*mm, 55*mm])
        services_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8E8E8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (2, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F8F8')]),
            # Allow row height to expand based on content
            ('WORDWRAP', (0, 0), (-1, -1), True),
            ('SPLITBYROW', (0, 0), (-1, -1), 1),
        ]))
        
        self.story.append(services_table)
        self.story.append(Spacer(1, 12))
        
        # Add service index with links
        self._build_service_index(services)
        
        # Detailed service descriptions
        self._build_detailed_services(services)
    
    def _build_service_index(self, services):
        """Build service index with simple references to detailed sections"""
        self.story.append(Paragraph("3.1 Service Index", self.styles['CustomHeading2']))
        
        index_text = "Service overview with corresponding section references:<br/><br/>"
        
        for i, service in enumerate(services[:20]):  # Limit to first 20
            uds_id = getattr(service, 'uds_service_id', None)
            service_id_str = f"0x{uds_id:02X}" if uds_id is not None else 'N/A'
            
            service_name = getattr(service, 'name', 'Unknown Service')
            if service_name.startswith('($'):
                parts = service_name.split(') ', 1)
                if len(parts) > 1:
                    service_name = parts[1]
            
            # Create simple reference to detailed section
            link_text = f"• {service_id_str} - {service_name} → Section 3.2.{i+1}<br/>"
            index_text += link_text
        
        self.story.append(Paragraph(index_text, self.styles['Normal']))
        self.story.append(Spacer(1, 12))
    
    def _build_detailed_services(self, services):
        """Build detailed service descriptions with improved formatting"""
        self.story.append(Paragraph("3.2 Detailed Service Descriptions", self.styles['CustomHeading2']))
        
        for i, service in enumerate(services[:20]):  # Limit to first 20 for PDF size
            uds_id = getattr(service, 'uds_service_id', None)
            service_id_str = f"0x{uds_id:02X}" if uds_id is not None else 'N/A'
            
            service_name = getattr(service, 'name', f'Service_{i}')
            if service_name.startswith('($'):
                parts = service_name.split(') ', 1)
                if len(parts) > 1:
                    clean_name = parts[1]
                else:
                    clean_name = service_name
            else:
                clean_name = service_name
            
            # Service header with simple anchor
            header = f"3.2.{i+1} {clean_name} ({service_id_str})"
            self.story.append(Paragraph(header, self.styles['CustomHeading3']))
            
            # Service description - now with full enhanced descriptions
            description = getattr(service, 'description', '')
            if not description or description == clean_name or len(description) < 20:
                # Use original name as fallback
                description = f"UDS diagnostic service providing {clean_name} functionality according to ISO 14229-1 specification."
            
            # Wrap description text for better formatting
            desc_text = description.replace('. ', '.\n\n')  # Add line breaks for better readability
            self.story.append(Paragraph(desc_text, self.styles['ServiceDescription']))
            
            # Service properties table with better formatting
            properties = [
                ['Property', 'Value', 'Description'],
                ['Service ID', service_id_str, 'UDS service identifier (hex)'],
                ['Service Name', clean_name, 'Descriptive name of the service'],
                ['Functional Addressing', '✓' if getattr(service, 'func', False) else '✗', 'Supports functional addressing mode'],
                ['Physical Addressing', '✓' if getattr(service, 'phys', False) else '✗', 'Supports physical addressing mode'],
                ['Multiple Response', '✓' if getattr(service, 'multiple_response', False) else '✗', 'Can send multiple response messages'],
                ['Response on Physical', '✓' if getattr(service, 'response_on_physical', False) else '✗', 'Responds to physical requests'],
                ['Response on Functional', '✓' if getattr(service, 'response_on_functional', False) else '✗', 'Responds to functional requests'],
            ]
            
            # Create property table with wrapping text
            props_table_data = []
            for row in properties:
                wrapped_row = []
                for cell in row:
                    if isinstance(cell, str) and len(cell) > 30:
                        # Wrap long text in paragraph
                        wrapped_row.append(Paragraph(cell, self.styles['Normal']))
                    else:
                        wrapped_row.append(cell)
                props_table_data.append(wrapped_row)
            
            props_table = Table(props_table_data, colWidths=[35*mm, 25*mm, 80*mm])
            props_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8E8E8')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (1, 1), (1, -1), 'CENTER'),
                ('WORDWRAP', (0, 0), (-1, -1), True),
                ('SPLITBYROW', (0, 0), (-1, -1), 1),
            ]))
            
            self.story.append(props_table)
            
            # Request/Response format if available
            request = getattr(service, 'request', None)
            if request:
                self.story.append(Paragraph("Request Format:", self.styles['Normal']))
                req_name = getattr(request, 'name', 'Request')
                self.story.append(Paragraph(f"Message: {req_name}", self.styles['CodeStyle']))
            
            pos_response = getattr(service, 'positive_response', None)
            if pos_response:
                self.story.append(Paragraph("Positive Response:", self.styles['Normal']))
                pos_name = getattr(pos_response, 'name', 'Positive Response')
                self.story.append(Paragraph(f"Message: {pos_name}", self.styles['CodeStyle']))
            
            self.story.append(Spacer(1, 10))
    
    def _build_dids_section(self, cdd_data):
        """Build DIDs section with improved formatting and links"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("4. Data Identifiers (DIDs)", self.styles['CustomHeading1']))
        
        dids = cdd_data.get('dids', [])
        
        # DIDs overview with simple anchor
        self.story.append(Paragraph("4.1 DID Overview", self.styles['CustomHeading2']))
        overview_text = f"""
        This section describes the {len(dids)} Data Identifiers (DIDs) available 
        through the ReadDataByIdentifier (0x22) and WriteDataByIdentifier (0x2E) services.
        """
        self.story.append(Paragraph(overview_text, self.styles['Normal']))
        self.story.append(Spacer(1, 12))
        
        # DIDs table with proper formatting and text wrapping
        did_table_data = [['DID', 'Name', 'Read', 'Write', 'Length', 'Details']]
        
        for i, did in enumerate(dids[:50]):  # Limit to first 50 for PDF size
            # Get DID ID - try different possible attributes
            did_id = getattr(did, 'did_id', None)
            if did_id is None:
                did_id = getattr(did, 'id', 0)
            
            # Convert to proper format if it's a string
            if isinstance(did_id, str):
                try:
                    # Handle hex strings like "0xFE90" or just numbers
                    if did_id.startswith('0x'):
                        did_id = int(did_id, 16)
                    else:
                        did_id = int(did_id)
                except ValueError:
                    did_id = 0
            
            did_name = getattr(did, 'name', 'Unknown DID')
            
            # Clean up name if it has special formatting
            if did_name.startswith('($'):
                parts = did_name.split(') ', 1)
                if len(parts) > 1:
                    clean_name = parts[1]
                else:
                    clean_name = did_name
            else:
                clean_name = did_name
            
            # Create simple reference to detailed section
            link_text = f'Section 4.2.{i+1}'
            
            # Use Paragraph objects for text wrapping
            did_table_data.append([
                Paragraph(f"0x{did_id:04X}" if isinstance(did_id, int) else str(did_id), self.styles['Normal']),
                Paragraph(clean_name[:25], self.styles['Normal']),
                Paragraph('✓' if getattr(did, 'readable', True) else '✗', self.styles['Normal']),
                Paragraph('✓' if getattr(did, 'writable', False) else '✗', self.styles['Normal']),
                Paragraph(f"{getattr(did, 'length', 0)} bytes", self.styles['Normal']),
                Paragraph(link_text, self.styles['Normal'])
            ])
        
        dids_table = Table(did_table_data, colWidths=[20*mm, 35*mm, 12*mm, 12*mm, 18*mm, 23*mm])
        dids_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8E8E8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (3, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('WORDWRAP', (0, 0), (-1, -1), True),
            ('SPLITBYROW', (0, 0), (-1, -1), 1),
        ]))
        
        self.story.append(dids_table)
        
        # Detailed DID descriptions
        self.story.append(Paragraph("4.2 Detailed DID Descriptions", self.styles['CustomHeading2']))
        
        for i, did in enumerate(dids[:15]):  # Show details for first 15 DIDs
            # Get DID ID
            did_id = getattr(did, 'did_id', None)
            if did_id is None:
                did_id = getattr(did, 'id', 0)
            
            if isinstance(did_id, str):
                try:
                    if did_id.startswith('0x'):
                        did_id = int(did_id, 16)
                    else:
                        did_id = int(did_id)
                except ValueError:
                    did_id = 0
            
            did_name = getattr(did, 'name', 'Unknown DID')
            did_description = getattr(did, 'description', '')
            
            # Clean up name
            if did_name.startswith('($'):
                parts = did_name.split(') ', 1)
                if len(parts) > 1:
                    clean_name = parts[1]
                else:
                    clean_name = did_name
            else:
                clean_name = did_name
            
            # DID header with simple format
            did_id_str = f"0x{did_id:04X}" if isinstance(did_id, int) else str(did_id)
            header = f"4.2.{i+1} {clean_name} (DID: {did_id_str})"
            self.story.append(Paragraph(header, self.styles['CustomHeading3']))
            
            # Enhanced description
            if not did_description or len(did_description) < 20:
                did_description = f"Data Identifier {did_id_str} providing {clean_name} data for diagnostic and monitoring purposes."
            
            # Format description with line breaks for readability
            formatted_desc = did_description.replace('. ', '.\n\n')
            self.story.append(Paragraph(formatted_desc, self.styles['ServiceDescription']))
            
            # DID properties table with text wrapping
            properties = [
                ['Property', 'Value', 'Description'],
                ['DID ID', did_id_str, 'Data Identifier value (hexadecimal)'],
                ['Name', clean_name, 'Descriptive name of the data'],
                ['Readable', '✓' if getattr(did, 'readable', True) else '✗', 'Can be read using ReadDataByIdentifier (0x22)'],
                ['Writable', '✓' if getattr(did, 'writable', False) else '✗', 'Can be written using WriteDataByIdentifier (0x2E)'],
                ['Length', f"{getattr(did, 'length', 0)} bytes", 'Data length in bytes'],
                ['Type', getattr(did, 'type', 'Unknown'), 'Data type or category'],
            ]
            
            # Create property table with text wrapping
            props_table_data = []
            for row in properties:
                wrapped_row = []
                for cell in row:
                    if isinstance(cell, str) and len(cell) > 25:
                        wrapped_row.append(Paragraph(cell, self.styles['Normal']))
                    else:
                        wrapped_row.append(cell)
                props_table_data.append(wrapped_row)
            
            props_table = Table(props_table_data, colWidths=[30*mm, 30*mm, 80*mm])
            props_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8E8E8')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (1, 1), (1, -1), 'CENTER'),
                ('WORDWRAP', (0, 0), (-1, -1), True),
                ('SPLITBYROW', (0, 0), (-1, -1), 1),
            ]))
            
            self.story.append(props_table)
            self.story.append(Spacer(1, 10))
        self.story.append(Spacer(1, 12))
    
    def _build_appendix(self, cdd_data):
        """Build appendix with technical details"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("5. Appendix", self.styles['CustomHeading1']))
        
        # Technical notes
        self.story.append(Paragraph("5.1 Technical Notes", self.styles['CustomHeading2']))
        
        tech_notes = """
        • All multi-byte values are transmitted in big-endian byte order
        • Negative Response Codes (NRCs) follow ISO 14229-1 specification
        • Session management is required for security-protected services
        • Physical addressing is used for all diagnostic communication
        • The diagnostic session must be maintained during service execution
        """
        
        self.story.append(Paragraph(tech_notes, self.styles['Normal']))
        
        # Conversion information
        self.story.append(Paragraph("5.2 Document Generation", self.styles['CustomHeading2']))
        
        conversion_info = f"""
        This document was automatically generated from CDD source file: {cdd_data.get('source_file', 'unknown')}
        
        Conversion Statistics:
        • Services extracted: {len(cdd_data.get('services', []))}
        • DIDs extracted: {len(cdd_data.get('dids', []))}
        • Generation time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        • Tool version: CDD Converter v1.0
        """
        
        self.story.append(Paragraph(conversion_info, self.styles['InfoBox']))

def create_comprehensive_pdf(cdd_data, output_path):
    """
    Create comprehensive PDF documentation from CDD data
    
    Args:
        cdd_data (dict): Parsed CDD data with services and DIDs
        output_path (str): Path where PDF should be saved
        
    Returns:
        str: Path to generated PDF file
    """
    converter = ComprehensivePDFConverter()
    return converter.convert_to_pdf(cdd_data, output_path)

if __name__ == "__main__":
    # Test data structure
    test_data = {
        'name': 'NX3_UDS_CanIfCfg',
        'source_file': 'NX3_UDS_CanIfCfg.cdd',
        'services': [
            {'name': 'DiagnosticSessionControl', 'service_id': 0x10, 'description': 'Control diagnostic sessions'},
            {'name': 'ReadDataByIdentifier', 'service_id': 0x22, 'description': 'Read data identifiers'},
        ],
        'dids': [
            {'name': 'DID_SwtH2OComp', 'did_id': 0xFE90, 'description': 'Software H2O compensation'},
            {'name': 'DID_CorrnNH3Fac', 'did_id': 0xFE28, 'description': 'Correction NH3 factor'},
        ]
    }
    
    create_comprehensive_pdf(test_data, 'test_output.pdf')
    print("Test PDF generated successfully!")