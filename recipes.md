# PDF Manager Recipes 📖

This document contains practical recipes and examples for using PDF Manager CLI effectively. Each recipe includes real-world scenarios and step-by-step instructions.

## 📑 Table of Contents

- [Basic Operations](#basic-operations)
- [File Organization](#file-organization)
- [Batch Processing](#batch-processing)
- [Compression Workflows](#compression-workflows)
- [Advanced Scenarios](#advanced-scenarios)
- [Automation Scripts](#automation-scripts)

---

## Basic Operations

### Recipe 1: Merge Documents for Email
**Scenario**: You have multiple PDF receipts and want to merge them into one file for email attachment.

```bash
# Merge all PDFs in current directory
pdf-manager merge receipt_*.pdf -o monthly_receipts.pdf

# Merge with compression to reduce email size
pdf-manager merge receipt_*.pdf -o monthly_receipts.pdf --compress medium
```

### Recipe 2: Quick File Inspection
**Scenario**: You want to see what PDF files are in a directory before processing them.

```bash
# List all PDFs and their sizes
pdf-manager walk ./documents

# Check specific range of files
pdf-manager walk ./scanned_docs --start 1 --end 10
```

### Recipe 3: Compress Large PDF for Web Upload
**Scenario**: You have a large PDF that needs to be compressed for web upload with size limits.

```bash
# Basic compression (maintains quality)
pdf-manager compress large_document.pdf web_ready.pdf --compress basic

# Aggressive compression (for strict size limits)
pdf-manager compress large_document.pdf web_optimized.pdf --compress aggressive

# Check compression levels first
pdf-manager compress --info
```

---

## File Organization

### Recipe 4: Organize Scanned Documents
**Scenario**: You have 50 scanned pages and want to organize them into smaller volumes.

```bash
# Create volumes of 5 pages each with compression
pdf-manager walk ./scans ./volumes --batch-size 5 --compress medium --prefix "Scan_Batch_"

# Create larger volumes for archiving
pdf-manager walk ./scans ./archive --batch-size 20 --compress aggressive --prefix "Archive_" --suffix "_2024"

# Create volumes in reverse order (newest first)
pdf-manager walk ./scans ./volumes_desc --order desc --batch-size 10
```

### Recipe 5: Create Chapter-Based Documents
**Scenario**: Merge specific groups of PDFs to create chapter-based documents.

```bash
# Chapter 1: Introduction materials
pdf-manager merge intro_*.pdf overview.pdf --output chapter1.pdf --compress basic

# Chapter 2: Technical documentation
pdf-manager merge technical_*.pdf specifications.pdf --output chapter2.pdf --compress basic

# Final book: Combine all chapters
pdf-manager merge chapter*.pdf --output complete_book.pdf --compress medium
```

### Recipe 6: Archive Old Documents
**Scenario**: Create archived volumes from old documents for long-term storage.

```bash
# Archive 2023 documents into large volumes with aggressive compression
pdf-manager walk ./documents/2023 ./archives/2023 --batch-size 50 --compress aggressive --prefix "Archive_2023_" --suffix "_Compressed"

# Create monthly archive volumes
pdf-manager walk ./documents/2023/january ./archives/2023/monthly --batch-size 20 --prefix "Jan2023_" --compress medium

# Verify compression by checking specific files
pdf-manager compress ./documents/2023/report.pdf ./test_compression.pdf --compress aggressive
```

---

## Batch Processing

### Recipe 7: Process Invoice Batches
**Scenario**: You receive invoices in batches and need to process them monthly.

```bash
# January invoices (files 1-31)
mkdir -p ./processed/january
pdf-manager walk ./invoices --start 1 --end 31 --compress medium --output-dir ./processed/january

# February invoices (files 32-59)
mkdir -p ./processed/february
pdf-manager walk ./invoices --start 32 --end 59 --compress medium --output-dir ./processed/february

# Create monthly summary
pdf-manager merge ./processed/january/*.pdf -o january_summary.pdf --compress basic
pdf-manager merge ./processed/february/*.pdf -o february_summary.pdf --compress basic
```

### Recipe 8: Student Assignment Processing
**Scenario**: Teacher needs to process student submissions efficiently.

```bash
# Check total submissions
pdf-manager walk ./submissions

# Process assignments in groups of 10 for grading
pdf-manager walk ./submissions --start 1 --end 10 --compress basic --output-dir ./grading/batch1
pdf-manager walk ./submissions --start 11 --end 20 --compress basic --output-dir ./grading/batch2

# Create final grade report combining all feedback
pdf-manager merge ./feedback/*.pdf -o final_grades.pdf --compress medium
```

### Recipe 9: Legal Document Processing
**Scenario**: Law office needs to process case documents with strict organization.

```bash
# Evidence documents (maintain high quality)
pdf-manager walk ./case_files/evidence --compress basic --output-dir ./processed/evidence

# Correspondence (medium compression)
pdf-manager walk ./case_files/correspondence --compress medium --output-dir ./processed/correspondence

# Create case summary combining key documents
pdf-manager merge ./processed/evidence/key_*.pdf ./processed/correspondence/summary_*.pdf -o case_summary.pdf --compress basic
```

---

## Compression Workflows

### Recipe 10: Three-Tier Compression Strategy
**Scenario**: Different compression needs for different document types.

```bash
# Tier 1: Legal/Important documents (basic compression)
pdf-manager walk ./important --compress basic --output-dir ./compressed/tier1

# Tier 2: General business documents (medium compression)
pdf-manager walk ./business --compress medium --output-dir ./compressed/tier2

# Tier 3: Archive/Reference documents (aggressive compression)
pdf-manager walk ./archive --compress aggressive --output-dir ./compressed/tier3
```

### Recipe 11: Size-Optimized Workflow
**Scenario**: Need to meet specific file size requirements for different platforms.

```bash
# Email attachments (< 25MB target)
pdf-manager compress presentation.pdf email_version.pdf --compress medium

# Web upload (< 10MB target)
pdf-manager compress presentation.pdf web_version.pdf --compress aggressive

# Print version (high quality)
pdf-manager compress presentation.pdf print_version.pdf --compress basic
```

### Recipe 12: Before/After Compression Analysis
**Scenario**: Compare compression results to choose the best setting.

```bash
# Test all compression levels on a sample file
pdf-manager compress sample.pdf sample_basic.pdf --compress basic
pdf-manager compress sample.pdf sample_medium.pdf --compress medium
pdf-manager compress sample.pdf sample_aggressive.pdf --compress aggressive

# Check file sizes to compare
ls -lh sample*.pdf

# Choose best option and apply to all files
pdf-manager walk ./documents --compress medium --output-dir ./optimized
```

---

## Advanced Scenarios

### Recipe 13: Project Documentation Workflow
**Scenario**: Software project needs to combine documentation from multiple sources.

```bash
# Combine API documentation
pdf-manager merge api_*.pdf -o api_documentation.pdf --compress basic

# Combine user guides
pdf-manager merge user_guide_*.pdf manual_*.pdf -o user_documentation.pdf --compress basic

# Create final project documentation
pdf-manager merge api_documentation.pdf user_documentation.pdf setup_guide.pdf -o complete_project_docs.pdf --compress medium

# Create web-optimized version
pdf-manager compress complete_project_docs.pdf project_docs_web.pdf --compress aggressive
```

### Recipe 14: Research Paper Compilation
**Scenario**: Academic researcher needs to compile research materials.

```bash
# Combine literature review sources
pdf-manager merge literature/*.pdf -o literature_review.pdf --compress basic

# Combine methodology documents
pdf-manager merge methodology/*.pdf -o methodology.pdf --compress basic

# Create research appendix
pdf-manager walk ./data --start 1 --end 50 --compress medium --output-dir ./appendix

# Final research compilation
pdf-manager merge literature_review.pdf methodology.pdf results.pdf ./appendix/*.pdf -o complete_research.pdf --compress medium
```

### Recipe 15: Client Presentation Workflow
**Scenario**: Consulting firm needs to prepare client deliverables.

```bash
# Executive summary (high quality for printing)
pdf-manager merge exec_summary_*.pdf -o executive_summary.pdf --compress basic

# Detailed analysis (balanced compression)
pdf-manager merge analysis_*.pdf charts_*.pdf -o detailed_analysis.pdf --compress medium

# Supporting materials (compressed for email)
pdf-manager walk ./supporting_docs --compress aggressive --output-dir ./client_materials

# Final client package
pdf-manager merge executive_summary.pdf detailed_analysis.pdf -o client_presentation.pdf --compress medium
```

---

## Automation Scripts

### Recipe 16: Daily Processing Script
**Scenario**: Automate daily document processing tasks.

```bash
#!/bin/bash
# daily_process.sh

# Create dated directories
DATE=$(date +"%Y-%m-%d")
mkdir -p "./processed/$DATE"

# Process incoming documents
pdf-manager walk ./incoming --compress medium --output-dir "./processed/$DATE"

# Create daily summary
pdf-manager merge "./processed/$DATE"/*.pdf -o "./summaries/daily_summary_$DATE.pdf" --compress basic

# Clean up processed files
mv ./incoming/*.pdf "./archive/$DATE/"

echo "Daily processing complete for $DATE"
```

### Recipe 17: Weekly Batch Processing
**Scenario**: Weekly consolidation of documents.

```bash
#!/bin/bash
# weekly_batch.sh

WEEK=$(date +"%Y-W%U")

# Process each day's documents
for day in {1..7}; do
    if [ -d "./daily/day_$day" ]; then
        pdf-manager walk "./daily/day_$day" --compress medium --output-dir "./weekly/$WEEK/day_$day"
    fi
done

# Create weekly summary
pdf-manager merge "./weekly/$WEEK"/*/*.pdf -o "./weekly/summary_$WEEK.pdf" --compress basic

echo "Weekly processing complete for $WEEK"
```

### Recipe 18: Selective Processing Script
**Scenario**: Process only files that meet certain criteria.

```bash
#!/bin/bash
# selective_process.sh

# Process only large files (>1MB) with aggressive compression
find ./documents -name "*.pdf" -size +1M -exec pdf-manager compress {} ./compressed/{} --compress aggressive \;

# Process small files (<1MB) with basic compression
find ./documents -name "*.pdf" -size -1M -exec pdf-manager compress {} ./compressed/{} --compress basic \;

# Create size-optimized summary
pdf-manager merge ./compressed/*.pdf -o size_optimized_summary.pdf --compress medium
```

---

## Tips and Best Practices

### Performance Tips

1. **Batch Processing**: Process files in logical groups rather than one by one
   ```bash
   # Efficient: Process range of files
   pdf-manager walk ./docs --start 1 --end 100 --compress medium --output-dir ./processed

   # Less efficient: Process individual files
   for file in *.pdf; do
       pdf-manager compress "$file" "processed_$file" --compress medium
   done
   ```

2. **Compression Strategy**: Choose compression level based on use case
   ```bash
   # Archives: Use aggressive compression
   pdf-manager walk ./archives --compress aggressive --output-dir ./storage

   # Active documents: Use basic compression
   pdf-manager walk ./current --compress basic --output-dir ./active
   ```

3. **Directory Organization**: Organize output directories logically
   ```bash
   # Good: Organized by purpose and date
   mkdir -p ./processed/{archive,active,web}/{2024-01,2024-02}

   # Process into appropriate directories
   pdf-manager walk ./old_docs --compress aggressive --output-dir ./processed/archive/2024-01
   ```

### Quality Considerations

1. **Test Compression**: Always test compression on sample files first
   ```bash
   # Test different levels
   pdf-manager compress test.pdf test_basic.pdf --compress basic
   pdf-manager compress test.pdf test_medium.pdf --compress medium
   pdf-manager compress test.pdf test_aggressive.pdf --compress aggressive

   # Compare results and choose best option
   ```

2. **Backup Important Files**: Keep originals of critical documents
   ```bash
   # Create backup before processing
   cp -r ./important ./backup/

   # Then process
   pdf-manager walk ./important --compress basic --output-dir ./processed
   ```

3. **Verify Output**: Check processed files before deleting originals
   ```bash
   # Process files
   pdf-manager walk ./docs --compress medium --output-dir ./processed

   # Verify processing was successful
   pdf-manager walk ./processed

   # Only then remove originals if needed
   ```

---

## Command Combinations

### Recipe 19: Complex Workflow Combinations

```bash
# Step 1: Inspect files first
pdf-manager walk ./project_docs

# Step 2: Process different sections separately
pdf-manager walk ./project_docs --start 1 --end 10 --compress basic --output-dir ./sections/intro
pdf-manager walk ./project_docs --start 11 --end 30 --compress medium --output-dir ./sections/main
pdf-manager walk ./project_docs --start 31 --end 40 --compress aggressive --output-dir ./sections/appendix

# Step 3: Combine sections with appropriate compression
pdf-manager merge ./sections/intro/*.pdf -o intro_section.pdf --compress basic
pdf-manager merge ./sections/main/*.pdf -o main_section.pdf --compress basic
pdf-manager merge ./sections/appendix/*.pdf -o appendix_section.pdf --compress medium

# Step 4: Create final document
pdf-manager merge intro_section.pdf main_section.pdf appendix_section.pdf -o final_document.pdf --compress medium

# Step 5: Create web version
pdf-manager compress final_document.pdf final_document_web.pdf --compress aggressive
```

### Recipe 20: Quality Control Workflow

```bash
# Step 1: Check compression info
pdf-manager compress --info

# Step 2: Test compression on sample
pdf-manager compress sample.pdf test_output.pdf --compress medium

# Step 3: If satisfied, process batch
pdf-manager walk ./batch --compress medium --output-dir ./processed

# Step 4: Verify batch processing
pdf-manager walk ./processed

# Step 5: Create summary if needed
pdf-manager merge ./processed/*.pdf -o batch_summary.pdf --compress basic
```

---

**Happy PDF processing! 🚀📄**

*For more information, see the main [README.md](README.md) or use `pdf-manager --help` for command-specific help.*