#!/usr/bin/env python3
"""Generate TTS audio files for the Pismo Disputes presentation."""

import subprocess
import os
import re

# Audio output directories
AUDIO_DIR = "presentation/assets/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Voice mappings
VOICES = {
    "ALEX": "en-US-GuyNeural",
    "JORDAN": "en-US-JennyNeural"
}

# Script lines by slide
SCRIPT = {
    1: [
        ("ALEX", "Hey everyone, welcome to our deep dive into the Pismo Disputes workflow. I'm Alex, and I'll be your guide through the state machine, API endpoints, and all the technical details that make this system tick."),
        ("JORDAN", "And I'm Jordan. I'll be covering the UX side of things, showing you how to translate all that technical goodness into interfaces that your users will actually enjoy. Or at least, not actively dislike."),
        ("ALEX", "Ha! Setting the bar high there, Jordan. But honestly, that's a realistic goal. By the end of this presentation, you'll know exactly how to build dispute workflow dialogs that handle every state, every edge case, and every network quirk."),
        ("JORDAN", "Think of it as your blueprint for building a disputes system that doesn't make bank operators want to throw their monitors out the window."),
        ("ALEX", "That's oddly specific. Speaking from experience?"),
        ("JORDAN", "Let's just say I've seen some things. Anyway, let's get into it!"),
    ],
    2: [
        ("JORDAN", "So before we dive into the technical weeds, let's talk about what we're actually dealing with. Disputes happen when a cardholder looks at their statement and goes, Wait, I didn't buy that."),
        ("ALEX", "Exactly. Or, I definitely returned that item. Or my personal favorite, Why am I still being charged for this subscription I cancelled three months ago?"),
        ("JORDAN", "We've all been there, right? Basically, any time there's a disagreement about a card transaction, that's a dispute."),
        ("ALEX", "And here's why this matters to the business. Global chargeback volume exceeds two hundred billion dollars annually."),
        ("JORDAN", "Wait, two hundred billion with a B? That's not a typo?"),
        ("ALEX", "Not a typo. Two hundred billion. So yeah, for issuers, handling disputes efficiently isn't just about customer service. It's about recovering funds, maintaining network compliance, and avoiding penalty fees."),
        ("JORDAN", "Plus, a bad disputes experience can tank your customer satisfaction scores faster than you can say chargeback rejected."),
        ("ALEX", "Exactly what Jordan said. This stuff really matters."),
    ],
    3: [
        ("ALEX", "Let's break down the three main categories of disputes you'll encounter. First up: Merchant Error. This is when the merchant genuinely messed something up."),
        ("JORDAN", "Right, wrong amount charged, duplicate transactions, goods that never arrived. These are usually the most straightforward because there's a clear paper trail."),
        ("ALEX", "Building on that, the second category is Identity Fraud. This is the scary one where someone's card details get stolen and used without authorization."),
        ("JORDAN", "Ooh, the scary one. These disputes require the most evidence because you're essentially saying a crime occurred. Cardholder statements, police reports, IP logs. The more documentation, the better."),
        ("ALEX", "And then there's the controversial third type: Friendly Fraud. This is when the cardholder actually did make the purchase but disputes it anyway."),
        ("JORDAN", "Ah yes, friendly fraud. Such a friendly name for something so frustrating. Maybe they forgot about the purchase, maybe buyer's remorse kicked in, or maybe they're just hoping for free stuff."),
        ("ALEX", "And that's exactly why your UI needs to handle all three types gracefully. Each one has a different evidence trail and resolution path."),
    ],
    4: [
        ("ALEX", "Alright, time for my favorite part. The PRIMITIVE state machine is Pismo's core architecture for managing dispute lifecycles."),
        ("JORDAN", "PRIMITIVE? Really? What it lacks in naming transparency, it definitely makes up for in flexibility. This thing is designed to let issuers build their own workflows on top of it."),
        ("ALEX", "Yeah, the name takes some getting used to. But here's the key concept: disputes move through states via events. You fire an event, the system validates the transition, and the dispute lands in a new state."),
        ("JORDAN", "So it's like a choose your own adventure book, but for financial disputes."),
        ("ALEX", "Ha! Kind of. The state machine has eight major groups. Think of them like chapters in a book, except this book has multiple endings."),
        ("JORDAN", "And some of those endings are sad. Lost disputes, expired deadlines. Not fun."),
        ("ALEX", "Exactly. The groups are OPEN, CARDNETWORK_CHARGEBACK, SECOND_PRESENTMENT, PREARBITRATION, DENIED, FAILED, LOSS, and WON. We'll cover each one."),
    ],
    5: [
        ("ALEX", "Let's walk through each state group. OPEN is where everything begins. It contains the PENDING state, essentially the dispute's waiting room before submission."),
        ("JORDAN", "Right, the waiting room. CARDNETWORK_CHARGEBACK is where things get active. This includes OPENED, CHARGEBACK_CREATED, and CHARGEBACK_PENDING_DOCUMENTATION."),
        ("ALEX", "Then CARDNETWORK_SECOND_PRESENTMENT kicks in when the acquirer decides to fight back. They're saying, Nope, this chargeback isn't valid."),
        ("JORDAN", "Oh, so now they want to argue about it. Fun times. And CARDNETWORK_PREARBITRATION is the escalation zone when second presentment didn't resolve things."),
        ("ALEX", "That's where the card network makes the final call. Judge, jury, and executioner."),
        ("JORDAN", "Then we have our terminal groups. DENIED means canceled, FAILED means something went wrong, LOSS means the issuer lost."),
        ("ALEX", "And WON means party time! Well, as much of a party as recovering disputed funds can be."),
        ("JORDAN", "Your UI needs to clearly communicate which outcome occurred and what it means financially. No ambiguity allowed."),
    ],
    6: [
        ("JORDAN", "Let's zoom out and look at the big picture. The dispute workflow has four main phases that every dispute passes through."),
        ("ALEX", "Phase one is Dispute Creation. The cardholder contacts their bank, the operator creates a dispute, evidence gets uploaded, and the OPEN event fires."),
        ("JORDAN", "Phase two is Network Processing. Pismo takes the ball and runs it over to the card network. They respond with either an acceptance or rejection."),
        ("ALEX", "Phase three is Resolution, and here's where it gets interesting. It can go multiple rounds. The acquirer might accept, contest, or let it expire."),
        ("JORDAN", "Multiple rounds? Like a boxing match?"),
        ("ALEX", "Kind of, yeah. Back and forth until someone wins or the deadline hits."),
        ("JORDAN", "Phase four is Terminal States. Won, lost, canceled, or failed. Your UI needs to guide users through each phase with clear status indicators."),
        ("ALEX", "And the whole process can take anywhere from a few days to several months. Build your UI with that timeline in mind."),
        ("JORDAN", "Months! That's why lifecycle visualization is so important. Users need to know where they are in the journey."),
    ],
    7: [
        ("ALEX", "Let's get hands-on. Creating a dispute starts with a POST request to the disputes endpoint. You need account ID, transaction ID, and reason code."),
        ("JORDAN", "From the UI side, this is our Dispute Creation Dialog. We use a Shadcn Dialog component with form inputs for each required field."),
        ("ALEX", "Once the API returns successfully, the dispute lands in PENDING status. This is where you can add evidence and prep everything before submission."),
        ("JORDAN", "Our mockup shows a clean three-section form. Transaction details, dispute type, and evidence checklist. Nice and organized."),
        ("ALEX", "Pro tip: validate everything client-side before hitting the API. Nothing frustrates operators more than filling out a whole form and getting an error at the end."),
        ("JORDAN", "Oh, absolutely. Been there, felt that pain. We also show a What's Next panel that explains the PENDING state."),
        ("ALEX", "That's a nice touch. Transparency builds trust with your operators."),
    ],
    8: [
        ("JORDAN", "Evidence is the lifeblood of disputes. Without proper documentation, even legitimate chargebacks get rejected."),
        ("ALEX", "Right, and that's why we need to make evidence upload as smooth as possible. The API endpoint is POST to disputes slash ID slash files. PDFs up to ten megabytes, images up to five."),
        ("JORDAN", "Our UI shows a checklist generated from the reason code. Required documents and supporting documents clearly marked so operators know exactly what they need."),
        ("ALEX", "The drag-and-drop zone supports multi-file upload with progress indicators and status badges. Very modern."),
        ("JORDAN", "Thanks! We also include inline validation warnings. Catch errors before uploads waste everyone's time."),
        ("ALEX", "Smart. But here's an important point: the API validates technical requirements, not evidence quality. A blurry receipt will upload just fine."),
        ("JORDAN", "So we need to train operators to collect strong evidence. The UI can guide them, but judgment is still required."),
        ("ALEX", "Exactly. Technology plus training equals success."),
    ],
    9: [
        ("ALEX", "This is the point of no return. Once you fire the OPEN event, the dispute gets submitted to the card network."),
        ("JORDAN", "No pressure! Our confirmation dialog includes a final checklist review. All evidence, all forms, and a clear warning that this cannot be undone."),
        ("ALEX", "The API call is PUT to disputes slash ID slash status with event set to OPEN. Success means OPENED status."),
        ("JORDAN", "The mockup shows the dispute amount prominently, a timeline preview, and big clear action buttons. We want operators to feel confident clicking that submit button."),
        ("ALEX", "After opening, expect five to seven business days for network response. Though it varies by network and dispute type."),
        ("JORDAN", "Five to seven days of waiting. That's why we show a status banner saying Submitted to Network with an estimated timeline."),
        ("ALEX", "Managing expectations is key."),
        ("JORDAN", "Couldn't agree more. Under-promise, over-deliver."),
    ],
    10: [
        ("JORDAN", "Good news arrives! The network accepted the dispute and created a chargeback. CHARGEBACK_CREATED status."),
        ("ALEX", "This is the outcome everyone hopes for. Funds have been provisionally credited to the cardholder."),
        ("JORDAN", "Wait, provisionally? So it's not final?"),
        ("ALEX", "Right, provisionally because the merchant can still contest. It's not over until it's over."),
        ("JORDAN", "Good to know. Our Chargeback Review screen uses an Alert component with a green success banner and clear status badge. Celebrate the win, but show what comes next."),
        ("ALEX", "The response includes network reference number and accepted amount. Parse these carefully for the next steps."),
        ("JORDAN", "We show What Can Happen Next with three possible outcomes: merchant accepts the loss, merchant contests, or deadline expires."),
        ("ALEX", "About thirty percent of chargebacks get contested. So prepare your operators for that possibility."),
        ("JORDAN", "Thirty percent? That's higher than I expected!"),
    ],
    11: [
        ("ALEX", "Plot twist. The acquirer didn't accept. They've submitted a second presentment with counter-evidence."),
        ("JORDAN", "Oh no. So we're not done yet."),
        ("ALEX", "Not even close. This is SECOND_PRESENTMENT status with a critical deadline. Thirty to forty-five days to respond."),
        ("JORDAN", "And if you miss that deadline?"),
        ("ALEX", "You lose. Automatically. No appeals."),
        ("JORDAN", "Yikes. That's why our Alert Dialog has a prominent countdown timer. Days remaining and recommended actions, right up front."),
        ("ALEX", "The acquirer's evidence arrives through webhooks. Documents and rebuttal arguments that need to be surfaced in your UI."),
        ("JORDAN", "We do side-by-side evidence comparison so operators can see both sides and decide whether escalation is worth it."),
        ("ALEX", "Three options: Accept the loss, escalate to pre-arbitration, or do nothing and let it expire. And only one of those is good."),
        ("JORDAN", "I'm guessing expire is the bad one?"),
        ("ALEX", "Expire and accept loss are both bad. Escalation is the only way to keep fighting."),
    ],
    12: [
        ("ALEX", "We've escalated to pre-arbitration. PRE_ARBITRATION_OPENED status. Now the card network makes the final call."),
        ("JORDAN", "The final boss battle. But important note: pre-arbitration has fees."),
        ("ALEX", "Right, escalate and lose, you pay arbitration costs. Not cheap."),
        ("JORDAN", "So we communicate this risk clearly in our UI. No surprises."),
        ("ALEX", "The API requires comprehensive evidence and network-specific questions. Visa and Mastercard have different requirements here."),
        ("JORDAN", "Our wizard has three steps. Review existing evidence, add new documentation, and confirm with fee disclosure."),
        ("ALEX", "Thirty to forty-five days for the network decision. ACCEPTED means you won. DECLINED means you lost and you owe fees."),
        ("JORDAN", "Ouch. Our color-coded badges show which evidence was most relevant to each phase. Helps with learning for next time."),
        ("ALEX", "That's a great feature. Win or lose, there's always something to learn."),
    ],
    13: [
        ("JORDAN", "Every dispute eventually ends. Let's talk about what winning and losing actually look like."),
        ("ALEX", "Winning lands you in CHARGEBACK_ACCEPTED or PRE_ARBITRATION_ACCEPTED. Provisional credit becomes permanent. Money's in the bank."),
        ("JORDAN", "Love a happy ending. Our win summary shows a green badge, final amount recovered, and complete timeline of how we got there."),
        ("ALEX", "Losing is more varied though. EXPIRED, REJECTED, DECLINED, or ISSUER_LOSS. Each one needs different messaging."),
        ("JORDAN", "Right, expired means someone missed a deadline. That deserves a root cause analysis."),
        ("ALEX", "And network rejection might indicate weak evidence. Different problem, different solution."),
        ("JORDAN", "Financial reconciliation happens automatically on the backend, but we show the impact clearly. What was recovered? What was lost? What can we learn?"),
        ("ALEX", "That learning piece is huge. Every dispute is a data point for improving the next one."),
    ],
    14: [
        ("ALEX", "Let's talk network specifics, starting with Visa. They have some unique requirements around form submission."),
        ("JORDAN", "Visa loves their questionnaires. Collaboration questionnaires and Allocation questionnaires. Submit these before opening the dispute."),
        ("ALEX", "Collaboration forms gather fraud detection details. Allocation forms handle chip liability disputes."),
        ("JORDAN", "Our form wizard detects the reason code and shows the appropriate questionnaire with structured inputs. Less guesswork for operators."),
        ("ALEX", "Nice. Visa also has PRE_ARB_ALLOCATION which bypasses second presentment for certain disputes. A fast track of sorts."),
        ("JORDAN", "Oh interesting. So some disputes can skip straight to arbitration?"),
        ("ALEX", "Exactly. Account for this path in your state machine handling. Reason codes use dot notation by the way. Ten dot X for fraud, eleven for authorization, twelve for processing, thirteen for consumer."),
        ("JORDAN", "Got it. Ten dot something equals fraud. That's easy to remember."),
        ("ALEX", "And watch for VFMP cases. The Visa Fraud Monitoring Program has special requirements and faster processing."),
    ],
    15: [
        ("ALEX", "Next up is Mastercard. The big difference here is the EBDF form, Electronic Batch Dispute File."),
        ("JORDAN", "Another acronym to remember. What makes EBDF special?"),
        ("ALEX", "Every Mastercard dispute requires EBDF submission. It's not optional."),
        ("JORDAN", "Ah, so our UI needs to collect all those required fields upfront. Got it."),
        ("ALEX", "Mastercard also uses TQR4 reports for reconciliation. Integrate this data for comprehensive reporting."),
        ("JORDAN", "Reason codes use a four-digit format starting with forty-eight. Common ones include forty-eight fifty-three for defective merchandise."),
        ("ALEX", "Mastercard's process is more linear than Visa. Second presentment to pre-arbitration to decision. Fewer branching paths."),
        ("JORDAN", "That's actually easier to visualize. Our UI emphasizes EBDF fields with inline validation. Show errors immediately."),
        ("ALEX", "And watch for dispute fees. Mastercard charges for certain outcomes. Track them in reconciliation."),
        ("JORDAN", "More fees to track. Building on Alex's point, the reconciliation view really needs to surface these costs clearly."),
    ],
    16: [
        ("JORDAN", "Last is ELO, a Brazilian card network. Important for LATAM markets."),
        ("ALEX", "And here's the curveball: evidence uploads go through ELO's portal manually, not through Pismo's API."),
        ("JORDAN", "Wait, manual portal uploads? In twenty twenty-six?"),
        ("ALEX", "I know, I know. But that's how it works. Your UI needs to clearly indicate this is an external step."),
        ("JORDAN", "We use warning banners and confirmations so operators don't miss the portal upload step. Big red flags essentially."),
        ("ALEX", "Pismo still manages the lifecycle. Create, open, and track through Pismo. Evidence just lives outside the system."),
        ("JORDAN", "ELO reason codes use three digits. What's the breakdown?"),
        ("ALEX", "One hundreds for authorization, two hundreds for processing, three hundreds for consumer disputes, four hundreds for fraud."),
        ("JORDAN", "Easy pattern. For LATAM deployments, also consider Portuguese language support. Some documentation may need to be in Portuguese."),
        ("ALEX", "Good call. Localization matters."),
    ],
    17: [
        ("JORDAN", "Alright developers, let's get practical. You've seen the workflow, you've seen the states. Now let's build the actual components."),
        ("ALEX", "Your dialogs need to be state-aware. Pull the current status and render the appropriate component for that state."),
        ("JORDAN", "Shadcn building blocks: Dialog, Card, Badge, Button, Form components, and AlertDialog. These will get you ninety percent of the way there."),
        ("ALEX", "For timeline visualization, map states to state groups. Show current phase and possible next states. Give users that sense of progress."),
        ("JORDAN", "Action buttons should be smart. Grey out invalid actions, show helpful tooltips, and always confirm destructive actions."),
        ("ALEX", "Building on Jordan's point, form validation is critical. Check evidence requirements before allowing the OPEN event. Don't let operators shoot themselves in the foot."),
        ("JORDAN", "Handle loading states and errors gracefully. Network latency is real. Surface meaningful messages, not just spinner forever."),
        ("ALEX", "Error messages should tell users what to do next, not just what went wrong."),
        ("JORDAN", "Exactly! We're on the same page."),
    ],
    18: [
        ("ALEX", "Alright, we've covered a lot of ground. Let's wrap up with the key takeaways."),
        ("JORDAN", "First, understand the state machine. Eight groups with specific transitions. Map your UI to these groups and you'll have a solid foundation."),
        ("ALEX", "Second, network differences matter. Visa forms, Mastercard EBDF, ELO portal uploads. Handle all three and you'll be ready for any deployment."),
        ("JORDAN", "Third, evidence is everything. Strong documentation wins disputes. Guide your operators to collect the right evidence upfront."),
        ("ALEX", "Fourth, deadlines are critical. Build countdown timers and notifications. No one should ever miss a deadline because they forgot."),
        ("JORDAN", "Fifth, design for the full lifecycle. Disputes take months. Tell the complete story from start to finish."),
        ("ALEX", "And check the Pismo developer docs. Disputes overview and state machine reference are essential reading."),
        ("JORDAN", "Test with real scenarios in sandbox before going to production. Edge cases will find you if you don't find them first."),
        ("ALEX", "Great advice. Thanks for joining us everyone!"),
        ("JORDAN", "Happy coding! And may all your disputes resolve in your favor."),
    ],
}

def generate_audio(text, voice, output_path):
    """Generate audio file using edge-tts."""
    cmd = [
        "edge-tts",
        "--voice", voice,
        "--text", text,
        "--write-media", output_path
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"  Generated: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ERROR: {output_path} - {e.stderr.decode()}")
        return False

def main():
    total = 0
    success = 0

    for slide_num, lines in SCRIPT.items():
        print(f"\nSlide {slide_num}:")
        for i, (speaker, text) in enumerate(lines, 1):
            filename = f"slide{slide_num:02d}_{speaker.lower()}_{i:02d}.mp3"
            output_path = os.path.join(AUDIO_DIR, filename)
            voice = VOICES[speaker]
            total += 1
            if generate_audio(text, voice, output_path):
                success += 1

    print(f"\n{'='*50}")
    print(f"Generated {success}/{total} audio files")
    print(f"Output directory: {AUDIO_DIR}")

if __name__ == "__main__":
    main()
