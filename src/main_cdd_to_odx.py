"""
CDD to ODX-D Converter

This module converts CANdela (.cdd) files to ODX-D format, preserving all UDS commands
and diagnostic information. The CDD file serves as the master source.
"""

import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional
from pathlib import Path
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.cdd_model import DiagnosticData
from parsers.cdd_parser import CDDParser
from converters.odx_converter import ODXTemplateGenerator, ODXDocument, ODXService, ODXDataIdentifier

class CDDToODXConverter:
    """Converts CDD files to ODX-D format"""
    
    def __init__(self):
        self.cdd_parser = CDDParser()
        self.odx_generator = ODXTemplateGenerator()
        
        # UDS Service ID mapping
        self.uds_services = {
            '0x10': 'DiagnosticSessionControl',
            '0x11': 'ECUReset',
            '0x14': 'ClearDiagnosticInformation',
            '0x19': 'ReadDTCInformation',
            '0x22': 'ReadDataByIdentifier',
            '0x23': 'ReadMemoryByAddress',
            '0x24': 'ReadScalingDataByIdentifier',
            '0x27': 'SecurityAccess',
            '0x28': 'CommunicationControl',
            '0x2A': 'ReadDataByPeriodicIdentifier',
            '0x2C': 'DynamicallyDefineDataIdentifier',
            '0x2E': 'WriteDataByIdentifier',
            '0x2F': 'InputOutputControlByIdentifier',
            '0x31': 'RoutineControl',
            '0x34': 'RequestDownload',
            '0x35': 'RequestUpload',
            '0x36': 'TransferData',
            '0x37': 'RequestTransferExit',
            '0x3D': 'WriteMemoryByAddress',
            '0x3E': 'TesterPresent',
            '0x83': 'AccessTimingParameter',
            '0x84': 'SecuredDataTransmission',
            '0x85': 'ControlDTCSetting',
            '0x86': 'ResponseOnEvent',
            '0x87': 'LinkControl'
        }
    
    def convert_cdd_to_odx(self, cdd_file_path: str, output_path: str = None) -> str:
        """
        Convert CDD file to ODX-D format
        
        Args:
            cdd_file_path: Path to input CDD file
            output_path: Path for output ODX-D file (optional)
            
        Returns:
            Generated ODX-D XML content
        """
        # Parse CDD file
        print(f"Parsing CDD file: {cdd_file_path}")
        diagnostic_data = self.cdd_parser.parse(cdd_file_path)
        
        # Extract ECU name from file
        ecu_name = Path(cdd_file_path).stem
        
        # Convert to ODX format
        odx_document = self._convert_diagnostic_data(diagnostic_data, ecu_name)
        
        # Generate ODX-D XML
        odx_xml = self.odx_generator.generate_odx_document(odx_document)
        
        # Save to file if output path provided
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(odx_xml)
            print(f"ODX-D file saved to: {output_path}")
        
        return odx_xml
    
    def _convert_diagnostic_data(self, data: DiagnosticData, ecu_name: str) -> ODXDocument:
        """Convert parsed CDD data to ODX document structure"""
        
        # Convert services
        odx_services = []
        for service in data.services:
            odx_service = self._convert_service(service)
            if odx_service:
                odx_services.append(odx_service)
        
        # Convert DIDs
        odx_dids = []
        for did in data.data_identifiers:
            odx_did = self._convert_data_identifier(did)
            if odx_did:
                odx_dids.append(odx_did)
        
        # Create ODX document
        return ODXDocument(
            services=odx_services,
            data_identifiers=odx_dids,
            communication_params=self._convert_communication_params(data.communication_params),
            ecu_name=ecu_name,
            version="1.0.0"
        )
    
    def _convert_service(self, service) -> Optional[ODXService]:
        """Convert CDD service to ODX service"""
        if not service.id or not service.name:
            return None
        
        # Normalize service ID
        service_id = self._normalize_service_id(service.id)
        service_name = self._get_service_name(service_id, service.name)
        
        # Convert request parameters
        request_params = []
        
        # Add service ID as first parameter
        request_params.append({
            "type": "ServiceId",
            "name": "ServiceId", 
            "value": service_id
        })
        
        # Add service-specific parameters
        for param in service.request_params:
            if param.get('type') == 'DataIdentifier':
                request_params.append({
                    "type": "DataIdentifier",
                    "name": "DID",
                    "value": param.get('value')
                })
        
        # Convert response parameters
        response_params = []
        
        # Add positive response service ID
        positive_response_id = self._get_positive_response_id(service_id)
        response_params.append({
            "type": "ServiceId",
            "name": "ServiceId",
            "value": positive_response_id
        })
        
        # Add response-specific parameters
        for param in service.response_params:
            if param.get('type') == 'DataIdentifier':
                response_params.append({
                    "type": "DataIdentifier", 
                    "name": "DID",
                    "value": param.get('value')
                })
                # Add data parameter for the DID content
                did_id = param.get('value', '').replace('0x', '')
                response_params.append({
                    "type": "Data",
                    "name": f"DID_{did_id}_Data",
                    "structure_ref": f"DOP.DID_{did_id}"
                })
        
        return ODXService(
            id=service_name.replace(' ', ''),
            name=service_name,
            service_id=service_id,
            request_params=request_params,
            response_params=response_params,
            description=service.description or f"{service_name} service"
        )
    
    def _convert_data_identifier(self, did) -> Optional[ODXDataIdentifier]:
        """Convert CDD DID to ODX data identifier"""
        if not did.identifier or not did.name:
            return None
        
        # Normalize DID identifier
        did_id = self._normalize_hex(did.identifier)
        did_name = did.name or f"DID_{did_id.replace('0x', '')}"
        
        # Determine data type and length
        data_type = did.encoding or "BYTEFIELD"
        length = did.length or 1
        
        return ODXDataIdentifier(
            id=f"DID_{did_id.replace('0x', '')}",
            identifier=did_id,
            name=did_name,
            description=did.description or f"Data Identifier {did_id}",
            data_type=data_type,
            length=length,
            structure=did.signals
        )
    
    def _convert_communication_params(self, comm_params) -> Dict:
        """Convert communication parameters"""
        if not comm_params:
            return {}
        
        return {
            "physical_request_id": comm_params.phys_req_id,
            "physical_response_id": comm_params.phys_res_id,
            "functional_request_id": comm_params.func_req_id,
            "p2_timeout": comm_params.p2_timeout,
            "p2_star_timeout": comm_params.p2_star_timeout,
            "s3_timeout": comm_params.s3_timeout
        }
    
    def _normalize_service_id(self, service_id: str) -> str:
        """Normalize service ID to standard hex format"""
        if not service_id:
            return "0x00"
        
        service_id = service_id.strip().upper()
        if not service_id.startswith('0X'):
            if all(c in '0123456789ABCDEF' for c in service_id):
                service_id = '0x' + service_id
        
        return service_id
    
    def _get_service_name(self, service_id: str, original_name: str) -> str:
        """Get standardized service name"""
        if service_id in self.uds_services:
            return self.uds_services[service_id]
        return original_name or f"Service_{service_id.replace('0x', '')}"
    
    def _get_positive_response_id(self, service_id: str) -> str:
        """Get positive response service ID (request + 0x40)"""
        try:
            request_id = int(service_id, 16)
            response_id = request_id + 0x40
            return f"0x{response_id:02X}"
        except:
            return "0x7F"  # Default negative response
    
    def _normalize_hex(self, value: str) -> str:
        """Normalize hexadecimal values"""
        if not value:
            return value
        
        value = value.strip().upper()
        if not value.startswith('0X'):
            if all(c in '0123456789ABCDEF' for c in value):
                value = '0x' + value
        
        return value

def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert CDD files to ODX-D format')
    parser.add_argument('input_file', help='Path to input CDD file')
    parser.add_argument('-o', '--output', help='Output ODX-D file path')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Create converter
    converter = CDDToODXConverter()
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        input_path = Path(args.input_file)
        output_path = input_path.parent / f"{input_path.stem}.odx-d"
    
    try:
        # Convert file
        odx_xml = converter.convert_cdd_to_odx(args.input_file, str(output_path))
        
        if args.verbose:
            print("Conversion completed successfully!")
            print(f"Input: {args.input_file}")
            print(f"Output: {output_path}")
            print(f"ODX-D content length: {len(odx_xml)} characters")
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())