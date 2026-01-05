#!/usr/bin/env python3
"""
Script to combine all markdown files and convert to PDF
"""
import os
import subprocess
from pathlib import Path

# List of all markdown files (in order)
md_files = [
    "01_Quality_Architect_Interview_Prep_Complete.md",
    "02_CSV_Interview_Advanced_Topics.md",
    "03_Strategic_Additions_and_Tools.md",
    "04_GxP_Testing_Part1_Fundamentals.md",
    "05_GxP_Testing_Part2_Selenium.md",
    "06_GxP_Testing_Part3_Playwright.md",
    "07_GxP_Testing_Part4_GitHub_Actions.md",
    "08_GxP_Testing_Part5-6_Reporting_RealWorld.md",
    "09_Quick_Reference_Card_Print_This.md",
    "Agile_Custom_Application_Complete_Guide.md",
    "CMC_Complete_Guide.md",
    "Critical_Thinking_Scenarios_Complete_Guide.md",
    "ERES_Compliance_Complete_Technical_Guide.md",
    "FMEA_QRM_Complete_Guide.md",
    "GxP_Testing_Automation_Guide_Part1.md",
    "GxP_Testing_Automation_Guide_Part2_Selenium.md",
    "GxP_Testing_Automation_Guide_Part3_Playwright.md",
    "GxP_Testing_Automation_Guide_Part4_GitHub_Actions.md",
    "GxP_Testing_Automation_Guide_Part5_6_Reporting_RealWorld.md",
    "GxP_Testing_Series_MASTER_INDEX.md",
    "ITSM_GRC_Complete_Guide.md",
    "MES_SAP_LIMS_Integration_Validation_Strategy.md",
    "MSAT_Complete_Guide.md",
    "MSAT_Learning_Guide_Beginner_to_Expert.md",
    "MSAT_Practice_Problems_with_Solutions.md",
    "ORGANIZED_STRUCTURE_GUIDE.md",
    "PARTS_4-10_COMPLETE_OUTLINE.md",
    "PAS-X_MES_Complete_Technical_Guide.md",
    "Part1_Hands_On_Coding_Practice_Guide.md",
    "Part2_Infrastructure_DevOps_Skills_Guide.md",
    "Part3_Security_Testing_Complete_Guide.md",
    "Part_01_Hands_On_Coding_Practice_Guide.md",
    "Part_02_Infrastructure_DevOps_Guide.md",
    "Part_03_Security_Testing_Complete_Guide.md",
    "Part_04-10_Complete_Outline_and_Examples.md",
    "PROGRESS_SUMMARY.md",
    "Project_1_SAP_Implementation_Complete_Guide.md",
    "Project_2_APMC_Complete_Guide.md",
    "Project_3_Go_Solo_Complete_Guide.md",
    "Quality_Architect_Interview_Prep_Guide.md",
    "QUICK_REFERENCE_CARD before interview.md",
    "Regulatory_Compliance_Complete_Debriefing.md",
    "SAP_S4HANA_Complete_Guide_Pharma_Manufacturing.md",
    "SAP_Terminology_Abbreviations_Complete_Reference.md",
    "Serialization_Track_Trace_Complete_Guide.md",
    "Strategic_Additions_And_Tools.md",
    "Syncade_MES_Complete_Technical_Guide.md",
    "TrackWise_QMS_Guide.md",
    "Veeva_Vault_QualityDocs_Guide.md"
]

def main():
    print("Starting PDF generation from markdown files...")

    # Create combined markdown file
    combined_md = "combined_documentation.md"

    print(f"Combining {len(md_files)} markdown files...")

    with open(combined_md, 'w', encoding='utf-8') as outfile:
        # Add title page
        outfile.write("# CSV Prep - Complete Documentation\n\n")
        outfile.write("---\n\n")

        for i, md_file in enumerate(md_files, 1):
            if os.path.exists(md_file):
                print(f"  [{i}/{len(md_files)}] Adding {md_file}")
                with open(md_file, 'r', encoding='utf-8') as infile:
                    outfile.write(f"\n\n<!-- Source: {md_file} -->\n\n")
                    outfile.write(infile.read())
                    outfile.write("\n\n---\n\n")
            else:
                print(f"  Warning: {md_file} not found, skipping...")

    print(f"\nCombined markdown saved to: {combined_md}")

    # Convert to HTML first
    print("\nConverting markdown to HTML...")
    html_file = "combined_documentation.html"

    try:
        subprocess.run([
            'pandoc',
            combined_md,
            '-o', html_file,
            '--standalone',
            '--toc',
            '--toc-depth=3',
            '--metadata', 'title=CSV Prep - Complete Documentation'
        ], check=True)
        print(f"HTML file created: {html_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting to HTML: {e}")
        return

    # Convert HTML to PDF
    print("\nConverting HTML to PDF...")
    pdf_file = "CSV_Prep_Complete_Documentation.pdf"

    try:
        subprocess.run([
            'wkhtmltopdf',
            '--enable-local-file-access',
            '--page-size', 'Letter',
            '--margin-top', '20mm',
            '--margin-bottom', '20mm',
            '--margin-left', '15mm',
            '--margin-right', '15mm',
            '--encoding', 'UTF-8',
            html_file,
            pdf_file
        ], check=True)
        print(f"\n✓ PDF successfully created: {pdf_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting to PDF: {e}")
        return

    # Clean up intermediate files
    print("\nCleaning up intermediate files...")
    if os.path.exists(combined_md):
        os.remove(combined_md)
        print(f"  Removed {combined_md}")
    if os.path.exists(html_file):
        os.remove(html_file)
        print(f"  Removed {html_file}")

    print(f"\n✓ Done! PDF created: {pdf_file}")

if __name__ == "__main__":
    main()
