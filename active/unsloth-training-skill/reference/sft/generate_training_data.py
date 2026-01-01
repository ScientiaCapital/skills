"""
Synthetic Training Data Generator for Sales Call Extraction Model
==================================================================

This script generates training data for fine-tuning a sales call extraction model.

Usage:
    1. Add your seed examples to SEED_EXAMPLES below (or load from file)
    2. Set your API key (Claude recommended, GPT-4 works too)
    3. Run: python generate_training_data.py
    4. Output: training_data.jsonl ready for Unsloth

Data generation strategy:
    - Start with 25-50 real examples from your CRM (anonymized)
    - Use LLM to generate 10-20 variations per seed
    - Add template-based generation for edge cases
    - Filter for quality
    - Target: 500-2000 examples

Cost estimate:
    - 50 seeds × 10 variations × ~1000 tokens = ~500K tokens
    - Claude Sonnet: ~$1.50
    - GPT-4o-mini: ~$0.30

Author: Tim Kipper
Purpose: GTME Portfolio - On-device sales assistant
"""

import json
import random
import os
import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import hashlib

# =============================================================================
# CONFIGURATION
# =============================================================================

CONFIG = {
    # API Configuration - set one of these
    "api_provider": "anthropic",  # "anthropic" or "openai"
    "anthropic_model": "claude-sonnet-4-20250514",
    "openai_model": "gpt-4o-mini",
    
    # Generation settings
    "variations_per_seed": 10,
    "template_examples": 200,  # Additional template-based examples
    "max_concurrent_requests": 5,
    
    # Output
    "output_file": "training_data.jsonl",
    "seed_file": "seed_examples.json",  # Optional: load seeds from file
    
    # Quality filtering
    "min_transcript_length": 50,
    "max_transcript_length": 2000,
}

# =============================================================================
# SCHEMA DEFINITION
# =============================================================================

@dataclass
class ExtractedLead:
    """Schema for extracted lead information."""
    company_name: str
    contact_name: Optional[str] = None
    contact_title: Optional[str] = None
    team_size: Optional[int] = None
    team_breakdown: Optional[str] = None
    location: Optional[str] = None
    vertical: Optional[str] = None
    current_software: List[str] = None
    pain_points: List[str] = None
    interest_areas: List[str] = None
    budget_mentioned: Optional[str] = None
    timeline: Optional[str] = None
    decision_makers: List[str] = None
    next_step: str = "none"  # demo | follow_up_call | send_info | proposal | none
    next_step_date: Optional[str] = None
    next_step_notes: Optional[str] = None
    intent_level: str = "unknown"  # high | medium | low | unknown
    key_quotes: List[str] = None
    competitors_mentioned: List[str] = None
    
    def __post_init__(self):
        # Initialize empty lists
        if self.current_software is None:
            self.current_software = []
        if self.pain_points is None:
            self.pain_points = []
        if self.interest_areas is None:
            self.interest_areas = []
        if self.decision_makers is None:
            self.decision_makers = []
        if self.key_quotes is None:
            self.key_quotes = []
        if self.competitors_mentioned is None:
            self.competitors_mentioned = []
    
    def to_dict(self) -> Dict:
        return asdict(self)

# =============================================================================
# DOMAIN KNOWLEDGE - MEP CONTRACTOR SPACE
# =============================================================================

# Company name components
COMPANY_PREFIXES = [
    "ABC", "Quality", "Premier", "First", "Pro", "Elite", "Superior",
    "Reliable", "Trusted", "Expert", "Advanced", "Modern", "Classic",
    "Regional", "Metro", "Valley", "Mountain", "Coastal", "Central",
    "Allied", "United", "American", "National", "Pacific", "Atlantic"
]

COMPANY_SUFFIXES = [
    "Mechanical", "HVAC", "Plumbing", "Services", "Contractors",
    "Systems", "Solutions", "Industries", "Enterprises", "Group",
    "& Sons", "Brothers", "Partners", "Associates", "Corp", "Inc", "LLC"
]

# Contact names
FIRST_NAMES = [
    "Mike", "John", "Dave", "Tom", "Steve", "Bob", "Jim", "Bill", "Joe", "Dan",
    "Sarah", "Lisa", "Jennifer", "Michelle", "Karen", "Amy", "Susan", "Linda",
    "Chris", "Pat", "Alex", "Sam", "Jordan", "Taylor", "Casey", "Morgan"
]

LAST_NAMES = [
    "Thompson", "Johnson", "Williams", "Brown", "Garcia", "Martinez", "Davis",
    "Rodriguez", "Smith", "Miller", "Wilson", "Anderson", "Taylor", "Thomas",
    "Moore", "Jackson", "Martin", "Lee", "Harris", "Clark", "Lewis", "Robinson"
]

TITLES = [
    "Owner", "President", "CEO", "General Manager", "Operations Manager",
    "Service Manager", "Office Manager", "Controller", "CFO", "COO",
    "VP of Operations", "Director of Operations", "Dispatch Manager",
    "Field Supervisor", "Project Manager", "Partner"
]

# Locations
LOCATIONS = [
    "Phoenix", "Phoenix metro", "Dallas", "DFW area", "Houston", "Austin",
    "Denver", "Denver metro", "Atlanta", "Chicago", "Chicagoland",
    "Los Angeles", "LA area", "San Diego", "Seattle", "Portland",
    "Minneapolis", "St. Louis", "Kansas City", "Nashville", "Charlotte",
    "Tampa", "Miami", "Orlando", "Jacksonville", "Indianapolis",
    "Columbus", "Cleveland", "Cincinnati", "Detroit", "Milwaukee"
]

# Verticals
VERTICALS = [
    "commercial HVAC", "residential HVAC", "light commercial HVAC",
    "commercial plumbing", "residential plumbing", "service plumbing",
    "new construction plumbing", "commercial electrical", "residential electrical",
    "fire protection", "refrigeration", "controls", "building automation",
    "sheet metal", "ductwork", "hydronic systems", "geothermal",
    "mechanical contracting", "design-build", "plan and spec"
]

# Current software
SOFTWARE_OPTIONS = [
    # FSM platforms
    ("ServiceTitan", ["ST", "Service Titan"]),
    ("Jobber", []),
    ("FieldEdge", ["Field Edge"]),
    ("Housecall Pro", ["HCP", "Housecall"]),
    ("Service Fusion", []),
    ("ServiceMax", []),
    ("FieldAware", []),
    ("mHelpDesk", []),
    ("Kickserv", []),
    ("Workiz", []),
    ("ServiceM8", []),
    
    # Accounting
    ("QuickBooks", ["QB", "Quickbooks"]),
    ("Sage", ["Sage 100", "Sage 300"]),
    ("Jonas", ["Jonas Construction"]),
    ("Foundation", ["Foundation Software"]),
    ("Viewpoint", ["Vista by Viewpoint"]),
    ("Procore", []),
    
    # Generic
    ("spreadsheets", ["Excel", "Google Sheets"]),
    ("paper", ["paper and pen", "whiteboards"]),
    ("nothing formal", ["no real system"]),
]

# Pain points
PAIN_POINTS = [
    # Pricing/cost
    "pricing is too high",
    "costs keep going up",
    "nickel and dimed on every feature",
    "paying for features we don't use",
    "per-user pricing is killing us",
    
    # Complexity
    "too complicated",
    "way too many clicks",
    "takes forever to do simple things",
    "steep learning curve",
    "techs won't use it",
    "field guys hate it",
    
    # Functionality gaps
    "reporting is terrible",
    "can't get the reports we need",
    "no real job costing",
    "inventory tracking is a joke",
    "scheduling is a nightmare",
    "dispatching takes forever",
    "can't customize anything",
    "no purchase order system",
    "estimates take too long",
    "no flat rate option",
    
    # Support
    "support is awful",
    "can never get anyone on the phone",
    "takes weeks to get help",
    "they don't understand our business",
    
    # Integration
    "doesn't talk to QuickBooks",
    "no accounting integration",
    "have to enter everything twice",
    "data silos everywhere",
    
    # Mobile
    "mobile app is garbage",
    "no offline mode",
    "crashes all the time",
    "techs can't use it in the field",
]

# Interest areas
INTEREST_AREAS = [
    "job costing",
    "scheduling",
    "dispatching",
    "invoicing",
    "inventory management",
    "reporting",
    "mobile app",
    "customer portal",
    "flat rate pricing",
    "estimates and proposals",
    "purchase orders",
    "time tracking",
    "GPS tracking",
    "maintenance agreements",
    "service agreements",
    "marketing automation",
    "call tracking",
    "integration with accounting",
    "QuickBooks integration",
    "payroll integration",
]

# Next step types
NEXT_STEPS = {
    "demo": [
        "wants to see a demo",
        "scheduled a demo",
        "doing a demo",
        "showing them the system",
        "live demo scheduled",
        "wants a full walkthrough",
    ],
    "follow_up_call": [
        "following up next week",
        "calling back in a few days",
        "check back with them",
        "needs to think about it",
        "wants to discuss internally first",
        "calling back after their busy season",
    ],
    "send_info": [
        "sending over some info",
        "emailing case studies",
        "sending pricing",
        "sharing some materials",
        "sending a one-pager",
        "emailing our brochure",
    ],
    "proposal": [
        "putting together a proposal",
        "sending a formal quote",
        "working on pricing for them",
        "customizing a package",
    ],
    "none": [
        "not a fit right now",
        "not ready to move",
        "happy with current solution",
        "no budget",
        "just kicking tires",
    ],
}

# Intent signals
HIGH_INTENT_SIGNALS = [
    "ready to move",
    "need something by",
    "budget approved",
    "pain is urgent",
    "current contract ending",
    "just fired",
    "can't take it anymore",
    "needs to happen",
    "making a decision",
]

LOW_INTENT_SIGNALS = [
    "just looking",
    "early stages",
    "no timeline",
    "happy enough",
    "not a priority",
    "maybe next year",
    "just curious",
]

# =============================================================================
# TEMPLATE-BASED GENERATION
# =============================================================================

def generate_company_name() -> str:
    """Generate a realistic MEP contractor company name."""
    pattern = random.choice([
        "{prefix} {suffix}",
        "{prefix} {suffix}",
        "{last} {suffix}",
        "{last} & {last2} {suffix}",
        "{last} {suffix}",
    ])
    
    return pattern.format(
        prefix=random.choice(COMPANY_PREFIXES),
        suffix=random.choice(COMPANY_SUFFIXES),
        last=random.choice(LAST_NAMES),
        last2=random.choice(LAST_NAMES),
    )

def generate_contact() -> tuple:
    """Generate a contact name and title."""
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    title = random.choice(TITLES)
    return f"{first} {last}", first, title

def generate_transcript_template() -> tuple:
    """Generate a synthetic transcript using templates."""
    
    # Generate basic info
    company = generate_company_name()
    contact_full, contact_first, title = generate_contact()
    team_size = random.choice([None, *range(5, 200, 5)])
    location = random.choice([None, *LOCATIONS])
    vertical = random.choice([None, *VERTICALS])
    
    # Current software
    num_software = random.randint(0, 3)
    software_items = random.sample(SOFTWARE_OPTIONS, min(num_software, len(SOFTWARE_OPTIONS)))
    current_software = [s[0] for s in software_items]
    
    # Pain points
    num_pains = random.randint(0, 4)
    pain_points = random.sample(PAIN_POINTS, min(num_pains, len(PAIN_POINTS)))
    
    # Interest areas
    num_interests = random.randint(1, 4)
    interest_areas = random.sample(INTEREST_AREAS, min(num_interests, len(INTEREST_AREAS)))
    
    # Next step
    next_step_type = random.choice(list(NEXT_STEPS.keys()))
    next_step_phrase = random.choice(NEXT_STEPS[next_step_type])
    
    # Intent
    if next_step_type == "demo":
        intent = random.choice(["high", "medium"])
    elif next_step_type == "proposal":
        intent = "high"
    elif next_step_type == "none":
        intent = random.choice(["low", "unknown"])
    else:
        intent = random.choice(["medium", "low", "unknown"])
    
    # Build transcript parts
    parts = []
    
    # Opening - who did they talk to
    openings = [
        f"Just finished a call with {contact_first} at {company}",
        f"Talked to {contact_full} over at {company}",
        f"Had a good conversation with {contact_first} from {company}",
        f"Quick call with {company}, spoke with {contact_first}",
        f"Just got off the phone with {contact_full}, {title} at {company}",
        f"Met with {contact_first} at {company}",
    ]
    parts.append(random.choice(openings))
    
    # Company details
    if team_size:
        size_phrases = [
            f"they're about {team_size} people",
            f"{team_size}-person shop",
            f"around {team_size} employees",
            f"team of {team_size}",
        ]
        parts.append(random.choice(size_phrases))
    
    if vertical:
        vertical_phrases = [
            f"doing {vertical}",
            f"focused on {vertical}",
            f"{vertical} work mostly",
            f"they specialize in {vertical}",
        ]
        parts.append(random.choice(vertical_phrases))
    
    if location:
        location_phrases = [
            f"based in {location}",
            f"out of {location}",
            f"in the {location} area",
            f"{location}",
        ]
        parts.append(random.choice(location_phrases))
    
    # Current software
    if current_software:
        if len(current_software) == 1:
            sw_phrases = [
                f"they're running {current_software[0]}",
                f"currently on {current_software[0]}",
                f"using {current_software[0]} right now",
                f"got {current_software[0]} but",
            ]
        else:
            sw_phrases = [
                f"they have {' and '.join(current_software)}",
                f"using {', '.join(current_software)}",
            ]
        parts.append(random.choice(sw_phrases))
    
    # Pain points
    if pain_points:
        for i, pain in enumerate(pain_points):
            if i == 0:
                pain_intros = [
                    f"{contact_first} said {pain}",
                    f"main complaint is {pain}",
                    f"biggest issue: {pain}",
                    f"they're frustrated because {pain}",
                ]
            else:
                pain_intros = [
                    f"also mentioned {pain}",
                    f"and {pain}",
                    f"plus {pain}",
                ]
            if random.random() > 0.3:  # Don't include all pains
                parts.append(random.choice(pain_intros))
    
    # Interest areas
    if interest_areas:
        interest_phrases = [
            f"really interested in our {', '.join(interest_areas[:2])}",
            f"wants to see the {interest_areas[0]} features",
            f"asked specifically about {' and '.join(interest_areas[:2])}",
            f"main focus was {interest_areas[0]}",
        ]
        parts.append(random.choice(interest_phrases))
    
    # Next steps
    parts.append(next_step_phrase)
    
    # Assemble transcript
    # Use different connectors for natural flow
    connectors = [", ", ". ", " - ", ", ", ". "]
    transcript = ""
    for i, part in enumerate(parts):
        if i == 0:
            transcript = part
        else:
            conn = random.choice(connectors)
            # Capitalize after period
            if conn == ". " and part:
                part = part[0].upper() + part[1:]
            transcript += conn + part
    
    if not transcript.endswith("."):
        transcript += "."
    
    # Build extraction
    extraction = ExtractedLead(
        company_name=company,
        contact_name=contact_full if random.random() > 0.2 else contact_first,
        contact_title=title if random.random() > 0.5 else None,
        team_size=team_size,
        location=location,
        vertical=vertical,
        current_software=current_software,
        pain_points=pain_points,
        interest_areas=interest_areas,
        next_step=next_step_type,
        intent_level=intent,
    )
    
    return transcript, extraction.to_dict()

# =============================================================================
# LLM-BASED GENERATION
# =============================================================================

VARIATION_PROMPT = """You are generating training data for a sales call extraction model used by MEP (Mechanical, Electrical, Plumbing) contractor software salespeople.

Here's a real example of a sales rep's voice note transcription after a prospect call:

<seed_transcript>
{seed_transcript}
</seed_transcript>

And here's what should be extracted from it:

<seed_extraction>
{seed_extraction}
</seed_extraction>

Generate {num_variations} NEW and DIFFERENT realistic variations. Each should:

1. SOUND LIKE NATURAL SPEECH - These are voice notes recorded in a car after a call:
   - Use filler words occasionally ("um", "so", "like", "you know")
   - Incomplete sentences are fine
   - Stream of consciousness is realistic
   - Mix of formal and casual language

2. COVER MEP CONTRACTOR DIVERSITY:
   - Company sizes from 5 to 200 employees
   - Different specialties: HVAC, plumbing, electrical, fire protection, refrigeration, etc.
   - Different markets: residential, commercial, light commercial, service, new construction
   - Different regions across the US

3. VARY THE INFORMATION DENSITY:
   - Some calls reveal a lot, some reveal little
   - Sometimes names are unclear or missing
   - Sometimes company size is vague ("small shop", "pretty big operation")
   - Not every call has clear next steps

4. INCLUDE REALISTIC SOFTWARE MENTIONS:
   - ServiceTitan, Jobber, FieldEdge, Housecall Pro, Service Fusion
   - QuickBooks, Sage, spreadsheets, paper systems
   - Sometimes they mention competitors or alternatives they've looked at

5. VARY INTENT LEVELS:
   - High intent: urgent pain, budget ready, clear timeline
   - Medium intent: interested but not urgent
   - Low intent: just looking, no timeline, early research
   - Include some calls that go nowhere

6. INCLUDE MEMORABLE QUOTES when appropriate - things the prospect actually said that reveal their situation

For each variation, output in this exact format:

---VARIATION {n}---
TRANSCRIPT:
[The voice note transcript - 50-300 words, natural spoken language]

EXTRACTION:
[Valid JSON matching this schema exactly]
{{
  "company_name": "string",
  "contact_name": "string or null",
  "contact_title": "string or null", 
  "team_size": integer or null,
  "team_breakdown": "string or null",
  "location": "string or null",
  "vertical": "string or null",
  "current_software": ["array"],
  "pain_points": ["array"],
  "interest_areas": ["array"],
  "budget_mentioned": "string or null",
  "timeline": "string or null",
  "decision_makers": ["array"],
  "next_step": "demo" | "follow_up_call" | "send_info" | "proposal" | "none",
  "next_step_date": "string or null",
  "next_step_notes": "string or null",
  "intent_level": "high" | "medium" | "low" | "unknown",
  "key_quotes": ["array of verbatim quotes"],
  "competitors_mentioned": ["array"]
}}
---END VARIATION {n}---

Make each variation meaningfully different from the seed and from each other. Vary:
- The specific company/contact details
- The pain points and interests
- The speaking style and level of detail
- The outcome and next steps

Generate exactly {num_variations} variations now:"""

async def generate_variations_anthropic(
    seed_transcript: str,
    seed_extraction: dict,
    num_variations: int = 10,
) -> List[tuple]:
    """Generate variations using Claude API."""
    
    try:
        import anthropic
    except ImportError:
        print("pip install anthropic")
        return []
    
    client = anthropic.Anthropic()
    
    prompt = VARIATION_PROMPT.format(
        seed_transcript=seed_transcript,
        seed_extraction=json.dumps(seed_extraction, indent=2),
        num_variations=num_variations,
        n="{n}",  # Keep placeholder for format
    )
    
    response = client.messages.create(
        model=CONFIG["anthropic_model"],
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return parse_variations(response.content[0].text)

async def generate_variations_openai(
    seed_transcript: str,
    seed_extraction: dict,
    num_variations: int = 10,
) -> List[tuple]:
    """Generate variations using OpenAI API."""
    
    try:
        from openai import OpenAI
    except ImportError:
        print("pip install openai")
        return []
    
    client = OpenAI()
    
    prompt = VARIATION_PROMPT.format(
        seed_transcript=seed_transcript,
        seed_extraction=json.dumps(seed_extraction, indent=2),
        num_variations=num_variations,
        n="{n}",
    )
    
    response = client.chat.completions.create(
        model=CONFIG["openai_model"],
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return parse_variations(response.choices[0].message.content)

def parse_variations(response_text: str) -> List[tuple]:
    """Parse LLM response into (transcript, extraction) pairs."""
    
    variations = []
    
    # Split by variation markers
    parts = response_text.split("---VARIATION")
    
    for part in parts[1:]:  # Skip first empty part
        try:
            # Extract transcript
            transcript_match = part.split("TRANSCRIPT:")[1].split("EXTRACTION:")[0]
            transcript = transcript_match.strip()
            
            # Extract JSON
            extraction_part = part.split("EXTRACTION:")[1]
            json_start = extraction_part.find("{")
            json_end = extraction_part.rfind("}") + 1
            json_str = extraction_part[json_start:json_end]
            extraction = json.loads(json_str)
            
            # Validate minimum fields
            if extraction.get("company_name") and len(transcript) > 30:
                variations.append((transcript, extraction))
                
        except (IndexError, json.JSONDecodeError) as e:
            print(f"  Warning: Failed to parse variation: {e}")
            continue
    
    return variations

# =============================================================================
# SEED EXAMPLES - ADD YOUR REAL DATA HERE
# =============================================================================

# These are example seeds - REPLACE WITH YOUR ACTUAL ANONYMIZED CRM DATA
SEED_EXAMPLES = [
    {
        "transcript": """Just got off a great call with Mike Thompson at Reliable Mechanical. 
        They're a 35-person commercial HVAC shop in Phoenix, been running ServiceTitan 
        for two years now. Mike said the pricing has gotten insane, like they're paying 
        almost three times what they started at. Really interested in our job costing, 
        said that's the biggest gap they have right now. They're also frustrated that 
        their techs don't use the mobile app because it's too complicated. 
        Mike said quote 'my guys just want to clock in and see their jobs, not navigate 
        a spaceship.' Wants to do a demo next Tuesday, bringing his ops manager.""",
        
        "extraction": {
            "company_name": "Reliable Mechanical",
            "contact_name": "Mike Thompson",
            "contact_title": None,
            "team_size": 35,
            "team_breakdown": None,
            "location": "Phoenix",
            "vertical": "commercial HVAC",
            "current_software": ["ServiceTitan"],
            "pain_points": [
                "pricing has gotten insane",
                "techs don't use mobile app",
                "mobile app too complicated"
            ],
            "interest_areas": ["job costing"],
            "budget_mentioned": None,
            "timeline": None,
            "decision_makers": ["Mike Thompson", "ops manager"],
            "next_step": "demo",
            "next_step_date": "next Tuesday",
            "next_step_notes": "bringing ops manager",
            "intent_level": "high",
            "key_quotes": [
                "my guys just want to clock in and see their jobs, not navigate a spaceship"
            ],
            "competitors_mentioned": ["ServiceTitan"]
        }
    },
    {
        "transcript": """Quick call with Premier Plumbing, talked to Dave who I think is 
        the GM. Smaller shop, maybe 12-15 people, mostly residential service in the 
        Denver area. They're literally running everything on paper and QuickBooks, 
        like literally paper work orders. Dave knows they need to modernize but said 
        his techs are older and he's worried about adoption. Mentioned they looked at 
        Housecall Pro last year but never pulled the trigger. No real urgency, said 
        maybe they'll think about it after their busy season. I'll check back in Q1.""",
        
        "extraction": {
            "company_name": "Premier Plumbing",
            "contact_name": "Dave",
            "contact_title": "GM",
            "team_size": 12,
            "team_breakdown": None,
            "location": "Denver area",
            "vertical": "residential service plumbing",
            "current_software": ["paper", "QuickBooks"],
            "pain_points": [
                "running on paper",
                "worried about tech adoption with older techs"
            ],
            "interest_areas": ["modernization", "field service management"],
            "budget_mentioned": None,
            "timeline": "after busy season",
            "decision_makers": ["Dave"],
            "next_step": "follow_up_call",
            "next_step_date": "Q1",
            "next_step_notes": None,
            "intent_level": "low",
            "key_quotes": [],
            "competitors_mentioned": ["Housecall Pro"]
        }
    },
    {
        "transcript": """So that was an interesting one. ABC Services, they're kind of a 
        hybrid - do both HVAC and plumbing. Talked to Sarah the owner and her ops guy 
        Marcus was on too. About 45 people between the two divisions, mix of commercial 
        and residential work in Atlanta. They tried Jobber maybe two years ago, total 
        disaster, half the team refused to use it and they eventually gave up. So now 
        they're gun shy. Sarah said she can't afford another failed implementation. 
        But she also said inventory tracking is killing them, like they have no idea 
        what's on the trucks. Marcus mentioned they're losing maybe 50K a year in 
        parts they can't account for. That got their attention when I mentioned our 
        inventory module. They want to see specifically how that works. Sarah asked 
        about implementation support, like hand holding through the transition. 
        Setting up a call next week to dig into that more.""",
        
        "extraction": {
            "company_name": "ABC Services",
            "contact_name": "Sarah",
            "contact_title": "Owner",
            "team_size": 45,
            "team_breakdown": "two divisions (HVAC and plumbing)",
            "location": "Atlanta",
            "vertical": "HVAC and plumbing",
            "current_software": [],
            "pain_points": [
                "inventory tracking",
                "don't know what's on trucks",
                "losing money on unaccounted parts",
                "previous failed implementation with Jobber"
            ],
            "interest_areas": ["inventory management", "implementation support"],
            "budget_mentioned": "50K/year in lost parts",
            "timeline": None,
            "decision_makers": ["Sarah", "Marcus"],
            "next_step": "follow_up_call",
            "next_step_date": "next week",
            "next_step_notes": "dig into inventory and implementation support",
            "intent_level": "medium",
            "key_quotes": [
                "can't afford another failed implementation"
            ],
            "competitors_mentioned": ["Jobber"]
        }
    },
]

# =============================================================================
# TRAINING DATA FORMATTING
# =============================================================================

SYSTEM_PROMPT = """You are a sales call extraction assistant for MEP (Mechanical, Electrical, Plumbing) contractor software sales.

Given a voice note transcript from a sales rep after a prospect call, extract structured information.

Output ONLY valid JSON with these fields:
{
  "company_name": "string",
  "contact_name": "string or null",
  "contact_title": "string or null",
  "team_size": "integer or null",
  "team_breakdown": "string or null (e.g., '15 field, 5 office')",
  "location": "string or null",
  "vertical": "string or null (e.g., 'commercial HVAC', 'residential plumbing')",
  "current_software": ["array", "of", "strings"],
  "pain_points": ["array", "of", "strings"],
  "interest_areas": ["array", "of", "strings"],
  "budget_mentioned": "string or null",
  "timeline": "string or null",
  "decision_makers": ["array", "of", "strings"],
  "next_step": "demo | follow_up_call | send_info | proposal | none",
  "next_step_date": "string or null",
  "next_step_notes": "string or null",
  "intent_level": "high | medium | low | unknown",
  "key_quotes": ["array", "of", "notable", "verbatim", "quotes"],
  "competitors_mentioned": ["array", "of", "strings"]
}

Rules:
- Only output JSON, no explanations
- Use null for missing information, don't guess
- Extract verbatim quotes that reveal intent or pain
- Normalize software names (e.g., "ST" → "ServiceTitan")
- Be conservative with intent_level unless signals are clear"""

def format_for_training(transcript: str, extraction: dict) -> dict:
    """Format a single example for Unsloth training."""
    return {
        "conversations": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": transcript.strip()
            },
            {
                "role": "assistant",
                "content": json.dumps(extraction, indent=2)
            }
        ]
    }

# =============================================================================
# MAIN GENERATION PIPELINE
# =============================================================================

async def generate_all_data():
    """Main function to generate training data."""
    
    print("="*60)
    print("TRAINING DATA GENERATOR")
    print("="*60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    all_examples = []
    
    # Load seed examples from file if it exists
    seed_file = Path(CONFIG["seed_file"])
    if seed_file.exists():
        print(f"Loading seeds from {seed_file}...")
        with open(seed_file) as f:
            seeds = json.load(f)
    else:
        print("Using built-in seed examples...")
        print("TIP: Create seed_examples.json with your real CRM data for better results")
        seeds = SEED_EXAMPLES
    
    print(f"Loaded {len(seeds)} seed examples")
    print()
    
    # Step 1: Add seed examples directly
    print("Step 1: Adding seed examples...")
    for seed in seeds:
        formatted = format_for_training(seed["transcript"], seed["extraction"])
        all_examples.append(formatted)
    print(f"  Added {len(seeds)} seed examples")
    print()
    
    # Step 2: Generate LLM variations
    print(f"Step 2: Generating LLM variations ({CONFIG['variations_per_seed']} per seed)...")
    
    # Select generation function based on provider
    if CONFIG["api_provider"] == "anthropic":
        generate_func = generate_variations_anthropic
    else:
        generate_func = generate_variations_openai
    
    variation_count = 0
    for i, seed in enumerate(seeds):
        print(f"  Processing seed {i+1}/{len(seeds)}...", end=" ")
        
        try:
            variations = await generate_func(
                seed["transcript"],
                seed["extraction"],
                CONFIG["variations_per_seed"]
            )
            
            for transcript, extraction in variations:
                formatted = format_for_training(transcript, extraction)
                all_examples.append(formatted)
                variation_count += 1
            
            print(f"generated {len(variations)} variations")
            
        except Exception as e:
            print(f"ERROR: {e}")
            continue
    
    print(f"  Total LLM variations: {variation_count}")
    print()
    
    # Step 3: Generate template-based examples
    print(f"Step 3: Generating template-based examples ({CONFIG['template_examples']})...")
    
    for _ in range(CONFIG["template_examples"]):
        transcript, extraction = generate_transcript_template()
        formatted = format_for_training(transcript, extraction)
        all_examples.append(formatted)
    
    print(f"  Added {CONFIG['template_examples']} template examples")
    print()
    
    # Step 4: Deduplicate
    print("Step 4: Deduplicating...")
    
    seen_hashes = set()
    unique_examples = []
    
    for example in all_examples:
        # Hash based on transcript content
        content = example["conversations"][1]["content"]
        content_hash = hashlib.md5(content.encode()).hexdigest()
        
        if content_hash not in seen_hashes:
            seen_hashes.add(content_hash)
            unique_examples.append(example)
    
    removed = len(all_examples) - len(unique_examples)
    print(f"  Removed {removed} duplicates")
    print()
    
    # Step 5: Quality filtering
    print("Step 5: Quality filtering...")
    
    filtered_examples = []
    for example in unique_examples:
        transcript = example["conversations"][1]["content"]
        
        # Length check
        if len(transcript) < CONFIG["min_transcript_length"]:
            continue
        if len(transcript) > CONFIG["max_transcript_length"]:
            continue
        
        # Check extraction is valid JSON
        try:
            extraction = json.loads(example["conversations"][2]["content"])
            if not extraction.get("company_name"):
                continue
        except:
            continue
        
        filtered_examples.append(example)
    
    removed = len(unique_examples) - len(filtered_examples)
    print(f"  Removed {removed} low-quality examples")
    print()
    
    # Step 6: Shuffle and save
    print(f"Step 6: Saving to {CONFIG['output_file']}...")
    
    random.shuffle(filtered_examples)
    
    with open(CONFIG["output_file"], "w") as f:
        for example in filtered_examples:
            f.write(json.dumps(example) + "\n")
    
    print(f"  Saved {len(filtered_examples)} examples")
    print()
    
    # Summary
    print("="*60)
    print("GENERATION COMPLETE")
    print("="*60)
    print(f"""
Summary:
  - Seed examples: {len(seeds)}
  - LLM variations: {variation_count}
  - Template examples: {CONFIG['template_examples']}
  - After dedup: {len(unique_examples)}
  - After filtering: {len(filtered_examples)}
  
Output file: {CONFIG['output_file']}

Next steps:
  1. Review a sample of examples for quality
  2. Run the Unsloth training notebook
  3. Adjust and regenerate if needed

Estimated training time: {len(filtered_examples) // 100 * 5}-{len(filtered_examples) // 100 * 10} minutes on T4 GPU
""")
    
    return filtered_examples

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def preview_data(filepath: str = "training_data.jsonl", n: int = 3):
    """Preview generated training data."""
    
    print(f"Preview of {filepath}:")
    print("="*60)
    
    with open(filepath) as f:
        for i, line in enumerate(f):
            if i >= n:
                break
            
            example = json.loads(line)
            transcript = example["conversations"][1]["content"]
            extraction = example["conversations"][2]["content"]
            
            print(f"\nExample {i+1}:")
            print("-"*40)
            print(f"TRANSCRIPT ({len(transcript)} chars):")
            print(transcript[:300] + "..." if len(transcript) > 300 else transcript)
            print()
            print("EXTRACTION:")
            print(extraction[:500] + "..." if len(extraction) > 500 else extraction)
            print()

def validate_data(filepath: str = "training_data.jsonl"):
    """Validate generated training data."""
    
    print(f"Validating {filepath}...")
    
    total = 0
    valid = 0
    issues = []
    
    with open(filepath) as f:
        for i, line in enumerate(f):
            total += 1
            try:
                example = json.loads(line)
                
                # Check structure
                assert "conversations" in example
                assert len(example["conversations"]) == 3
                assert example["conversations"][0]["role"] == "system"
                assert example["conversations"][1]["role"] == "user"
                assert example["conversations"][2]["role"] == "assistant"
                
                # Check extraction is valid JSON
                extraction = json.loads(example["conversations"][2]["content"])
                assert "company_name" in extraction
                
                valid += 1
                
            except Exception as e:
                issues.append((i+1, str(e)))
    
    print(f"\nValidation Results:")
    print(f"  Total examples: {total}")
    print(f"  Valid: {valid}")
    print(f"  Invalid: {total - valid}")
    
    if issues[:5]:
        print(f"\nFirst 5 issues:")
        for line_num, error in issues[:5]:
            print(f"  Line {line_num}: {error}")

# =============================================================================
# RUN
# =============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "preview":
            preview_data()
        elif command == "validate":
            validate_data()
        elif command == "template-only":
            # Just generate template examples (no API needed)
            print("Generating template-only dataset...")
            examples = []
            for _ in range(500):
                transcript, extraction = generate_transcript_template()
                examples.append(format_for_training(transcript, extraction))
            
            random.shuffle(examples)
            with open(CONFIG["output_file"], "w") as f:
                for ex in examples:
                    f.write(json.dumps(ex) + "\n")
            print(f"Saved {len(examples)} template examples to {CONFIG['output_file']}")
        else:
            print(f"Unknown command: {command}")
            print("Usage: python generate_training_data.py [preview|validate|template-only]")
    else:
        # Run full generation
        asyncio.run(generate_all_data())
