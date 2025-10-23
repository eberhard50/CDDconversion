import xml.etree.ElementTree as ET
from typing import Dict, List, Set
from collections import defaultdict

class CDDAnalyzer:
    def __init__(self):
        self.tag_counts = defaultdict(int)
        self.unique_tags = set()
        self.diagnostic_tags = set()
        
    def analyze_structure(self, file_path: str) -> Dict:
        """Analyze CDD file structure and identify key elements"""
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Get all unique tags in the document
        self._collect_tags(root)
        
        # Look for diagnostic-specific elements
        diagnostic_elements = self._find_diagnostic_elements(root)
        
        # Analyze namespace
        namespace_info = self._analyze_namespace(root)
        
        return {
            'namespace': namespace_info,
            'total_tags': len(self.unique_tags),
            'tag_frequency': dict(self.tag_counts),
            'diagnostic_elements': diagnostic_elements,
            'potential_services': self._find_potential_services(root),
            'potential_dids': self._find_potential_dids(root),
            'communication_elements': self._find_communication_elements(root)
        }
    
    def _collect_tags(self, element):
        """Recursively collect all tag names"""
        tag_name = element.tag.split('}')[-1] if '}' in element.tag else element.tag
        self.unique_tags.add(tag_name)
        self.tag_counts[tag_name] += 1
        
        for child in element:
            self._collect_tags(child)
    
    def _analyze_namespace(self, root) -> Dict:
        """Extract namespace information"""
        namespace_info = {}
        if root.tag.startswith('{'):
            namespace_info['uri'] = root.tag.split('}')[0][1:]
            namespace_info['tag'] = root.tag.split('}')[1]
        else:
            namespace_info['uri'] = None
            namespace_info['tag'] = root.tag
            
        # Get all namespace declarations
        namespace_info['declarations'] = {}
        for key, value in root.attrib.items():
            if key.startswith('xmlns'):
                namespace_info['declarations'][key] = value
                
        return namespace_info
    
    def _find_diagnostic_elements(self, root) -> List[Dict]:
        """Find elements that might contain diagnostic information"""
        diagnostic_keywords = [
            'service', 'diagnostic', 'did', 'pid', 'dtc', 'request', 'response',
            'communication', 'timing', 'security', 'session', 'identifier', 'data'
        ]
        
        found_elements = []
        
        def search_element(elem, path=""):
            tag_name = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
            current_path = f"{path}/{tag_name}" if path else tag_name
            
            # Check if tag contains diagnostic keywords
            for keyword in diagnostic_keywords:
                if keyword.lower() in tag_name.lower():
                    found_elements.append({
                        'tag': tag_name,
                        'path': current_path,
                        'attributes': dict(elem.attrib),
                        'has_text': bool(elem.text and elem.text.strip()),
                        'children_count': len(list(elem)),
                        'text_preview': elem.text[:100] if elem.text else None
                    })
                    break
            
            for child in elem:
                search_element(child, current_path)
        
        search_element(root)
        return found_elements
    
    def _find_potential_services(self, root) -> List[Dict]:
        """Look for potential service definitions"""
        service_patterns = [
            'SERVICE', 'DiagnosticService', 'DIAGNOSTIC-SERVICE',
            'UDSService', 'REQUEST', 'RESPONSE', 'SERVICES'
        ]
        
        services = []
        for pattern in service_patterns:
            # Try case-sensitive first
            elements = root.findall(f".//{pattern}")
            # Then try lowercase
            if not elements:
                elements = root.findall(f".//{pattern.lower()}")
            
            for elem in elements:
                services.append({
                    'tag': elem.tag,
                    'attributes': dict(elem.attrib),
                    'children': [child.tag for child in elem[:5]],  # First 5 children
                    'text_preview': elem.text[:50] if elem.text else None
                })
        
        return services
    
    def _find_potential_dids(self, root) -> List[Dict]:
        """Look for potential DID definitions"""
        did_patterns = [
            'DID', 'DataIdentifier', 'DATA-IDENTIFIER', 'PID', 'DATAOBJ'
        ]
        
        dids = []
        for pattern in did_patterns:
            # Try case-sensitive first
            elements = root.findall(f".//{pattern}")
            # Then try lowercase
            if not elements:
                elements = root.findall(f".//{pattern.lower()}")
            
            for elem in elements:
                dids.append({
                    'tag': elem.tag,
                    'attributes': dict(elem.attrib),
                    'text': elem.text[:50] if elem.text else None,
                    'children': [child.tag for child in elem[:5]]
                })
        
        return dids
    
    def _find_communication_elements(self, root) -> List[Dict]:
        """Look for communication parameter definitions"""
        comm_patterns = [
            'Communication', 'COMMUNICATION', 'Timing', 'TIMING',
            'CanId', 'CAN-ID', 'Transport', 'TRANSPORT', 'PROTOCOL'
        ]
        
        comm_elements = []
        for pattern in comm_patterns:
            # Try case-sensitive first
            elements = root.findall(f".//{pattern}")
            # Then try lowercase
            if not elements:
                elements = root.findall(f".//{pattern.lower()}")
            
            for elem in elements:
                comm_elements.append({
                    'tag': elem.tag,
                    'attributes': dict(elem.attrib),
                    'children': [child.tag for child in elem[:5]],
                    'text_preview': elem.text[:50] if elem.text else None
                })
        
        return comm_elements

def analyze_cdd_file(file_path: str):
    """Analyze a CDD file and print structure information"""
    try:
        analyzer = CDDAnalyzer()
        results = analyzer.analyze_structure(file_path)
        
        print("=== CDD File Analysis ===")
        print(f"File: {file_path}")
        print(f"Namespace: {results['namespace']}")
        print(f"Total unique tags: {results['total_tags']}")
        
        print("\n=== Most Common Tags (Top 20) ===")
        sorted_tags = sorted(results['tag_frequency'].items(), key=lambda x: x[1], reverse=True)
        for tag, count in sorted_tags[:20]:
            print(f"  {tag}: {count}")
        
        print("\n=== Potential Diagnostic Elements ===")
        if results['diagnostic_elements']:
            for elem in results['diagnostic_elements'][:10]:
                print(f"  {elem['path']}")
                print(f"    Attributes: {elem['attributes']}")
                if elem['text_preview']:
                    print(f"    Text: {elem['text_preview']}")
                print()
        else:
            print("  No diagnostic elements found with standard keywords")
        
        print("=== Potential Services ===")
        if results['potential_services']:
            for service in results['potential_services'][:5]:
                print(f"  {service['tag']} - {service['attributes']}")
                print(f"    Children: {service['children']}")
        else:
            print("  No service elements found with standard patterns")
        
        print("\n=== Potential DIDs ===")
        if results['potential_dids']:
            for did in results['potential_dids'][:5]:
                print(f"  {did['tag']} - {did.get('text', 'No text')}")
                print(f"    Attributes: {did['attributes']}")
        else:
            print("  No DID elements found with standard patterns")
        
        print("\n=== Communication Elements ===")
        if results['communication_elements']:
            for comm in results['communication_elements'][:5]:
                print(f"  {comm['tag']} - {comm['attributes']}")
        else:
            print("  No communication elements found with standard patterns")
            
        return results
        
    except Exception as e:
        print(f"Error analyzing file: {e}")
        return None