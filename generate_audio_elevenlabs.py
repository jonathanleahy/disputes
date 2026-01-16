#!/usr/bin/env python3
"""Generate TTS audio using ElevenLabs API with emotions."""

import requests
import os
import time
import re

API_KEY = os.environ.get("ELEVENLABS_API_KEY", "your-api-key-here")
API_URL = "https://api.elevenlabs.io/v1/text-to-speech"

VOICES = {
    "ALEX": "onwK4e9ZLuTAKqWW03F9",  # Daniel - professional male
    "JORDAN": "XB0fDUnXU5powFXDhCwa"  # Charlotte - warm female
}

AUDIO_DIR = "presentation/assets/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Script lines by slide (copied from generate_audio.py)
SCRIPT = {
    1: [
        ("ALEX", "Hey everyone, welcome to our deep dive into the Pismo Disputes workflow. I'm Alex, and I'll be your guide through the state machine, API endpoints, and all the technical details that make this system tick."),
        ("JORDAN", "And I'm Jordan. I'll be covering the UX side of things, showing you how to translate all that technical goodness into interfaces that your users will actually enjoy. Or at least, not actively dislike."),
        ("ALEX", "That's setting the bar high, Jordan. By the end of this presentation, you'll know exactly how to build dispute workflow dialogs that handle every state, every edge case, and every network quirk."),
        ("JORDAN", "Think of it as your blueprint for building a disputes system that doesn't make bank operators want to throw their monitors out the window. Let's get into it."),
    ],
    2: [
        ("JORDAN", "So before we dive into the technical weeds, let's talk about what we're actually dealing with. Disputes happen when a cardholder looks at their statement and says, Wait, I didn't buy that."),
        ("ALEX", "Or I definitely returned that item, or Why am I still being charged for this subscription I cancelled three months ago? Basically, any time there's a disagreement about a card transaction."),
        ("JORDAN", "And here's why this matters to the business side. The global chargeback volume exceeds two hundred billion dollars annually. That's not a typo. Two hundred billion with a B."),
        ("ALEX", "For issuers, handling disputes efficiently isn't just about customer service. It's about recovering funds for cardholders, maintaining network compliance, and avoiding penalty fees."),
        ("JORDAN", "Plus, a bad disputes experience can tank your customer satisfaction scores faster than you can say chargeback rejected. So yeah, this stuff matters."),
    ],
    3: [
        ("ALEX", "Let's break down the three main categories of disputes you'll encounter. First up: Merchant Error. This is when the merchant genuinely messed something up."),
        ("JORDAN", "Wrong amount charged, duplicate transactions, goods that never arrived. These are usually the most straightforward disputes because there's a clear paper trail."),
        ("ALEX", "Second category is Identity Fraud. This is the scary one where someone's card details get stolen and used without authorization."),
        ("JORDAN", "These disputes require the most evidence because you're essentially saying a crime occurred. Cardholder statements, police reports, IP logs. The more documentation, the better."),
        ("ALEX", "And then there's the controversial third type: Friendly Fraud. This is when the cardholder actually did make the purchase but disputes it anyway."),
        ("JORDAN", "Maybe they forgot about it, maybe buyer's remorse kicked in, or maybe they're just hoping for free stuff. Your UI needs to handle all three types."),
    ],
    4: [
        ("ALEX", "Alright, time for my favorite part. The PRIMITIVE state machine is Pismo's core architecture for managing dispute lifecycles."),
        ("JORDAN", "What it lacks in naming transparency, it makes up for in flexibility. This thing is designed to let issuers build their own workflows on top of it."),
        ("ALEX", "Here's the key concept: disputes move through states via events. You fire an event, the system validates the transition, and the dispute lands in a new state."),
        ("JORDAN", "The state machine has eight major groups. Think of them like chapters in a book, except this book has multiple endings and some of them are sad."),
        ("ALEX", "The groups are OPEN, CARDNETWORK_CHARGEBACK, SECOND_PRESENTMENT, PREARBITRATION, DENIED, FAILED, LOSS, and WON. We'll cover each one."),
    ],
    5: [
        ("ALEX", "Let's walk through each state group. OPEN is where everything begins. It contains the PENDING state, the dispute's waiting room before submission."),
        ("JORDAN", "CARDNETWORK_CHARGEBACK is the active phase. This includes OPENED, CHARGEBACK_CREATED, and CHARGEBACK_PENDING_DOCUMENTATION."),
        ("ALEX", "CARDNETWORK_SECOND_PRESENTMENT kicks in when the acquirer decides to fight back. They're saying, Nope, this chargeback isn't valid."),
        ("JORDAN", "CARDNETWORK_PREARBITRATION is the escalation zone. If second presentment didn't resolve things, this is where the card network makes the final call."),
        ("ALEX", "Then we have our terminal groups. DENIED means canceled. FAILED means something went wrong. LOSS means the issuer lost. And WON means party time."),
        ("JORDAN", "Your UI needs to clearly communicate which outcome occurred and what it means financially."),
    ],
    6: [
        ("JORDAN", "Let's zoom out and look at the big picture. The dispute workflow has four main phases that every dispute passes through."),
        ("ALEX", "Phase one is Dispute Creation. The cardholder contacts their bank, the operator creates a dispute, evidence gets uploaded, and the OPEN event fires."),
        ("JORDAN", "Phase two is Network Processing. Pismo takes the ball and runs it over to the card network. They respond with either an acceptance or rejection."),
        ("ALEX", "Phase three is Resolution, and it can go multiple rounds. The acquirer might accept, contest, or let it expire."),
        ("JORDAN", "Phase four is Terminal States. Won, lost, canceled, or failed. Your UI needs to guide users through each phase."),
        ("ALEX", "The whole process can take anywhere from a few days to several months. Build your UI with that timeline in mind."),
    ],
    7: [
        ("ALEX", "Let's get hands-on. Creating a dispute starts with a POST request to the disputes endpoint. You need account ID, transaction ID, and reason code."),
        ("JORDAN", "From the UI side, this is our Dispute Creation Dialog. We use a Shadcn Dialog component with form inputs for each required field."),
        ("ALEX", "Once the API returns successfully, the dispute lands in PENDING status. This is where you can add evidence and prep everything."),
        ("JORDAN", "Our mockup shows a clean three-section form. Transaction details, dispute type, and evidence checklist."),
        ("ALEX", "Pro tip: validate everything client-side before hitting the API. Nothing frustrates operators more than form errors at the end."),
        ("JORDAN", "We also show a What's Next panel that explains the PENDING state. Transparency builds trust."),
    ],
    8: [
        ("JORDAN", "Evidence is the lifeblood of disputes. Without proper documentation, even legitimate chargebacks get rejected."),
        ("ALEX", "The API endpoint is POST to disputes slash ID slash files. PDFs up to ten megabytes, images up to five."),
        ("JORDAN", "Our UI shows a checklist generated from the reason code. Required documents and supporting documents clearly marked."),
        ("ALEX", "The drag-and-drop zone supports multi-file upload with progress indicators and status badges."),
        ("JORDAN", "We include inline validation warnings. Catch errors before uploads waste time."),
        ("ALEX", "Remember: the API validates technical requirements, not evidence quality. Train operators to collect strong evidence."),
    ],
    9: [
        ("ALEX", "This is the point of no return. Once you fire the OPEN event, the dispute gets submitted to the card network."),
        ("JORDAN", "Our confirmation dialog includes a final checklist review. All evidence, all forms, and a clear warning this cannot be undone."),
        ("ALEX", "The API call is PUT to disputes slash ID slash status with event set to OPEN. Success means OPENED status."),
        ("JORDAN", "The mockup shows the dispute amount prominently, a timeline, and big clear action buttons."),
        ("ALEX", "After opening, expect five to seven business days for network response. Varies by network and dispute type."),
        ("JORDAN", "We show a status banner saying Submitted to Network with an estimated timeline. Managing expectations is key."),
    ],
    10: [
        ("JORDAN", "Good news arrives. The network accepted the dispute and created a chargeback. CHARGEBACK_CREATED status."),
        ("ALEX", "Funds have been provisionally credited to the cardholder. Provisionally because the merchant can still contest."),
        ("JORDAN", "Our Chargeback Review screen uses an Alert component. Green success banner and clear status badge."),
        ("ALEX", "The response includes network reference number and accepted amount. Parse these carefully for next steps."),
        ("JORDAN", "We show What Can Happen Next with three outcomes: accept loss, contest, or expire."),
        ("ALEX", "About thirty percent of chargebacks get contested. Prepare operators for that possibility."),
    ],
    11: [
        ("ALEX", "Plot twist. The acquirer didn't accept. They've submitted a second presentment with counter-evidence."),
        ("JORDAN", "This is SECOND_PRESENTMENT status with a critical deadline. Thirty to forty-five days to respond. Miss it and you lose."),
        ("ALEX", "The acquirer's evidence arrives through webhooks. Documents and rebuttal arguments that need to be surfaced in your UI."),
        ("JORDAN", "Our Alert Dialog has a prominent countdown timer. Days remaining and recommended actions."),
        ("ALEX", "Three options: Accept loss, escalate to pre-arbitration, or do nothing and expire. Only one is good."),
        ("JORDAN", "Side-by-side evidence comparison helps operators decide whether escalation is worth it."),
    ],
    12: [
        ("ALEX", "We've escalated to pre-arbitration. PRE_ARBITRATION_OPENED status. The card network makes the final call."),
        ("JORDAN", "Important: pre-arbitration has significant fees. Visa charges two-fifty to five hundred dollars, Mastercard charges one-fifty to four hundred. If you lose, that fee is gone plus the dispute amount. Win rates hover around forty to fifty percent, so only escalate with strong evidence."),
        ("ALEX", "The API requires comprehensive evidence and network-specific questions. Visa and Mastercard have different requirements."),
        ("JORDAN", "Our wizard has three steps. Review evidence, add documentation, confirm with fee disclosure."),
        ("ALEX", "Thirty to forty-five days for the network decision. ACCEPTED means you won. DECLINED means you lost."),
        ("JORDAN", "Color-coded badges show which evidence was most relevant to each phase."),
    ],
    13: [
        ("JORDAN", "Every dispute eventually ends. Let's talk about what winning and losing actually look like."),
        ("ALEX", "Winning lands you in CHARGEBACK_ACCEPTED or PRE_ARBITRATION_ACCEPTED. Provisional credit becomes permanent."),
        ("JORDAN", "Our win summary shows a green badge, final amount recovered, and complete timeline."),
        ("ALEX", "Losing is more varied. EXPIRED, REJECTED, DECLINED, or ISSUER_LOSS. Each needs different messaging."),
        ("JORDAN", "Missing a deadline deserves root cause analysis. Network rejection might indicate weak evidence."),
        ("ALEX", "Financial reconciliation happens automatically, but show the impact clearly. What was recovered? What was lost?"),
    ],
    14: [
        ("ALEX", "Let's talk network specifics, starting with Visa. They have unique requirements around form submission."),
        ("JORDAN", "Visa uses Collaboration questionnaires and Allocation questionnaires. Submit these before opening the dispute."),
        ("ALEX", "Collaboration forms gather fraud detection details. Allocation forms handle chip liability disputes."),
        ("JORDAN", "Our form wizard detects the reason code and shows the appropriate questionnaire with structured inputs."),
        ("ALEX", "Visa has PRE_ARB_ALLOCATION which bypasses second presentment for certain disputes. Account for this path."),
        ("JORDAN", "Reason codes use dot notation. Ten dot X for fraud, eleven for authorization, twelve for processing, thirteen for consumer."),
        ("ALEX", "Watch for VFMP cases. The Visa Fraud Monitoring Program has special requirements and faster processing."),
    ],
    15: [
        ("ALEX", "Next is Mastercard. The big difference is the EBDF form, Electronic Batch Dispute File."),
        ("JORDAN", "Every Mastercard dispute requires EBDF submission. Your UI needs to collect all required fields."),
        ("ALEX", "Mastercard uses TQR4 reports for reconciliation. Integrate this data for comprehensive reporting."),
        ("JORDAN", "Reason codes use four-digit format starting with forty-eight. Common ones include forty-eight fifty-three."),
        ("ALEX", "Mastercard's process is more linear than Visa. Second presentment to pre-arbitration to decision."),
        ("JORDAN", "Our UI emphasizes EBDF fields with inline validation. Show errors immediately."),
        ("ALEX", "Watch for dispute fees. Mastercard charges for certain outcomes. Track them in reconciliation."),
    ],
    16: [
        ("JORDAN", "Last is ELO, a Brazilian card network. Important for LATAM markets."),
        ("ALEX", "The biggest difference: evidence uploads go through ELO's portal manually, not through Pismo's API."),
        ("JORDAN", "Yes, manual portal uploads. Your UI needs to clearly indicate this is an external step."),
        ("ALEX", "Pismo still manages the lifecycle. Create, open, and track through Pismo. Evidence lives outside."),
        ("JORDAN", "We use warning banners and confirmations so operators don't miss the portal upload step."),
        ("ALEX", "ELO codes use three digits. One hundreds for authorization, two hundreds for processing, three hundreds for consumer, four hundreds for fraud."),
        ("JORDAN", "For LATAM, consider Portuguese language support. Some documentation may need to be in Portuguese."),
    ],
    17: [
        ("JORDAN", "Alright developers, let's get practical. You've seen the workflow. Now let's build the components."),
        ("ALEX", "Your dialogs need to be state-aware. Pull the status and render the appropriate component."),
        ("JORDAN", "Shadcn building blocks: Dialog, Card, Badge, Button, Form components, and AlertDialog."),
        ("ALEX", "For timeline visualization, map to state groups. Show current phase and possible next states."),
        ("JORDAN", "Action buttons should be smart. Grey out invalid actions. Show tooltips. Confirm destructive actions."),
        ("ALEX", "Form validation is critical. Check evidence requirements before allowing the OPEN event."),
        ("JORDAN", "Handle loading states and errors gracefully. Network latency is real. Surface meaningful messages."),
    ],
    18: [
        ("ALEX", "We've covered a lot. Let's wrap up with key takeaways."),
        ("JORDAN", "First, understand the state machine. Eight groups with specific transitions. Map your UI to these groups."),
        ("ALEX", "Second, network differences matter. Visa forms, Mastercard EBDF, ELO portal uploads. Handle all three."),
        ("JORDAN", "Third, evidence is everything. Strong documentation wins. Guide operators to collect the right evidence."),
        ("ALEX", "Fourth, deadlines are critical. Build countdown timers and notifications to keep operators on track."),
        ("JORDAN", "Fifth, design for the full lifecycle. Disputes take months. Tell the complete story."),
        ("ALEX", "Check the Pismo developer docs. Disputes overview and state machine reference are essential reading."),
        ("JORDAN", "Test with real scenarios in sandbox. Edge cases will find you in production if you don't find them first. Happy coding!"),
    ],
}


def get_emotion_settings(text):
    """Determine voice settings based on content."""
    text_lower = text.lower()

    # Default settings
    settings = {
        "stability": 0.5,
        "similarity_boost": 0.8,
        "style": 0.5,
        "use_speaker_boost": True
    }

    # Adjust based on content
    if any(word in text_lower for word in ["billion", "200", "percent", "million"]):
        settings["style"] = 0.7  # More emphatic for statistics
    elif any(word in text_lower for word in ["fraud", "crime", "stolen", "unauthorized"]):
        settings["style"] = 0.4  # More serious
        settings["stability"] = 0.6
    elif any(word in text_lower for word in ["won", "win", "accepted", "success", "party"]):
        settings["style"] = 0.8  # Upbeat
    elif any(word in text_lower for word in ["lost", "loss", "rejected", "deadline", "miss", "expire"]):
        settings["style"] = 0.6  # Concerned
        settings["stability"] = 0.55
    elif any(word in text_lower for word in ["welcome", "hello", "hey everyone", "i'm"]):
        settings["style"] = 0.7  # Friendly

    return settings


def generate_audio(text, voice_id, output_path):
    """Generate audio using ElevenLabs API."""
    settings = get_emotion_settings(text)

    response = requests.post(
        f"{API_URL}/{voice_id}",
        headers={
            "xi-api-key": API_KEY,
            "Content-Type": "application/json"
        },
        json={
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": settings
        }
    )

    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"  Generated: {output_path}")
        return True
    else:
        print(f"  ERROR: {response.status_code} - {response.text}")
        return False


def main():
    total = 0
    success = 0

    for slide_num, lines in SCRIPT.items():
        print(f"\nSlide {slide_num}:")
        for i, (speaker, text) in enumerate(lines, 1):
            filename = f"slide{slide_num:02d}_{speaker.lower()}_{i:02d}.mp3"
            output_path = os.path.join(AUDIO_DIR, filename)
            voice_id = VOICES[speaker]
            total += 1

            if generate_audio(text, voice_id, output_path):
                success += 1

            time.sleep(0.5)  # Rate limiting

    print(f"\n{'='*50}")
    print(f"Generated {success}/{total} audio files")


if __name__ == "__main__":
    main()
