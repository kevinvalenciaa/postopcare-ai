# handout_generator.py
"""
Ticket 13: Multi-Section Handout Generator

PURPOSE: Generate complete patient handouts with 5-7 coordinated sections.
         Each section is generated in order, maintaining consistency.

SETUP:
    pip install openai python-dotenv

STANDALONE: Uses OpenAI directly (no dependency on other modules).
"""

import os
import time
from datetime import datetime
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

# Try to import OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️  OpenAI not installed. Run: pip install openai")


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class Section:
    """
    A single section of a handout.
    
    Example:
        Section(
            section_type="pain_management",
            title="Pain Management",
            content="Some pain after surgery is normal...",
            order=2,
            word_count=150
        )
    """
    section_type: str
    title: str
    content: str
    order: int
    word_count: int


@dataclass
class Handout:
    """
    A complete patient handout.
    
    Example:
        Handout(
            procedure="Total Knee Replacement",
            title="After Your Knee Replacement: Recovery Guide",
            sections=[Section(...), Section(...), ...],
            markdown="# After Your Knee Replacement...",
            html="<h1>After Your Knee Replacement...</h1>",
            total_words=850,
            generation_time=45.2
        )
    """
    procedure: str
    title: str
    sections: list  # list[Section]
    markdown: str
    html: str
    total_words: int
    generation_time: float


# =============================================================================
# SECTION CONFIGURATIONS
# =============================================================================

# Default sections for most procedures
DEFAULT_SECTIONS = [
    {"type": "overview", "title": "Overview", "order": 1},
    {"type": "pain_management", "title": "Pain Management", "order": 2},
    {"type": "activity_restrictions", "title": "Activity Restrictions", "order": 3},
    {"type": "wound_care", "title": "Wound Care", "order": 4},
    {"type": "warning_signs", "title": "Warning Signs - When to Call Your Doctor", "order": 5},
    {"type": "follow_up", "title": "Follow-Up Care", "order": 6},
]

# Special sections for specific procedures
PROCEDURE_SECTIONS = {
    "cesarean-section": [
        {"type": "overview", "title": "Overview", "order": 1},
        {"type": "pain_management", "title": "Pain Management", "order": 2},
        {"type": "activity_restrictions", "title": "Activity Restrictions", "order": 3},
        {"type": "wound_care", "title": "Incision Care", "order": 4},
        {"type": "baby_care", "title": "Caring for Yourself and Baby", "order": 5},
        {"type": "warning_signs", "title": "Warning Signs", "order": 6},
        {"type": "follow_up", "title": "Follow-Up Care", "order": 7},
    ],
    "laparoscopic-cholecystectomy": [
        {"type": "overview", "title": "Overview", "order": 1},
        {"type": "pain_management", "title": "Pain Management", "order": 2},
        {"type": "diet", "title": "Diet After Surgery", "order": 3},
        {"type": "activity_restrictions", "title": "Activity Restrictions", "order": 4},
        {"type": "wound_care", "title": "Wound Care", "order": 5},
        {"type": "warning_signs", "title": "Warning Signs", "order": 6},
        {"type": "follow_up", "title": "Follow-Up Care", "order": 7},
    ],
}


# =============================================================================
# OPENAI HELPER
# =============================================================================

def call_openai(prompt: str, system_prompt: str = None) -> str:
    """
    Call OpenAI API to generate text.
    
    Input:
        prompt = "Write pain management instructions..."
        system_prompt = "You are a medical writer..."
    
    Output:
        "Pain Management\n\nSome pain after surgery is normal..."
    """
    if not OPENAI_AVAILABLE:
        return "[OpenAI not available - install with: pip install openai]"
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "[OPENAI_API_KEY not set in environment]"
    
    client = OpenAI(api_key=api_key)
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=500,
        temperature=0.7
    )
    
    return response.choices[0].message.content


# =============================================================================
# HANDOUT GENERATOR CLASS
# =============================================================================

class HandoutGenerator:
    """
    Generates complete multi-section patient handouts.
    
    Usage:
        generator = HandoutGenerator()
        handout = generator.generate("Total Knee Replacement")
        print(handout.markdown)
    """
    
    def __init__(self):
        """Initialize with system prompt for medical writing."""
        self.system_prompt = """You are a medical writer creating patient-friendly post-operative care instructions.

REQUIREMENTS:
- Write at a 6th-8th grade reading level
- Use simple, clear language (avoid medical jargon)
- Be specific and actionable
- Use short paragraphs (2-3 sentences)
- Include specific timeframes when relevant
- Be reassuring but accurate

AVOID:
- Complex medical terminology
- Long sentences
- Vague instructions like "as needed" without explanation"""
    
    
    def generate(self, procedure: str, procedure_slug: str = None) -> Handout:
        """
        Generate a complete handout for a procedure.
        
        Input:
            procedure = "Total Knee Replacement"
            procedure_slug = "total-knee-replacement"  # Optional, for custom sections
        
        Output:
            Handout(
                procedure="Total Knee Replacement",
                title="After Your Total Knee Replacement: Recovery Guide",
                sections=[Section(...), ...],
                markdown="# After Your Total Knee Replacement...",
                html="<h1>After Your Total Knee Replacement...</h1>",
                total_words=850,
                generation_time=45.2
            )
        """
        start_time = time.time()
        print(f"\n📝 Generating handout for: {procedure}")
        print("-" * 40)
        
        # Get sections for this procedure
        sections_config = self._get_sections(procedure_slug)
        
        # Generate each section
        sections = []
        for config in sections_config:
            print(f"  Generating: {config['title']}...")
            section = self._generate_section(
                procedure=procedure,
                section_type=config["type"],
                title=config["title"],
                order=config["order"]
            )
            sections.append(section)
        
        # Convert to Markdown and HTML
        markdown = self._to_markdown(procedure, sections)
        html = self._to_html(procedure, sections)
        
        # Calculate stats
        total_words = sum(s.word_count for s in sections)
        elapsed = time.time() - start_time
        
        print(f"\n✅ Complete! {len(sections)} sections, {total_words} words, {elapsed:.1f}s")
        
        return Handout(
            procedure=procedure,
            title=f"After Your {procedure}: Recovery Guide",
            sections=sections,
            markdown=markdown,
            html=html,
            total_words=total_words,
            generation_time=round(elapsed, 1)
        )
    
    
    def _get_sections(self, procedure_slug: str = None) -> list[dict]:
        """Get the section configuration for a procedure."""
        if procedure_slug and procedure_slug in PROCEDURE_SECTIONS:
            return PROCEDURE_SECTIONS[procedure_slug]
        return DEFAULT_SECTIONS
    
    
    def _generate_section(
        self,
        procedure: str,
        section_type: str,
        title: str,
        order: int
    ) -> Section:
        """
        Generate a single section.
        
        Input:
            procedure = "Total Knee Replacement"
            section_type = "pain_management"
            title = "Pain Management"
            order = 2
        
        Output:
            Section(
                section_type="pain_management",
                title="Pain Management",
                content="Some pain after surgery is normal...",
                order=2,
                word_count=150
            )
        """
        # TODO: Implement
        #
        # prompt = f"""Write the "{title}" section for a patient handout about {procedure} surgery.
        #
        # This section should:
        # - Be 100-200 words
        # - Include specific, actionable instructions
        # - Mention timeframes where relevant
        # - Be reassuring but factual
        #
        # Write in clear, simple language for patients."""
        #
        # content = call_openai(prompt, self.system_prompt)
        # word_count = len(content.split())
        #
        # return Section(
        #     section_type=section_type,
        #     title=title,
        #     content=content,
        #     order=order,
        #     word_count=word_count
        # )
        
        pass
    
    
    def _to_markdown(self, procedure: str, sections: list[Section]) -> str:
        """
        Convert sections to Markdown format.
        
        Output:
            "# After Your Total Knee Replacement: Recovery Guide
            
            ## Overview
            
            You have just had knee replacement surgery...
            
            ## Pain Management
            
            Some pain after surgery is normal..."
        """
        # TODO: Implement
        #
        # lines = [
        #     f"# After Your {procedure}: Recovery Guide",
        #     "",
        #     f"*Generated on {datetime.now().strftime('%B %d, %Y')}*",
        #     "",
        # ]
        #
        # for section in sorted(sections, key=lambda s: s.order):
        #     lines.append(f"## {section.title}")
        #     lines.append("")
        #     lines.append(section.content)
        #     lines.append("")
        #
        # return "\n".join(lines)
        
        pass
    
    
    def _to_html(self, procedure: str, sections: list[Section]) -> str:
        """
        Convert sections to HTML format.
        
        Output:
            "<html>
            <head><title>After Your Total Knee Replacement</title></head>
            <body>
            <h1>After Your Total Knee Replacement: Recovery Guide</h1>
            <h2>Overview</h2>
            <p>You have just had...</p>
            </body>
            </html>"
        """
        # TODO: Implement
        #
        # import html as html_lib
        #
        # body_parts = [
        #     f"<h1>After Your {html_lib.escape(procedure)}: Recovery Guide</h1>",
        #     f"<p><em>Generated on {datetime.now().strftime('%B %d, %Y')}</em></p>",
        # ]
        #
        # for section in sorted(sections, key=lambda s: s.order):
        #     body_parts.append(f"<h2>{html_lib.escape(section.title)}</h2>")
        #     # Convert paragraphs
        #     for para in section.content.split("\n\n"):
        #         if para.strip():
        #             body_parts.append(f"<p>{html_lib.escape(para.strip())}</p>")
        #
        # html = f"""<!DOCTYPE html>
        # <html>
        # <head>
        #     <meta charset="utf-8">
        #     <title>After Your {html_lib.escape(procedure)}</title>
        #     <style>
        #         body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
        #         h1 {{ color: #2c5282; }}
        #         h2 {{ color: #2b6cb0; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; }}
        #     </style>
        # </head>
        # <body>
        # {"".join(body_parts)}
        # </body>
        # </html>"""
        #
        # return html
        
        pass


# =============================================================================
# MOCK DATA FOR TESTING
# =============================================================================

MOCK_SECTIONS = [
    Section(
        section_type="overview",
        title="Overview",
        content="You have just had total knee replacement surgery. This guide will help you recover safely at home. Most patients spend 1-3 days in the hospital before going home. Full recovery takes about 3 months, but you will feel better each week.",
        order=1,
        word_count=47
    ),
    Section(
        section_type="pain_management",
        title="Pain Management",
        content="Some pain after surgery is normal. Take your prescribed pain medication as directed. You can also use ice packs for 20 minutes at a time to reduce swelling. Pain should get better each day. If pain suddenly gets worse, call your doctor.",
        order=2,
        word_count=48
    ),
    Section(
        section_type="activity_restrictions",
        title="Activity Restrictions",
        content="Start walking with your walker or crutches on the day of surgery. Walk a little more each day. Do your physical therapy exercises 3 times daily. Do not twist or pivot on your new knee. Avoid stairs for the first week if possible.",
        order=3,
        word_count=47
    ),
    Section(
        section_type="wound_care",
        title="Wound Care",
        content="Keep your incision clean and dry. Do not soak in a bath or pool until your doctor says it is okay. Change bandages as instructed. It is normal for the incision to be slightly red and warm.",
        order=4,
        word_count=40
    ),
    Section(
        section_type="warning_signs",
        title="Warning Signs - When to Call Your Doctor",
        content="Call your doctor if you have: fever over 101°F, increasing pain or swelling, redness spreading from the incision, drainage or pus from the wound, calf pain or swelling, or shortness of breath. These could be signs of infection or blood clots.",
        order=5,
        word_count=50
    ),
    Section(
        section_type="follow_up",
        title="Follow-Up Care",
        content="Your first follow-up appointment is usually 2 weeks after surgery. Bring a list of your medications and any questions. Physical therapy will continue for 6-12 weeks. Most patients can return to normal activities in 3 months.",
        order=6,
        word_count=43
    ),
]


def test_with_mock_data():
    """Test output format without API calls."""
    print("=" * 50)
    print("TESTING WITH MOCK DATA")
    print("=" * 50)
    
    # Build mock handout
    handout = Handout(
        procedure="Total Knee Replacement",
        title="After Your Total Knee Replacement: Recovery Guide",
        sections=MOCK_SECTIONS,
        markdown="# After Your Total Knee Replacement: Recovery Guide\n\n## Overview\n\n...",
        html="<h1>After Your Total Knee Replacement</h1>...",
        total_words=sum(s.word_count for s in MOCK_SECTIONS),
        generation_time=0.1
    )
    
    print(f"\n📄 Handout: {handout.title}")
    print(f"   Procedure: {handout.procedure}")
    print(f"   Sections: {len(handout.sections)}")
    print(f"   Total words: {handout.total_words}")
    
    print("\n📋 Sections:")
    for s in handout.sections:
        print(f"   {s.order}. {s.title} ({s.word_count} words)")
    
    print("\n📝 Sample content (Overview):")
    print(f"   {MOCK_SECTIONS[0].content}")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    # Test with mock data first
    test_with_mock_data()
    
    # Uncomment to generate with real API:
    # print("\n" + "=" * 50)
    # print("GENERATING WITH OPENAI")
    # print("=" * 50)
    #
    # generator = HandoutGenerator()
    # handout = generator.generate("Total Knee Replacement", "total-knee-replacement")
    #
    # # Save outputs
    # with open("handout.md", "w") as f:
    #     f.write(handout.markdown)
    # with open("handout.html", "w") as f:
    #     f.write(handout.html)
    #
    # print(f"\nSaved to handout.md and handout.html")
