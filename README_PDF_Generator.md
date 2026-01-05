# CSV Prep - PDF Generator Documentation

## 📚 Overview

This automated PDF generator creates a **professional, colored, A4-formatted PDF book** from all markdown files in the repository. The generated PDF includes:

- ✅ **A4 Paper Format** - Properly formatted for international standard paper size
- 🎨 **Professional Styling** - Colored headings, tables, and code blocks
- 📊 **Mermaid Diagram Support** - Automatic rendering of Mermaid diagrams as visual graphics
- 🔍 **Table of Contents** - Auto-generated with clickable links
- 📄 **Source File Markers** - Shows which file each section came from
- 🔄 **Auto-Discovery** - Automatically finds all .md files (no hardcoded list!)

## 🚀 Quick Start

### Generate PDF (Simple)

```bash
python3 generate_pdf.py
```

That's it! The script will:
1. 🔍 Auto-discover all `.md` files in the current directory
2. 📚 Combine them into a single document
3. 🎨 Apply professional styling
4. 📊 Render Mermaid diagrams
5. 📄 Create `CSV_Prep_Complete_Documentation.pdf` in A4 format

## 📋 Features in Detail

### 1. **Auto-Discovery of Files**
- No need to maintain a hardcoded list of files
- Automatically finds all `.md` files in the repository
- Smart sorting: numbered files first (01, 02, ...), then alphabetical

### 2. **A4 Format**
- Page size: 210mm × 297mm (A4)
- Proper margins: Top/Bottom 20mm, Left/Right 15mm
- High-quality: 300 DPI output

### 3. **Professional Styling**
- **Colored headings**: Blue/Navy gradient for H1/H2
- **Styled tables**: Gradient headers, alternating row colors
- **Code blocks**: Dark theme with syntax highlighting
- **Blockquotes**: Styled with left border and background
- **Links**: Colored and interactive

### 4. **Mermaid Diagram Rendering**
- Mermaid code blocks are automatically rendered as diagrams
- Supports flowcharts, sequence diagrams, class diagrams, etc.
- Example:
  ````markdown
  ```mermaid
  graph TD
      A[Start] --> B[Process]
      B --> C[End]
  ```
  ````

### 5. **Source File Tracking**
- Each section shows which `.md` file it came from
- Helpful for maintenance and updates

## 🔧 Requirements

The script requires the following tools (already installed):
- Python 3.x
- `pandoc` - For markdown to HTML conversion
- `wkhtmltopdf` - For HTML to PDF conversion

## 📁 Files in This System

| File | Purpose |
|------|---------|
| `generate_pdf.py` | Main PDF generation script |
| `pdf_styles.css` | Professional styling for the PDF |
| `CSV_Prep_Complete_Documentation.pdf` | Generated PDF output |
| `README_PDF_Generator.md` | This documentation file |

## 🔄 Updating the PDF

### When You Add New Markdown Files

Simply add your new `.md` file to the repository and run:

```bash
python3 generate_pdf.py
```

The script will automatically:
- Detect the new file
- Include it in the PDF
- Maintain proper sorting
- Update the table of contents

**No code changes needed!** 🎉

### When You Update Existing Files

Just run the script again:

```bash
python3 generate_pdf.py
```

The PDF will be regenerated with your latest changes.

## 🎨 Customizing Styling

To customize the PDF appearance, edit `pdf_styles.css`:

### Change Colors
```css
:root {
    --primary-color: #2c3e50;      /* Main headings */
    --secondary-color: #3498db;     /* Subheadings */
    --accent-color: #e74c3c;        /* Highlights */
    --success-color: #27ae60;       /* Success elements */
    --warning-color: #f39c12;       /* Warnings */
}
```

### Change Fonts
```css
body {
    font-family: 'Your Font', sans-serif;
}
```

### Change Page Margins
Edit in `generate_pdf.py`:
```python
'--margin-top', '25mm',     # Adjust as needed
'--margin-bottom', '25mm',
'--margin-left', '20mm',
'--margin-right', '20mm',
```

## 🐛 Troubleshooting

### PDF is Too Large
- The PDF size depends on content (current: ~10MB)
- Consider splitting into multiple PDFs if needed
- Images and diagrams increase file size

### Mermaid Diagrams Not Rendering
- Ensure you're using proper Mermaid syntax
- Check that code blocks are marked as ` ```mermaid `
- The script adds a 2-second JavaScript delay for rendering

### Missing Files in PDF
- Check that your `.md` files are in the same directory as the script
- Verify file permissions (should be readable)

## 🔐 Automation Ideas

### Auto-Generate on Commit (Git Hook)
Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
python3 generate_pdf.py
git add CSV_Prep_Complete_Documentation.pdf
```

### Scheduled Generation (Cron)
```bash
# Generate PDF daily at 2 AM
0 2 * * * cd /path/to/CSV-Prep && python3 generate_pdf.py
```

## 📊 Output Details

The generated PDF includes:

1. **Title Page** - Professional cover with title, subtitle, and generation date
2. **Table of Contents** - Auto-generated with 3 levels of depth
3. **Content Sections** - All your markdown files combined
4. **Source Markers** - Shows origin file for each section

## 💡 Tips & Best Practices

1. **Keep Markdown Clean**: Use proper markdown syntax for best results
2. **Test Mermaid Locally**: Verify diagrams before generating PDF
3. **Regular Updates**: Run the script after major content changes
4. **Version Control**: Commit both the script and generated PDF
5. **Backup**: Keep the old PDF before regenerating (just in case)

## 🎯 What Makes This Flexible?

✅ **No hardcoded file list** - Auto-discovers files
✅ **Smart sorting** - Handles numbered and named files
✅ **Extensible** - Easy to modify and customize
✅ **Self-contained** - All dependencies clearly documented
✅ **Reproducible** - Same input always produces same output

## 📞 Support

If you encounter issues:
1. Check that all requirements are installed
2. Verify your markdown syntax
3. Review the console output for errors
4. Check file permissions

## 🎓 Example Workflow

```bash
# 1. Add a new markdown file
echo "# My New Guide" > New_Guide.md

# 2. Generate updated PDF
python3 generate_pdf.py

# 3. Verify the PDF
ls -lh CSV_Prep_Complete_Documentation.pdf

# 4. Commit changes
git add New_Guide.md CSV_Prep_Complete_Documentation.pdf
git commit -m "Add new guide and update PDF"
git push
```

---

**Generated by:** CSV Prep PDF Generator v2.0
**Last Updated:** January 2026
**Maintained by:** Auto-discovery system - Just add files and run!
