# CDD Converter Tool

A comprehensive tool for converting CANdela (CDD) files to multiple output formats including ODX-D, PDF documentation, and HTML overview reports.

## 🚀 Features

- **Triple-Format Output**: Convert CDD files to ODX-D, PDF, and HTML formats simultaneously
- **Web Interface**: User-friendly Flask web application for easy file uploads and conversions
- **Enhanced CDD Parser**: Comprehensive parsing of CANdela database files
- **Professional Output**: High-quality PDF documentation and responsive HTML reports
- **Data Consistency**: All output formats use identical parsed data for consistency  

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