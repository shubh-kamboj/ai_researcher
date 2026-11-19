from langchain_core.tools import tool
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet

@tool
def render_latex_pdf(latex_content: str) -> str:
    """Render a LaTeX document to PDF.

    Args:
        latex_content: The LaTeX document content as a string

    Returns:
        Path to the generated PDF document
    """

    try:
        output_dir = Path("output").absolute()
        output_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"paper_{timestamp}.pdf"
        final_pdf = output_dir / pdf_filename

        # Setup PDF document
        doc = SimpleDocTemplate(
            str(final_pdf),
            pagesize=A4
        )
        styles = getSampleStyleSheet()

        # Add content
        story = []
        story.append(Paragraph("Research Paper", styles["Title"]))
        story.append(Spacer(1, 20))
        story.append(Paragraph(latex_content, styles["BodyText"]))
        
        # Generate PDF
        doc.build(story)

        if not final_pdf.exists():
            raise FileNotFoundError("PDF file was not generated")
        print(f"Successfully generated PDF at {final_pdf}")
        return str(final_pdf)
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        raise
