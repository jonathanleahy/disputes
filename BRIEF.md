# Pismo Disputes Workflow Presentation - Project Brief

## Overview

Create an **in-depth investigation** and interactive HTML/CSS presentation that walks developers through the Pismo Disputes workflow system. The presentation must come across as **professional, crisp, and clear** while maintaining an engaging two-host conversational format.

The presentation will help developers understand the state machine, transitions, and UI patterns needed for building workflow dialogs in the final React/Shadcn application.

---

## Target Audience

**Primary**: Developers who will be creating workflow dialogs for a Disputes Management System
**Context**: These developers need to understand:
- The Pismo PRIMITIVE state machine (comprehensive coverage)
- State transitions and events for ALL card networks
- Network-specific workflows (Visa, Mastercard, ELO) - dedicated sections for each
- UI patterns for each workflow step (React/Shadcn style)

---

## User Requirements (Answers to Clarifying Questions)

| Question | Answer |
|----------|--------|
| **TTS Tool** | Edge TTS - Free Microsoft Azure voices via edge-tts CLI |
| **Presentation Scope** | Full walkthrough, all networks (15-20 slides) |
| **Mockup Style** | Polished UI mockups - React/Shadcn style to match final application |
| **Host Tone** | Conversational/playful - Light banter between hosts, some humor |
| **Overall Quality** | Professional, crisp, and clear - in-depth investigation |

---

## Technical Requirements

### Stack
- **HTML5** - Semantic markup
- **Tailwind CSS** - Styling framework (via CDN)
- **GSAP** - Animation library (via CDN)
- **Light Mode** - Clean, professional appearance

### Voice/Audio Requirements
- **Text-to-Speech**: ElevenLabs API v2 (eleven_multilingual_v2 model for higher quality)
- **Pre-generated Audio**: All voice audio files must be pre-created and bundled with presentation
- **Preloading**: Audio files must be preloaded on presentation start to prevent buffering
- **Two Distinct Voices**:
  - Host A (Alex): Technical lead - use "Daniel" voice (voice ID: onwK4e9ZLuTAKqWW03F9) - professional male
  - Host B (Jordan): UX specialist - use "Charlotte" voice (voice ID: XB0fDUnXU5powFXDhCwa) - warm, friendly female
- **Emotional Delivery**: Vary tone based on content context (excited for wins, serious for losses, friendly introductions)
- **Dialogue Interaction**: Natural pauses and reactions between hosts
- **Generation**: Use ElevenLabs API v2 to generate MP3 files per slide segment with voice settings:
  - stability: 0.5
  - similarity_boost: 0.8
  - style: 0.5 (expressiveness)
  - use_speaker_boost: True
- **API Key**: Stored securely in environment variable ELEVENLABS_API_KEY

### Presentation Features
- Slide-based navigation (keyboard + click)
- GSAP animations for transitions and reveals
- Interactive workflow diagrams
- Screenshot mockups of potential UI
- State machine visualization (D3.js with dagre layout)
- Play/pause controls for narration
- Auto-advance option with voice sync
- **Synchronized Content Reveal**: Cards and content appear as the speaker discusses them
- **Avatar Speech Bubbles**: Show speaker avatar with speech bubble containing current dialogue
- **Highlighting**: Elements highlight when being discussed
- **Micro-animations**: Icons and visual elements animate contextually
- **Slide Numbers**: Every slide shows "Slide X of 18"

---

## Enhanced Presentation Features (v2)

### Audio Enhancements
- **ElevenLabs API**: Use eleven_multilingual_v2 model for higher quality
- **Emotions in Speech**: Add emotional delivery - excited for wins, serious for losses, friendly introductions
- **Voice Selection**:
  - Alex: Use "Daniel" voice (more professional male voice)
  - Jordan: Use "Charlotte" voice (warm, friendly female)
- **Dialogue Interaction**: Hosts should respond to each other naturally, with pauses and reactions

### Visual Icon Animations
- **Contextual Icons**: Display relevant SVG icons/emojis before text reveals
- **Icon Flow**: Icons fade/slide in → hold briefly → fade out as content appears
- **Memory Aids**: Use visual symbols to reinforce key concepts:
  - Credit card icon for disputes
  - Shield icon for fraud
  - Clock icon for deadlines
  - Check/X icons for win/loss
  - Document icon for evidence
  - Network icons (Visa, Mastercard, ELO logos)

### Synchronized Content Reveal
- **Pre-reveal Hints**: Show icon/visual BEFORE the speaker discusses a topic
- **Text Emphasis**: Display key phrases or terms as the speaker says them
- **Sequenced Reveals**:
  1. Icon appears and pulses
  2. Speaker begins discussing topic
  3. Card/content fades in
  4. Icon fades out or moves to content

### Card Network Detail Slide
- Add a dedicated slide (slide 2.5 or modify intro) showing:
  - Visa, Mastercard, ELO logos prominently
  - Brief description of each network's quirks
  - Why network differences matter

### Micro-animations Throughout
- Subtle icon animations during speech
- Highlight effects on key terms
- Progress indicators for multi-step processes
- Gentle pulse effects on active elements

### Contextual Visual Illustrations
When slides have minimal content but speakers describe scenarios, show dynamic visuals:
- **Detailed Scene Illustrations**: Create rich SVG illustrations that depict the spoken scenario
- **NOT simple icons**: Full scene illustrations with multiple elements, depth, and context
- **Example**: When Alex says "Or I definitely returned that item, or Why am I still being charged for this subscription?" show:
  1. "Returned that item" → SVG scene of a package with return label, arrows, store backdrop
  2. "Subscription I cancelled" → SVG scene of a calendar with recurring charges, X mark, phone
  3. "Disagreement about a transaction" → SVG scene of receipt with question marks, confused face
- **Illustration Style**:
  - Flat design with subtle gradients
  - 2-3 color palette per illustration (grays + accent color)
  - 150-200px size for visibility
  - Scene composition with foreground/background elements
- **Parallax Effects**: Subtle depth movement on visuals
- **Timing**: Visuals appear/disappear synced with speech phrases
- **Generation**: Create SVGs programmatically based on sentence analysis
- **Layout**: Floating visuals positioned to complement content

### Interactive Host Dialogue
- **Natural Flow**: Hosts respond to each other's points without awkward gaps
- **Callbacks**: Reference what the other host just said ("Like Jordan mentioned...")
- **Shared Enthusiasm**: React to interesting facts ("Two hundred billion? That's huge!")
- **Handoffs**: Smooth transitions ("Speaking of which, Alex, tell us about...")
- **No Dead Air**: Always have visual or audio activity

---

## Audio Generation (ElevenLabs v2)

### API Configuration
```python
# Model: eleven_multilingual_v2 (newer, higher quality)
# Endpoint: POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}

voice_settings = {
    "stability": 0.5,
    "similarity_boost": 0.8,
    "style": 0.5,  # 0-1, controls expressiveness
    "use_speaker_boost": True
}

# Voice IDs (newer voices)
ALEX_VOICE = "onwK4e9ZLuTAKqWW03F9"  # Daniel
JORDAN_VOICE = "XB0fDUnXU5powFXDhCwa"  # Charlotte
```

### Emotional Delivery Guidelines
- **Introductions**: Warm, welcoming tone
- **Technical explanations**: Clear, measured pace
- **Statistics/Impact**: Slight emphasis, concern
- **Warnings/Deadlines**: Serious, urgent
- **Win scenarios**: Upbeat, satisfied
- **Loss scenarios**: Sympathetic, constructive
- **Humor moments**: Light, playful

---

## Content Structure

### Proposed Slides (18 slides)

1. **Title Slide** - "Pismo Disputes Workflow: A Developer's Guide"
2. **Introduction** - What are disputes? Why do they matter? Financial impact.
3. **Dispute Types** - Merchant Error, Identity Fraud, Friendly Fraud
4. **The PRIMITIVE State Machine** - Overview of states and groups
5. **State Groups Deep Dive** - OPEN, CARDNETWORK_CHARGEBACK, DENIED, FAILED, LOSS, WON
6. **Core Workflow Overview** - Cardholder → Issuer → Network → Resolution
7. **Step 1: Creating a Dispute** - API call, PENDING state, mockup
8. **Step 2: Uploading Evidence** - File uploads, evidence types, mockup
9. **Step 3: Opening the Dispute** - PENDING → OPENED transition, mockup
10. **Step 4: Chargeback Creation** - Network accepts, CHARGEBACK_CREATED, mockup
11. **Step 5: Second Presentment** - Acquirer contests, deadline tracking, mockup
12. **Step 6: Pre-Arbitration** - Escalation path, final resolution, mockup
13. **Resolution States** - WON vs LOSS scenarios, financial reconciliation
14. **Visa Workflow** - Collaboration/Allocation forms, specific codes
15. **Mastercard Workflow** - EBDF forms, TQR4 reports, specific codes
16. **ELO Workflow** - Portal uploads, LATAM considerations
17. **Building Your Dialogs** - UI patterns, Shadcn components, form requirements
18. **Key Takeaways & Resources** - Summary, API links, next steps

---

## Screenshot Mockups to Include

**Style**: Polished UI mockups matching React/Shadcn design system
- Use Shadcn/ui component patterns (Cards, Buttons, Forms, Tables, Badges)
- Tailwind CSS styling with consistent color palette
- Light mode with clean, professional appearance

For each workflow step, include a polished mockup showing:

1. **Dispute Creation Dialog** - Shadcn Dialog with form inputs, Select for reason codes
2. **Evidence Upload Screen** - Card layout with file dropzone, uploaded documents table
3. **Status Dashboard** - Timeline component, Badge states, action Button group
4. **Chargeback Review** - Alert component for network response, next steps cards
5. **Second Presentment Alert** - AlertDialog with deadline countdown, action buttons
6. **Pre-Arbitration Form** - Multi-step form wizard, evidence summary table
7. **Resolution Summary** - Card with final status Badge, financial impact display

---

## Speaker Notes Format

Two hosts will present with a **conversational/playful tone** - light banter but professional:
- **Host A (Alex)**: Technical lead, explains state machine and API details. Voice: Daniel (ElevenLabs)
- **Host B (Jordan)**: UX specialist, explains UI patterns and user experience. Voice: Charlotte (ElevenLabs)

Each slide will have alternating dialogue between both hosts with:
- Natural conversation flow
- Occasional light humor or relatable comments
- Clear transitions between technical and UX topics
- Professional delivery despite playful moments

---

## Project Structure

```
pismo-disputes-presentation/
├── BRIEF.md                 # This file
├── research/                # Background documentation
│   ├── pismo-api-summary.md
│   ├── state-machine.md
│   └── workflow-diagrams.md
├── presentation/            # Final presentation
│   ├── index.html
│   ├── styles.css           # Custom styles beyond Tailwind
│   ├── scripts.js           # GSAP animations and navigation
│   └── assets/
│       ├── mockups/         # UI mockup images (SVG/HTML)
│       └── audio/           # Pre-generated voice narration
│           ├── alex/        # Host A voice files
│           └── jordan/      # Host B voice files
└── speaker-notes/           # Presentation script
    └── script.md
```

---

## Subagent Assignments

| Agent | Responsibility |
|-------|---------------|
| **Research Agent** | Compile Pismo API documentation into research/ folder |
| **Architect Agent** | Design presentation structure and flow |
| **Designer Agent** | Create UI mockups and visual design system |
| **Developer Agent** | Build HTML/CSS/GSAP presentation |
| **Documentation Agent** | Write speaker notes with two-host dialogue |

---

## Workflow Diagrams to Include

### Main State Machine Flow
```
PENDING → OPENED → CHARGEBACK_CREATED → [ACCEPTED | SECOND_PRESENTMENT]
                                               ↓
                                    PRE_ARBITRATION_OPENED
                                               ↓
                                   [ACCEPTED | DECLINED]
```

### Decision Points
- After OPENED: Network accepts or rejects
- After CHARGEBACK_CREATED: Acquirer accepts loss or contests
- After SECOND_PRESENTMENT: Escalate, accept, or expire
- After PRE_ARBITRATION: Final network decision

---

## Success Criteria

1. Presentation runs smoothly in modern browsers
2. All animations enhance understanding without distracting
3. Mockups clearly illustrate UI patterns for each state
4. Speaker notes provide natural two-host dialogue
5. Developers can reference presentation when building dialogs

---

## Questions for User (Before Proceeding)

See AskUserQuestion tool call for 5 clarifying questions.

---

## Timeline Tracking

Work will be tracked via the TodoWrite tool with the following phases:
1. Research compilation
2. Presentation design
3. Mockup creation
4. Development
5. Speaker notes
6. Review and serve

---

## Audio Generation

### ElevenLabs v2 Setup
```bash
# Install elevenlabs Python SDK
pip install elevenlabs

# Set API key
export ELEVENLABS_API_KEY="your_api_key_here"
```

### Python Generation Script
```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])

# Voice IDs
ALEX_VOICE = "onwK4e9ZLuTAKqWW03F9"   # Daniel - professional male
JORDAN_VOICE = "XB0fDUnXU5powFXDhCwa"  # Charlotte - warm, friendly female

def generate_audio(text, voice_id, output_path):
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        text=text,
        voice_settings={
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.5,
            "use_speaker_boost": True
        }
    )
    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

# Generate audio for Alex
generate_audio(
    "Welcome to the Pismo Disputes workflow guide.",
    ALEX_VOICE,
    "alex_slide1.mp3"
)

# Generate audio for Jordan
generate_audio(
    "Let's explore how to build great dispute dialogs.",
    JORDAN_VOICE,
    "jordan_slide1.mp3"
)
```

### Audio File Naming Convention
```
presentation/assets/audio/
├── alex/
│   ├── slide01_intro.mp3
│   ├── slide02_intro.mp3
│   └── ...
└── jordan/
    ├── slide01_intro.mp3
    ├── slide02_intro.mp3
    └── ...
```

### Preloading Strategy
```javascript
// Preload all audio on page load
const audioFiles = [
  'assets/audio/alex/slide01_intro.mp3',
  'assets/audio/jordan/slide01_intro.mp3',
  // ... all files
];

audioFiles.forEach(src => {
  const audio = new Audio();
  audio.preload = 'auto';
  audio.src = src;
});
```

---

## Sources

- [Pismo Disputes Overview](https://developers.pismo.io/pismo-docs/docs/disputes-overview)
- [Pismo Disputes State Machine](https://developers.pismo.io/pismo-docs/docs/disputes-state-machine)
- Project research: `/home/jon/temp/disputes/projects/disputes/CLAUDE.md`
