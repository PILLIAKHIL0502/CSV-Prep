#!/usr/bin/env python3
"""
Enhanced PDF Generator for CSV-Prep Documentation
- Auto-discovers all .md files
- Renders Mermaid diagrams
- Professional A4 formatting with colors
- Flexible and maintainable
"""

import os
import glob
import subprocess
import re
from pathlib import Path
from datetime import datetime


def find_all_markdown_files():
    """
    Automatically discover all markdown files in the repository.
    Returns a sorted list of markdown files.
    """
    # Find all .md files in current directory
    md_files = glob.glob("*.md")

    # Sort files with priority to numbered files first, then alphabetically
    def sort_key(filename):
        # Extract leading numbers if present
        match = re.match(r'^(\d+)', filename)
        if match:
            return (0, int(match.group(1)), filename)
        else:
            return (1, 0, filename.lower())

    md_files.sort(key=sort_key)

    return md_files


def create_title_page():
    """Create a professional title page"""
    today = datetime.now().strftime("%B %d, %Y")

    title_content = f"""
<div class="title-page">

# CSV Prep - Complete Documentation

<div class="subtitle">
Comprehensive Interview Preparation & Technical Reference Guide
</div>

<div class="subtitle">
Quality Architect • Computer System Validation • GxP Compliance
</div>

<div class="metadata">
Generated: {today}<br>
Auto-compiled from all markdown documentation files
</div>

</div>

---

"""
    return title_content


def process_markdown_content(content, filename):
    """
    Process markdown content to enhance it for PDF generation.
    Adds source file markers and prepares mermaid diagrams.
    """
    # Add source file marker
    processed = f'<div class="source-file">📄 Source: {filename}</div>\n\n'
    processed += content

    return processed


def create_combined_markdown(md_files):
    """
    Combine all markdown files into a single document.
    """
    combined_md = "combined_documentation.md"

    print(f"\n📚 Combining {len(md_files)} markdown files...")

    with open(combined_md, 'w', encoding='utf-8') as outfile:
        # Add title page
        outfile.write(create_title_page())

        # Process each markdown file
        for i, md_file in enumerate(md_files, 1):
            if os.path.exists(md_file):
                print(f"  ✓ [{i}/{len(md_files)}] {md_file}")

                with open(md_file, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    processed_content = process_markdown_content(content, md_file)
                    outfile.write(processed_content)
                    outfile.write("\n\n---\n\n")
            else:
                print(f"  ⚠ [{i}/{len(md_files)}] {md_file} - NOT FOUND, skipping...")

    print(f"\n✓ Combined markdown saved: {combined_md}")
    return combined_md


def convert_to_html_with_mermaid(combined_md):
    """
    Convert markdown to HTML with mermaid.js support for diagram rendering.
    """
    html_file = "combined_documentation.html"

    print("\n🔄 Converting markdown to HTML...")

    try:
        # Convert using pandoc with our custom CSS
        subprocess.run([
            'pandoc',
            combined_md,
            '-o', html_file,
            '--standalone',
            '--toc',
            '--toc-depth=3',
            '--css=pdf_styles.css',
            '--metadata', 'title=CSV Prep - Complete Documentation',
            '--metadata', 'lang=en',
            '--highlight-style=tango'
        ], check=True)

        print(f"✓ HTML file created: {html_file}")

        # Inject mermaid.js into HTML for diagram rendering
        inject_mermaid_support(html_file)

        return html_file

    except subprocess.CalledProcessError as e:
        print(f"❌ Error converting to HTML: {e}")
        return None


def inject_mermaid_support(html_file):
    """
    Inject mermaid.js library and initialization script into HTML.
    """
    print("🎨 Adding Mermaid.js support for diagram rendering...")

    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Mermaid.js injection
    mermaid_script = """
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
        mermaid.initialize({
            startOnLoad: true,
            theme: 'default',
            securityLevel: 'loose',
            flowchart: {
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'basis'
            }
        });
    </script>
    <style>
        .mermaid {
            text-align: center;
            margin: 20px 0;
            padding: 15px;
            background-color: #fafafa;
            border: 2px solid #bdc3c7;
            border-radius: 8px;
        }
    </style>
"""

    # Inject before closing </head> tag
    html_content = html_content.replace('</head>', f'{mermaid_script}</head>')

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("✓ Mermaid.js support added")


def convert_html_to_pdf(html_file, pdf_file):
    """
    Convert HTML to PDF with A4 formatting and professional styling.
    """
    print("\n📄 Converting HTML to PDF with A4 formatting...")

    try:
        subprocess.run([
            'wkhtmltopdf',
            '--enable-local-file-access',
            '--page-size', 'A4',                    # A4 paper size
            '--margin-top', '20mm',
            '--margin-bottom', '20mm',
            '--margin-left', '15mm',
            '--margin-right', '15mm',
            '--encoding', 'UTF-8',
            '--enable-javascript',                   # Enable JS for Mermaid
            '--javascript-delay', '2000',            # Wait for Mermaid to render
            '--no-stop-slow-scripts',
            '--enable-internal-links',               # Enable TOC links
            '--enable-external-links',
            '--print-media-type',
            '--dpi', '300',                          # High quality
            html_file,
            pdf_file
        ], check=True)

        print(f"\n✅ PDF successfully created: {pdf_file}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Error converting to PDF: {e}")
        return False


def cleanup_intermediate_files(files_to_remove):
    """Clean up intermediate files"""
    print("\n🧹 Cleaning up intermediate files...")

    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"  ✓ Removed {file}")


def get_file_size(filepath):
    """Get human-readable file size"""
    size = os.path.getsize(filepath)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0


def main():
    """Main execution function"""

    print("=" * 70)
    print("  CSV-PREP DOCUMENTATION PDF GENERATOR")
    print("  Professional • Colored • A4 Format • Mermaid Support")
    print("=" * 70)

    # Step 1: Auto-discover all markdown files
    print("\n🔍 Step 1: Auto-discovering markdown files...")
    md_files = find_all_markdown_files()

    if not md_files:
        print("❌ No markdown files found!")
        return

    print(f"✓ Found {len(md_files)} markdown files")

    # Step 2: Combine markdown files
    print("\n📝 Step 2: Combining markdown files...")
    combined_md = create_combined_markdown(md_files)

    # Step 3: Convert to HTML with styling and Mermaid support
    print("\n🎨 Step 3: Converting to styled HTML...")
    html_file = convert_to_html_with_mermaid(combined_md)

    if not html_file:
        return

    # Step 4: Convert HTML to PDF (A4 format)
    print("\n📋 Step 4: Generating PDF (A4 format)...")
    pdf_file = "CSV_Prep_Complete_Documentation.pdf"

    success = convert_html_to_pdf(html_file, pdf_file)

    if not success:
        return

    # Step 5: Cleanup
    cleanup_intermediate_files([combined_md, html_file])

    # Final summary
    print("\n" + "=" * 70)
    print("✅ SUCCESS!")
    print("=" * 70)
    print(f"📚 Markdown files processed: {len(md_files)}")
    print(f"📄 PDF file: {pdf_file}")
    print(f"📊 File size: {get_file_size(pdf_file)}")
    print(f"📐 Format: A4 (210mm × 297mm)")
    print(f"🎨 Features: Professional styling, colored, Mermaid diagrams")
    print("=" * 70)
    print("\n💡 This script auto-discovers all .md files.")
    print("   Just add new .md files and run this script again!")
    print("=" * 70)


if __name__ == "__main__":
    main()
