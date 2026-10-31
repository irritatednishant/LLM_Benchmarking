"""
Script to generate PROJECT_SYNOPSIS.docx matching the exact format of the reference document,
featuring a React.js frontend and Python FastAPI backend.
"""
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_synopsis_docx(filename="PROJECT_SYNOPSIS.docx"):
    doc = Document()

    # Set margins
    for section in doc.sections:
        section.top_margin = Inches(0.85)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base style: Times New Roman, 11pt
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)

    def add_p(text="", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=5, line_spacing=1.15, bold=False):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if text:
            run = p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11)
            run.font.bold = bold
            run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    # Header / Title (Centered)
    p_title = add_p("PROJECT SYNOPSIS", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=3, bold=True)
    p_title.runs[0].font.size = Pt(13)

    p_sub1 = add_p("SLM Benchmark", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2, bold=True)
    p_sub1.runs[0].font.size = Pt(12)

    p_sub2 = add_p("A Local Small Language Model Performance & Reliability Analysis Web Platform", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=12, bold=True)
    p_sub2.runs[0].font.size = Pt(11)

    # Section 1
    add_p("1. Project Definition and Introduction", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=5, space_after=3, bold=True)
    
    add_p(
        "With the rapid emergence and adoption of open-source Small Language Models (SLMs) such as Llama 3.2, Mistral, and Phi-4 Mini, developers and organizations increasingly seek to run AI models locally for strict data privacy, zero API costs, and offline availability. However, selecting the optimal model for production systems is challenging because empirical trade-offs between execution speed, memory footprint, and generation reliability are often undocumented across consumer hardware setups. Furthermore, downstream applications—such as automated customer ticket routing, data extraction, and internal microservices—demand strict adherence to structured outputs (e.g., valid JSON schemas), which lightweight models can frequently fail to generate accurately without a unified evaluation interface.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=5, line_spacing=1.15
    )

    add_p(
        "SLM Benchmark is a proposed full-stack web application and diagnostic framework designed to evaluate, profile, and compare local small language models executed via Ollama through an intuitive, interactive web interface. Built with a React.js single-page application and a high-performance Python FastAPI backend, the platform enables users to configure benchmark test suites, execute prompts across multiple model architectures, and monitor inference metrics in real time. By establishing an automated, data-driven testing pipeline, the project bridges the gap between raw parameter counts and real-world deployment viability, helping developers select the ideal model for resource-constrained environments.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=9, line_spacing=1.15
    )

    # Section 2
    add_p("2. What the System Will Do", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=4, space_after=3, bold=True)

    add_p(
        "The web application provides an interactive control dashboard where users can select candidate models, choose from standardized prompt suites, or craft custom test inputs. The FastAPI backend orchestrates asynchronous inference runs with the local Ollama runtime, continuously streaming live telemetry—including end-to-end latency, tokens generated per second, prompt evaluation velocity, and active RAM consumption—directly to the React frontend. For structured tasks, the system passes domain-specific prompts and utilizes Pydantic validation to inspect JSON syntax and field integrity, computing empirical schema compliance rates visualized through dynamic charts.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=5, line_spacing=1.15
    )

    add_p(
        "For example, a user can navigate to the benchmark dashboard, select models like Llama 3.2 3B, Mistral 7B, and Phi-4 Mini, and trigger a customer support ticket evaluation suite. The backend dispatches requests, measures hardware resource allocation, parses model outputs against target Pydantic contracts, and persists metrics to SQLite and dual CSV/JSON datastores. The React interface dynamically renders real-time latency gauges, token velocity bar charts, and JSON validation success rates side-by-side, allowing users to visually inspect generation quality and export comprehensive comparative reports for architectural decision-making.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=9, line_spacing=1.15
    )

    # Tech Stack
    add_p("Language :", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=4, space_after=3, bold=True)

    def add_bullet(label, value):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        
        r1 = p.add_run(label)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        r1.font.bold = False

        r2 = p.add_run(value)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(11)
        return p

    add_bullet("Frontend: ", "React.js, HTML5, CSS3 and JavaScript (with Chart.js for data visualization)")
    add_bullet("Backend: ", "Python with the FastAPI framework, Ollama API, and Pydantic")
    add_bullet("Database: ", "SQLite (with structured CSV and JSON logging datastores)")
    add_bullet("Core functionality: ", "Interactive web dashboard, multi-model benchmarking, latency & throughput profiling, and JSON schema validation")

    # Conclusion
    add_p("Conclusion", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=7, space_after=3, bold=True)

    add_p(
        "SLM Benchmark aims to make local AI adoption practical, transparent, and dependable by providing an accessible, full-stack web platform for evaluating small language models before production deployment. By integrating a responsive React.js frontend, an asynchronous FastAPI backend, live hardware telemetry, and Pydantic schema validation, the project represents a comprehensive application of modern web development, API engineering, and AI performance evaluation. Its focus on speed, memory economy, and output validity empowers developers to make informed architectural choices while ensuring complete data privacy in a local, offline environment.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=0, line_spacing=1.15
    )

    # PAGE BREAK TO PAGE 2
    doc.add_page_break()

    # Page 2: Student Details
    p_sname = add_p("Student Name: Nishant", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=4, bold=False)
    p_sname.runs[0].font.bold = False

    p_enum = add_p("Enrollment Number: 10517704426", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=4, bold=False)
    
    p_course = add_p("Course: Master of Computer Applications (MCA 1-B)", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=4, bold=False)
    
    p_mentor = add_p("Project Mentor: Dr. Cosmena", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=4, bold=False)

    doc.save(filename)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    create_synopsis_docx()
