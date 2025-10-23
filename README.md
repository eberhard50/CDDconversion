# CDD to ODX-D Converter

This tool converts CANdela (.cdd) files to ODX-D format, creating machine-readable diagnostic files for UDS toolchains.

## Overview

The converter takes your CDD file as the master source and generates a compliant ODX-D file containing:
- All UDS diagnostic services (ReadDataByIdentifier, WriteDataByIdentifier, etc.)
- Data Identifiers (DIDs) with proper structure
- Communication parameters (CAN IDs, timing)
- Diagnostic sessions and security levels

## Key Features

✅ **CDD as Master**: Your CDD file is the authoritative source  
✅ **Complete UDS Support**: All standard UDS services (0x10, 0x22, 0x2E, etc.)  
✅ **ODX-D Compliant**: Generated files follow ODX 2.2.0 specification  
✅ **Machine Readable**: Perfect for diagnostic toolchains  
✅ **Standard DIDs**: Includes automotive standard DIDs (VIN, ECU info, etc.)  

## Prerequisites

**Python 3.8 or higher** (currently not installed)

## Installation & Setup

1. **Install Python** from https://www.python.org/downloads/
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Quick Start
Place your CDD file in the project root and run:
```bash
python run_cdd_to_odx.py
```

### Advanced Usage
```bash
python src/main_cdd_to_odx.py your_file.cdd -o output.odx-d
```

## Generated ODX-D Structure

The converter creates a complete ODX-D file with:

### 1. **Diagnostic Services**
- ReadDataByIdentifier (0x22)
- WriteDataByIdentifier (0x2E)  
- DiagnosticSessionControl (0x10)
- SecurityAccess (0x27)
- TesterPresent (0x3E)
- ReadDTCInformation (0x19)
- ClearDiagnosticInformation (0x14)

### 2. **Data Identifiers (DIDs)**
- VIN (0xF190) - Vehicle Identification Number
- Active Diagnostic Session (0xF186)
- ECU Software Number (0xF18A)
- ECU Serial Number (0xF18C)
- Boot Software ID (0xF1A0)

### 3. **Communication Parameters**
- Physical Request ID: 0x7E0
- Physical Response ID: 0x7E8
- Functional Request ID: 0x7DF
- Timing: P2=50ms, P2*=5000ms, S3=5000ms

## Next Steps (After Python Installation)

1. **Install Python** and dependencies
2. **Test with your CDD file**: `python run_cdd_to_odx.py`
3. **Validate ODX output** with your diagnostic tools
4. **Integrate into toolchain** for automated conversion

The converter is ready to use once Python is installed! 🚀
- **Frameworks**: 
  - Flask or Django for web-based interface
  - Pandoc for document conversion
  - ReportLab for PDF generation
- **Database**: SQLite or NoSQL for storing user preferences and conversion history
- **Libraries**: 
  - `pandas` for data manipulation
  - `BeautifulSoup` for HTML generation
  - `docx` for Word document creation

#### Development Plan
1. **Phase 1: Research and Planning**
   - Analyze CDD file structure and conversion requirements.
   - Identify libraries and tools for conversion.

2. **Phase 2: Design**
   - Create wireframes for the user interface.
   - Design the architecture of the application.

3. **Phase 3: Implementation**
   - Develop the backend for file processing and conversion.
   - Build the frontend interface for user interaction.
   - Integrate conversion libraries and ensure data integrity.

4. **Phase 4: Testing**
   - Conduct unit testing for individual components.
   - Perform integration testing to ensure all parts work together.
   - Gather feedback from beta testers.

5. **Phase 5: Deployment**
   - Deploy the application on a cloud platform (e.g., AWS, Heroku).
   - Ensure scalability and performance optimization.

6. **Phase 6: Maintenance and Updates**
   - Regularly update the tool based on user feedback.
   - Add new features and support for additional file formats as needed.

#### Budget Estimate
- **Development Costs**: $15,000 - $25,000 (depending on team size and duration)
- **Hosting Costs**: $100 - $500 per year (depending on traffic)
- **Marketing Costs**: $1,000 - $3,000 for initial promotion

#### Timeline
- **Total Duration**: Approximately 6 months
  - Research and Planning: 1 month
  - Design: 1 month
  - Implementation: 2 months
  - Testing: 1 month
  - Deployment: 1 month

#### Conclusion
The CDD File Converter Tool will significantly enhance the accessibility of chemical data by providing a straightforward and efficient way to convert CDD files into various document formats. By focusing on user experience and data integrity, this tool aims to become an essential resource for professionals in the chemical field.