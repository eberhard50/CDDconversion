#!/usr/bin/env python3
"""
Enhanced CDD Parser - Comprehensive extraction of all CDD diagnostic information
Extracts complete information for full ODX-D conversion
"""

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import re


@dataclass
class CDDComponent:
    """Represents a component in a service request/response"""
    id: str
    name: str
    qualifier: str
    description: str = ""
    component_type: str = ""  # CONSTCOMP, STATICCOMP, etc.
    must: bool = False
    spec: str = ""
    bit_length: str = ""
    value: str = ""
    data_type_ref: str = ""


@dataclass
class CDDServiceMessage:
    """Represents a service request, positive response, or negative response"""
    id: str
    name: str
    qualifier: str
    components: List[CDDComponent] = field(default_factory=list)


@dataclass
class CDDProtocolService:
    """Represents a complete UDS protocol service"""
    id: str
    name: str
    qualifier: str
    description: str = ""
    uds_service_id: Optional[int] = None  # The actual UDS service ID (0x10, 0x22, etc.)
    func: bool = False
    phys: bool = False
    multiple_response: bool = False
    response_on_physical: bool = False
    response_on_functional: bool = False
    request: Optional[CDDServiceMessage] = None
    positive_response: Optional[CDDServiceMessage] = None
    negative_response: Optional[CDDServiceMessage] = None


@dataclass
class CDDDataObject:
    """Represents a data object within a DID structure"""
    id: str
    name: str
    qualifier: str
    description: str = ""
    data_type_ref: str = ""
    spec: str = ""


@dataclass
class CDDDID:
    """Represents a Data Identifier"""
    id: str
    number: int  # DID number (e.g., 65168)
    number_hex: str  # DID in hex (e.g., 0xFE90)
    name: str
    qualifier: str
    description: str = ""
    data_objects: List[CDDDataObject] = field(default_factory=list)


@dataclass
class CDDCommunicationParams:
    """Represents communication parameters"""
    physical_request_id: str = ""
    physical_response_id: str = ""
    functional_request_id: str = ""
    addressing_scheme: str = ""
    can_id_type: str = ""


@dataclass
class CDDDocument:
    """Complete CDD document representation"""
    ecu_name: str = ""
    manufacturer: str = ""
    version: str = ""
    protocol_services: List[CDDProtocolService] = field(default_factory=list)
    dids: List[CDDDID] = field(default_factory=list)
    communication_params: CDDCommunicationParams = field(default_factory=CDDCommunicationParams)
    


class EnhancedCDDParser:
    """Enhanced parser for comprehensive CDD file analysis"""
    
    def __init__(self):
        self.document = CDDDocument()
        self.namespaces = {}
    
    def parse_file(self, file_path: str) -> CDDDocument:
        """Parse CDD file and extract all diagnostic information"""
        print(f"📖 Parsing CDD file: {file_path}")
        
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Register XML namespace
            ET.register_namespace('', '')  # Default namespace
            
            # Extract basic document info
            self._extract_document_info(root)
            
            # Extract communication parameters
            self._extract_communication_params(root)
            
            # Extract DIDs
            self._extract_dids(root)
            
            # Extract protocol services
            self._extract_protocol_services(root)
            
            print(f"✅ Parsing complete:")
            print(f"   📋 Services: {len(self.document.protocol_services)}")
            print(f"   🔢 DIDs: {len(self.document.dids)}")
            
            return self.document
            
        except Exception as e:
            print(f"❌ Error parsing CDD file: {e}")
            raise
    
    def _extract_document_info(self, root):
        """Extract basic document information"""
        # Try to find ECUDOC element
        ecudoc = root.find('.//ECUDOC')
        if ecudoc is not None:
            self.document.manufacturer = ecudoc.get('manufacturer', 'Unknown')
            
        # Try to extract ECU name from filename or content
        # This will be set by the calling code based on filename
        
    def _extract_communication_params(self, root):
        """Extract communication parameters (CAN IDs, etc.)"""
        try:
            # Look for request/response CAN IDs in the document
            # These are typically in COMMPARAMSET or similar structures
            comm_params = CDDCommunicationParams()
            
            # Search for common CAN ID patterns
            for elem in root.iter():
                if elem.text and 'CAN-ID' in elem.get('xml:lang', ''):
                    # Extract CAN ID information
                    pass
                    
            self.document.communication_params = comm_params
            
        except Exception as e:
            print(f"⚠️ Warning: Could not extract communication parameters: {e}")
    
    def _extract_dids(self, root):
        """Extract all Data Identifiers (DIDs)"""
        try:
            dids_section = root.find('.//DIDS')
            if dids_section is None:
                print("⚠️ No DIDS section found")
                return
            
            did_count = 0
            for did_elem in dids_section.findall('DID'):
                did = self._parse_did(did_elem)
                if did:
                    self.document.dids.append(did)
                    did_count += 1
            
            print(f"📊 Extracted {did_count} DIDs")
            
        except Exception as e:
            print(f"❌ Error extracting DIDs: {e}")
    
    def _parse_did(self, did_elem) -> Optional[CDDDID]:
        """Parse a single DID element"""
        try:
            did_id = did_elem.get('id', '')
            did_number = int(did_elem.get('n', '0'))
            did_hex = f"0x{did_number:04X}"
            
            # Extract name
            name_elem = did_elem.find('NAME/TUV')
            if name_elem is None:
                # Try without namespace
                name_elems = did_elem.findall('.//TUV')
                name_elem = next((elem for elem in name_elems if 'xml:lang' not in elem.attrib or elem.get('{http://www.w3.org/XML/1998/namespace}lang') == 'en-US'), name_elems[0] if name_elems else None)
            name = name_elem.text if name_elem is not None else f"DID_{did_hex}"
            
            # Extract qualifier
            qual_elem = did_elem.find('QUAL')
            qualifier = qual_elem.text if qual_elem is not None else name
            
            # Extract description
            desc_elem = did_elem.find('DESC/TUV')
            if desc_elem is None:
                # Try to find any TUV in DESC
                desc_elems = did_elem.findall('.//DESC//TUV')
                desc_elem = desc_elems[0] if desc_elems else None
            description = desc_elem.text if desc_elem is not None else ""
            
            # Extract data objects
            data_objects = []
            structure_elem = did_elem.find('STRUCTURE')
            if structure_elem is not None:
                for dataobj_elem in structure_elem.findall('.//DATAOBJ'):
                    data_obj = self._parse_data_object(dataobj_elem)
                    if data_obj:
                        data_objects.append(data_obj)
            
            return CDDDID(
                id=did_id,
                number=did_number,
                number_hex=did_hex,
                name=name,
                qualifier=qualifier,
                description=description,
                data_objects=data_objects
            )
            
        except Exception as e:
            print(f"⚠️ Error parsing DID: {e}")
            return None
    
    def _parse_data_object(self, dataobj_elem) -> Optional[CDDDataObject]:
        """Parse a data object within a DID"""
        try:
            obj_id = dataobj_elem.get('id', '')
            
            # Extract name
            name_elem = dataobj_elem.find('NAME/TUV')
            if name_elem is None:
                name_elems = dataobj_elem.findall('.//TUV')
                name_elem = name_elems[0] if name_elems else None
            name = name_elem.text if name_elem is not None else "DataObject"
            
            # Extract qualifier
            qual_elem = dataobj_elem.find('QUAL')
            qualifier = qual_elem.text if qual_elem is not None else name
            
            # Extract data type reference
            dtref = dataobj_elem.get('dtref', '')
            spec = dataobj_elem.get('spec', '')
            
            return CDDDataObject(
                id=obj_id,
                name=name,
                qualifier=qualifier,
                data_type_ref=dtref,
                spec=spec
            )
            
        except Exception as e:
            print(f"⚠️ Error parsing data object: {e}")
            return None
    
    def _extract_protocol_services(self, root):
        """Extract all protocol services (UDS services)"""
        try:
            services_section = root.find('.//PROTOCOLSERVICES')
            if services_section is None:
                print("⚠️ No PROTOCOLSERVICES section found")
                return
            
            service_count = 0
            for service_elem in services_section.findall('PROTOCOLSERVICE'):
                service = self._parse_protocol_service(service_elem)
                if service:
                    self.document.protocol_services.append(service)
                    service_count += 1
            
            print(f"🔧 Extracted {service_count} protocol services")
            
        except Exception as e:
            print(f"❌ Error extracting protocol services: {e}")
    
    def _parse_protocol_service(self, service_elem) -> Optional[CDDProtocolService]:
        """Parse a single protocol service"""
        try:
            service_id = service_elem.get('id', '')
            
            # Extract name
            name_elem = service_elem.find('NAME/TUV')
            if name_elem is None:
                name_elems = service_elem.findall('.//TUV')
                name_elem = name_elems[0] if name_elems else None
            name = name_elem.text if name_elem is not None else "Unknown Service"
            
            # Extract qualifier  
            qual_elem = service_elem.find('QUAL')
            qualifier = qual_elem.text if qual_elem is not None else ""
            
            # Extract description from NAME TUV or other description elements
            description = ""
            
            # First try to get description from DESC element
            desc_elem = service_elem.find('DESC/TUV')
            if desc_elem is not None and desc_elem.text:
                description = desc_elem.text
            elif name_elem is not None and name_elem.text:
                # Use name as fallback and enhance with standard UDS descriptions
                description = self._get_enhanced_service_description(name_elem.text, uds_service_id)
            else:
                description = "UDS diagnostic service"
            
            # Extract UDS service ID from SID component
            uds_service_id = None
            sid_component = service_elem.find(".//CONSTCOMP[@spec='sid']")
            if sid_component is not None:
                sid_value = sid_component.get('v', '')
                if sid_value:
                    try:
                        uds_service_id = int(sid_value)
                    except ValueError:
                        pass
            
            # Extract service attributes
            func = service_elem.get('func') == '1'
            phys = service_elem.get('phys') == '1'
            mresp = service_elem.get('mresp') == '1'
            resp_on_phys = service_elem.get('respOnPhys') == '1'
            resp_on_func = service_elem.get('respOnFunc') == '1'
            
            # Parse request
            request = None
            req_elem = service_elem.find('REQ')
            if req_elem is not None:
                request = self._parse_service_message(req_elem)
            
            # Parse positive response
            positive_response = None
            pos_elem = service_elem.find('POS')
            if pos_elem is not None:
                positive_response = self._parse_service_message(pos_elem)
            
            # Parse negative response
            negative_response = None
            neg_elem = service_elem.find('NEG')
            if neg_elem is not None:
                negative_response = self._parse_service_message(neg_elem)
            
            return CDDProtocolService(
                id=service_id,
                name=name,
                qualifier=qualifier,
                description=description,
                uds_service_id=uds_service_id,
                func=func,
                phys=phys,
                multiple_response=mresp,
                response_on_physical=resp_on_phys,
                response_on_functional=resp_on_func,
                request=request,
                positive_response=positive_response,
                negative_response=negative_response
            )
            
        except Exception as e:
            print(f"❌ Error parsing protocol service: {e}")
            return None
    
    def _get_enhanced_service_description(self, service_name: str, uds_service_id: Optional[int]) -> str:
        """Generate enhanced service description based on UDS service ID and name"""
        
        # Standard UDS service descriptions
        uds_descriptions = {
            0x10: "Controls diagnostic session state. Allows switching between different diagnostic sessions (default, programming, extended) with different access levels and timeouts.",
            0x11: "Performs ECU reset operations. Supports hard reset, key-off-on reset, and soft reset to restart ECU functionality.",
            0x14: "Clears diagnostic trouble codes (DTCs) and their associated status information from ECU memory.",
            0x19: "Reads diagnostic trouble codes (DTCs) with various subfunctions for different DTC formats and status masks.",
            0x22: "Reads data from ECU memory using Data Identifiers (DIDs). Provides access to real-time data, configuration parameters, and diagnostic information.",
            0x23: "Reads data from ECU memory by specifying memory address and size. Direct memory access for diagnostic purposes.",
            0x24: "Reads scaling information for data identifiers to convert raw values to physical units.",
            0x27: "Provides security access to protected diagnostic functions. Uses seed-key mechanism for authentication.",
            0x28: "Controls communication with ECU. Can disable/enable normal communication and network management.",
            0x2A: "Reads data with periodic transmission. Sets up cyclic data transmission from ECU to tester.",
            0x2C: "Dynamically defines data identifiers by memory address. Creates custom DIDs for specific memory locations.",
            0x2E: "Writes data to ECU memory using Data Identifiers (DIDs). Allows modification of configuration parameters and calibration data.",
            0x2F: "Controls input/output operations. Can force specific states on ECU inputs and outputs for testing purposes.",
            0x31: "Executes diagnostic routines. Starts, stops, and requests results from various diagnostic procedures.",
            0x34: "Initiates download of data to ECU memory. Requests memory allocation for data transfer operations.",
            0x35: "Initiates upload of data from ECU memory. Requests memory allocation for data retrieval operations.",
            0x36: "Transfers data blocks to ECU during download operations. Continues data transfer started with RequestDownload.",
            0x37: "Transfers data blocks from ECU during upload operations. Continues data transfer started with RequestUpload.",
            0x38: "Completes data transfer operations. Finalizes download/upload and verifies data integrity.",
            0x3D: "Writes data to ECU memory by specifying memory address and size. Direct memory write access for diagnostic purposes.",
            0x3E: "Maintains active diagnostic session. Prevents timeout of current diagnostic session through periodic transmission.",
            0x83: "Provides access to diagnostic data related to communication and network management.",
            0x84: "Controls network management and communication flow within the vehicle network.",
            0x85: "Manages diagnostic communication timing parameters and session behavior.",
            0x86: "Controls response behavior for diagnostic requests in functional and physical addressing modes.",
            0x87: "Provides access to vehicle identification and diagnostic capabilities information."
        }
        
        # Get description by UDS service ID if available
        if uds_service_id in uds_descriptions:
            return uds_descriptions[uds_service_id]
        
        # Try to extract description from service name
        if service_name:
            if "DiagnosticSessionControl" in service_name:
                return uds_descriptions.get(0x10, "Controls diagnostic session state")
            elif "ECUReset" in service_name:
                return uds_descriptions.get(0x11, "Performs ECU reset operations")
            elif "ClearDiagnosticInformation" in service_name:
                return uds_descriptions.get(0x14, "Clears diagnostic trouble codes")
            elif "ReadDTCInformation" in service_name:
                return uds_descriptions.get(0x19, "Reads diagnostic trouble codes")
            elif "ReadDataByIdentifier" in service_name:
                return uds_descriptions.get(0x22, "Reads data using Data Identifiers")
            elif "ReadMemoryByAddress" in service_name:
                return uds_descriptions.get(0x23, "Reads data by memory address")
            elif "SecurityAccess" in service_name:
                return uds_descriptions.get(0x27, "Provides security access control")
            elif "CommunicationControl" in service_name:
                return uds_descriptions.get(0x28, "Controls ECU communication")
            elif "WriteDataByIdentifier" in service_name:
                return uds_descriptions.get(0x2E, "Writes data using Data Identifiers")
            elif "InputOutputControlByIdentifier" in service_name:
                return uds_descriptions.get(0x2F, "Controls input/output operations")
            elif "RoutineControl" in service_name:
                return uds_descriptions.get(0x31, "Executes diagnostic routines")
            elif "RequestDownload" in service_name:
                return uds_descriptions.get(0x34, "Initiates data download to ECU")
            elif "RequestUpload" in service_name:
                return uds_descriptions.get(0x35, "Initiates data upload from ECU")
            elif "TransferData" in service_name:
                return "Transfers data blocks between tester and ECU during download/upload operations"
            elif "RequestTransferExit" in service_name:
                return uds_descriptions.get(0x38, "Completes data transfer operations")
            elif "WriteMemoryByAddress" in service_name:
                return uds_descriptions.get(0x3D, "Writes data by memory address")
            elif "TesterPresent" in service_name:
                return uds_descriptions.get(0x3E, "Maintains active diagnostic session")
        
        return f"UDS diagnostic service providing {service_name} functionality according to ISO 14229-1 specification."
    
    def _parse_service_message(self, msg_elem) -> Optional[CDDServiceMessage]:
        """Parse a service message (request/response)"""
        try:
            msg_id = msg_elem.get('id', '')
            
            # Extract name
            name_elem = msg_elem.find('NAME/TUV')
            if name_elem is None:
                name_elems = msg_elem.findall('.//TUV')
                name_elem = name_elems[0] if name_elems else None
            name = name_elem.text if name_elem is not None else "Message"
            
            # Extract qualifier
            qual_elem = msg_elem.find('QUAL')
            qualifier = qual_elem.text if qual_elem is not None else ""
            
            # Parse components
            components = []
            
            # Parse CONSTCOMP elements
            for comp_elem in msg_elem.findall('.//CONSTCOMP'):
                component = self._parse_component(comp_elem, 'CONSTCOMP')
                if component:
                    components.append(component)
            
            # Parse STATICCOMP elements
            for comp_elem in msg_elem.findall('.//STATICCOMP'):
                component = self._parse_component(comp_elem, 'STATICCOMP')
                if component:
                    components.append(component)
            
            # Parse SIMPLEPROXYCOMP elements
            for comp_elem in msg_elem.findall('.//SIMPLEPROXYCOMP'):
                component = self._parse_component(comp_elem, 'SIMPLEPROXYCOMP')
                if component:
                    components.append(component)
            
            return CDDServiceMessage(
                id=msg_id,
                name=name,
                qualifier=qualifier,
                components=components
            )
            
        except Exception as e:
            print(f"⚠️ Error parsing service message: {e}")
            return None
    
    def _parse_component(self, comp_elem, comp_type: str) -> Optional[CDDComponent]:
        """Parse a service component"""
        try:
            comp_id = comp_elem.get('id', '')
            
            # Extract name
            name_elem = comp_elem.find('NAME/TUV')
            if name_elem is None:
                name_elems = comp_elem.findall('.//TUV')
                name_elem = name_elems[0] if name_elems else None
            name = name_elem.text if name_elem is not None else "Component"
            
            # Extract qualifier
            qual_elem = comp_elem.find('QUAL')
            qualifier = qual_elem.text if qual_elem is not None else ""
            
            # Extract attributes
            must = comp_elem.get('must') == '1'
            spec = comp_elem.get('spec', '')
            bit_length = comp_elem.get('bl', '')
            value = comp_elem.get('v', '')
            dtref = comp_elem.get('dtref', '')
            
            return CDDComponent(
                id=comp_id,
                name=name,
                qualifier=qualifier,
                component_type=comp_type,
                must=must,
                spec=spec,
                bit_length=bit_length,
                value=value,
                data_type_ref=dtref
            )
            
        except Exception as e:
            print(f"⚠️ Error parsing component: {e}")
            return None


def test_enhanced_parser():
    """Test function for the enhanced parser"""
    parser = EnhancedCDDParser()
    
    # Test with the actual CDD file
    cdd_file = "NX3_UDS_CanIfCfg.cdd"
    document = parser.parse_file(cdd_file)
    
    print("\n📋 CDD Analysis Summary:")
    print(f"ECU: {document.ecu_name}")
    print(f"Manufacturer: {document.manufacturer}")
    print(f"Services: {len(document.protocol_services)}")
    print(f"DIDs: {len(document.dids)}")
    
    # Show first few services
    print("\n🔧 First 5 Services:")
    for i, service in enumerate(document.protocol_services[:5]):
        print(f"  {i+1}. {service.name} ({service.qualifier})")
        if service.request:
            print(f"     Request components: {len(service.request.components)}")
        if service.positive_response:
            print(f"     Response components: {len(service.positive_response.components)}")
    
    # Show first few DIDs
    print("\n🔢 First 5 DIDs:")
    for i, did in enumerate(document.dids[:5]):
        print(f"  {i+1}. {did.name} ({did.number_hex}) - {did.qualifier}")
        print(f"     Data objects: {len(did.data_objects)}")
    
    return document


if __name__ == "__main__":
    test_enhanced_parser()