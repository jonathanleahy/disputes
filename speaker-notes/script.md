# Pismo Disputes Workflow Presentation - Speaker Notes Script

**Hosts:**
- **Alex** - Technical Lead (male voice: en-US-GuyNeural)
- **Jordan** - UX Specialist (female voice: en-US-JennyNeural)

**Tone:** Conversational and playful with light banter, but professional delivery.

---

## [SLIDE 1] Title Slide
*"Pismo Disputes Workflow: A Developer's Guide"*

**ALEX:** Hey everyone, welcome to our deep dive into the Pismo Disputes workflow. I'm Alex, and I'll be your guide through the state machine, API endpoints, and all the technical details that make this system tick.

**JORDAN:** And I'm Jordan. I'll be covering the UX side of things, showing you how to translate all that technical goodness into interfaces that your users will actually enjoy. Or at least, not actively dislike.

**ALEX:** That's setting the bar high, Jordan. By the end of this presentation, you'll know exactly how to build dispute workflow dialogs that handle every state, every edge case, and every network quirk.

**JORDAN:** Think of it as your blueprint for building a disputes system that doesn't make bank operators want to throw their monitors out the window. Let's get into it.

---

## [SLIDE 2] Introduction
*What are disputes? Why do they matter? Financial impact.*

**JORDAN:** So before we dive into the technical weeds, let's talk about what we're actually dealing with. Disputes happen when a cardholder looks at their statement and says, "Wait, I didn't buy that."

**ALEX:** Or "I definitely returned that item," or "Why am I still being charged for this subscription I cancelled three months ago?" Basically, any time there's a disagreement about a card transaction.

**JORDAN:** And here's why this matters to the business side. The global chargeback volume exceeds two hundred billion dollars annually. That's not a typo. Two hundred billion with a B.

**ALEX:** For issuers, handling disputes efficiently isn't just about customer service. It's about recovering funds for cardholders, maintaining network compliance, and avoiding penalty fees. Get it wrong, and you're leaving money on the table.

**JORDAN:** Plus, a bad disputes experience can tank your customer satisfaction scores faster than you can say "chargeback rejected." So yeah, this stuff matters.

---

## [SLIDE 3] Dispute Types
*Merchant Error, Identity Fraud, Friendly Fraud*

**ALEX:** Let's break down the three main categories of disputes you'll encounter. First up: Merchant Error. This is when the merchant genuinely messed something up.

**JORDAN:** Wrong amount charged, duplicate transactions, goods that never arrived. These are usually the most straightforward disputes because there's a clear paper trail showing what went wrong.

**ALEX:** Second category is Identity Fraud. This is the scary one where someone's card details get stolen and used without authorization. Card-not-present fraud, counterfeit cards, the whole criminal enterprise thing.

**JORDAN:** These disputes require the most evidence because you're essentially saying a crime occurred. Cardholder statements, police reports, IP logs. The more documentation, the better.

**ALEX:** And then there's the controversial third type: Friendly Fraud. This is when the cardholder actually did make the purchase but disputes it anyway.

**JORDAN:** Maybe they forgot about it, maybe buyer's remorse kicked in, or maybe they're just hoping for free stuff. Either way, your UI needs to handle all three types while guiding operators through the right evidence collection for each.

---

## [SLIDE 4] The PRIMITIVE State Machine
*Overview of states and groups*

**ALEX:** Alright, time for my favorite part. The PRIMITIVE state machine is Pismo's core architecture for managing dispute lifecycles. And yes, PRIMITIVE is in all caps because it's an acronym. Probably. Pismo hasn't told me what it stands for.

**JORDAN:** What it lacks in naming transparency, it makes up for in flexibility. This thing is designed to let issuers build their own workflows on top of it.

**ALEX:** Here's the key concept: disputes move through states via events. You fire an event, the system validates the transition, and the dispute lands in a new state. Simple in theory, complex in practice.

**JORDAN:** The state machine has eight major groups, and each group represents a phase of the dispute lifecycle. Think of them like chapters in a book, except this book has multiple endings and some of them are sad.

**ALEX:** The groups are OPEN, CARDNETWORK_CHARGEBACK, CARDNETWORK_SECOND_PRESENTMENT, CARDNETWORK_PREARBITRATION, DENIED, FAILED, LOSS, and WON. We'll cover each one in detail.

**JORDAN:** From a UX perspective, these groups help us organize our interface. Each group needs different UI elements, different actions, and different messaging. Map your UI to these groups, and you're halfway there.

---

## [SLIDE 5] State Groups Deep Dive
*OPEN, CARDNETWORK_CHARGEBACK, DENIED, FAILED, LOSS, WON*

**ALEX:** Let's walk through each state group. OPEN is where everything begins. It contains the PENDING state, which is basically the dispute's waiting room before submission to the network.

**JORDAN:** CARDNETWORK_CHARGEBACK is the active phase. This includes OPENED, CHARGEBACK_CREATED, and CHARGEBACK_PENDING_DOCUMENTATION. The dispute is live with the card network and things are happening.

**ALEX:** CARDNETWORK_SECOND_PRESENTMENT kicks in when the acquirer or merchant decides to fight back. They're saying, "Nope, this chargeback isn't valid, here's our evidence."

**JORDAN:** CARDNETWORK_PREARBITRATION is the escalation zone. If second presentment didn't resolve things, this is where the card network makes the final call. High stakes, limited options.

**ALEX:** Then we have our terminal groups. DENIED means the issuer canceled the dispute. FAILED means something went wrong technically. LOSS means the issuer lost. And WON means party time.

**JORDAN:** Well, party time for the issuer and cardholder. The merchant and acquirer probably aren't throwing confetti. Your UI needs to clearly communicate which of these outcomes occurred and what it means financially.

---

## [SLIDE 6] Core Workflow Overview
*Cardholder to Issuer to Network to Resolution*

**JORDAN:** Let's zoom out and look at the big picture. The dispute workflow has four main phases that every dispute passes through, regardless of network.

**ALEX:** Phase one is Dispute Creation. The cardholder contacts their bank, the operator creates a dispute in the system, evidence gets uploaded, and network-specific forms get submitted. Then the OPEN event fires to submit everything.

**JORDAN:** Phase two is Network Processing. Pismo takes the ball and runs it over to the card network. The network crunches through their rules and responds with either an acceptance or a rejection.

**ALEX:** Phase three is where it gets interesting. This is Resolution, and it can go multiple rounds. The acquirer might accept the chargeback, contest it, or let it expire. If they contest, we escalate to pre-arbitration.

**JORDAN:** And phase four is Terminal States. Every dispute eventually lands in one of our final buckets: won, lost, canceled, or failed. Your UI needs to guide users through each phase while setting clear expectations about what comes next.

**ALEX:** The whole process can take anywhere from a few days to several months, depending on how contentious things get. Build your UI with that timeline in mind.

---

## [SLIDE 7] Step 1: Creating a Dispute
*API call, PENDING state, mockup*

**ALEX:** Let's get hands-on. Creating a dispute starts with a POST request to the disputes endpoint. You'll need the account ID, transaction ID, dispute type, reason code, and disputed amount.

**JORDAN:** From the UI side, this is our Dispute Creation Dialog. We're using a Shadcn Dialog component with form inputs for each required field. The reason code selector is particularly important because it determines the evidence requirements.

**ALEX:** Once the API returns successfully, the dispute lands in PENDING status. This is a stable state where you can add evidence, submit forms, and basically prep everything before going live with the network.

**JORDAN:** Our mockup shows a clean three-section form. Section one captures transaction details. Section two handles dispute type and reason code selection. Section three shows the evidence checklist based on the selected reason code.

**ALEX:** Pro tip: validate everything client-side before hitting the API. Nothing frustrates operators more than filling out a long form only to get a four hundred error at the end.

**JORDAN:** We also show a "What's Next" panel that explains the PENDING state and lists the actions available. Transparency builds trust, even when the user is an internal operator.

---

## [SLIDE 8] Step 2: Uploading Evidence
*File uploads, evidence types, mockup*

**JORDAN:** Evidence is the lifeblood of disputes. Without proper documentation, even legitimate chargebacks get rejected. Our Evidence Upload Screen needs to make this process foolproof.

**ALEX:** The API endpoint is POST to disputes slash ID slash files. You can upload PDFs up to ten megabytes, images up to five megabytes, and TIFFs for scanned documents. The API validates format and size before accepting.

**JORDAN:** Our UI shows a checklist generated from the reason code selection. If you picked fraud card-not-present, we show cardholder statement as required, with IP logs and device fingerprint as supporting documents.

**ALEX:** The drag-and-drop zone supports multi-file upload with progress indicators. Each uploaded file shows a preview, file name, size, and a status badge indicating whether it's been accepted by the API.

**JORDAN:** We also include inline validation warnings. If someone tries to upload a giant forty-megabyte video file, we catch that before they waste time waiting for an upload that's going to fail anyway.

**ALEX:** One more thing: the API doesn't tell you if your evidence is good enough to win. It only validates the technical requirements. Train your operators to collect strong evidence, not just any evidence.

---

## [SLIDE 9] Step 3: Opening the Dispute
*PENDING to OPENED transition, mockup*

**ALEX:** This is the point of no return. Once you fire the OPEN event, the dispute gets submitted to the card network and you're locked into the process. No pressure.

**JORDAN:** Our Open Dispute confirmation dialog includes a final checklist review. We show all uploaded evidence, submitted forms, and a clear warning that this action cannot be undone. Make them click twice if you have to.

**ALEX:** The API call is a PUT to disputes slash ID slash status with the event set to OPEN. If successful, the status transitions to OPENED. If something's missing, you'll get a four hundred error with details about what's wrong.

**JORDAN:** The mockup shows a summary card with the dispute amount prominently displayed, a timeline showing the current position in the workflow, and big clear action buttons for Open and Cancel.

**ALEX:** After opening, the dispute enters a waiting period while the network processes the submission. Typical response time is five to seven business days, but it varies by network and dispute type.

**JORDAN:** We show a status banner that says "Submitted to Network - Awaiting Response" with an estimated timeline. Managing expectations is half the battle in dispute management.

---

## [SLIDE 10] Step 4: Chargeback Creation
*Network accepts, CHARGEBACK_CREATED, mockup*

**JORDAN:** Good news arrives. The card network has accepted the dispute and created a chargeback. This is CHARGEBACK_CREATED status, and it means we're making progress.

**ALEX:** At this point, the funds have been provisionally credited to the cardholder's account. I say provisionally because the merchant can still contest. But for now, the money has moved.

**JORDAN:** Our Chargeback Review screen uses an Alert component to highlight the network response. Green success banner, clear status badge, and a summary of what just happened in plain language.

**ALEX:** The response from Pismo includes the network's reference number, the accepted amount, and any messages from the network. Parse these carefully because they contain important details for the next steps.

**JORDAN:** We also show a "What Can Happen Next" section with three possible outcomes. The acquirer can accept the loss, contest with second presentment, or let the deadline expire. Each outcome links to its own explanation.

**ALEX:** This is a good state to be in, but don't celebrate yet. About thirty percent of chargebacks get contested. Your UI should prepare operators for that possibility.

---

## [SLIDE 11] Step 5: Second Presentment
*Acquirer contests, deadline tracking, mockup*

**ALEX:** Plot twist. The acquirer didn't accept the chargeback. They've submitted a second presentment, which is basically their counter-argument with supporting evidence. The dispute just got interesting.

**JORDAN:** This is SECOND_PRESENTMENT status, and it comes with a critical deadline. The issuer has thirty to forty-five days depending on the network to respond. Miss that deadline, and you automatically lose.

**ALEX:** The acquirer's evidence package arrives through Pismo's webhooks. You'll get documents, their rebuttal arguments, and sometimes transaction details you hadn't seen before. All of this needs to be surfaced in your UI.

**JORDAN:** Our Second Presentment Alert uses an AlertDialog with a prominent countdown timer. Nothing focuses the mind like watching days tick away. We show the deadline date, days remaining, and recommended actions.

**ALEX:** At this point, the issuer has three options. Accept the loss with the ISSUER_LOSS event, escalate to pre-arbitration with the PRE_ARBITRATION event, or do nothing and let it expire. Only one of these options is good.

**JORDAN:** The mockup includes side-by-side evidence comparison. Our evidence on the left, their evidence on the right. This helps operators quickly assess whether escalation is worth it or if it's time to cut losses.

---

## [SLIDE 12] Step 6: Pre-Arbitration
*Escalation path, final resolution, mockup*

**ALEX:** We've escalated to pre-arbitration. This is PRE_ARBITRATION_OPENED status, and it's the final battleground. The card network will review both sides' evidence and make a binding decision.

**JORDAN:** Important context: pre-arbitration has fees. If you escalate and lose, you're not just out the dispute amount, you're also paying arbitration costs. Make sure your UI communicates this financial risk clearly.

**ALEX:** The API call requires additional documentation. You'll need to compile a comprehensive evidence package and potentially answer network-specific questions. Visa and Mastercard have different requirements here.

**JORDAN:** Our Pre-Arbitration Form is a multi-step wizard. Step one reviews existing evidence. Step two captures any new documentation. Step three shows a fee disclosure and final confirmation. No surprises.

**ALEX:** Once submitted, it's another waiting game. The network takes thirty to forty-five days to review and render a decision. PRE_ARBITRATION_ACCEPTED means you won. PRE_ARBITRATION_DECLINED means you lost.

**JORDAN:** The evidence summary table shows everything submitted throughout the dispute lifecycle. We use color-coded badges to indicate which evidence was most relevant to each phase. It helps operators learn what works.

---

## [SLIDE 13] Resolution States
*WON vs LOSS scenarios, financial reconciliation*

**JORDAN:** Every dispute eventually ends. Let's talk about what winning and losing actually look like, because it's not just about status badges.

**ALEX:** When you win, the status lands in one of three states: CHARGEBACK_ACCEPTED, PRE_ARBITRATION_ACCEPTED, or CHARGEBACK_REJECT_COLLABORATION. The provisional credit becomes permanent, and the case is closed.

**JORDAN:** Our Resolution Summary for wins shows a big green badge, the final amount recovered, and a timeline of how we got there. Operators like to see the complete journey, especially for cases that took months to resolve.

**ALEX:** Losing is more varied. EXPIRED means you missed a deadline. CHARGEBACK_REJECTED means the network said no. PRE_ARBITRATION_DECLINED means you lost the final appeal. ISSUER_LOSS means you gave up voluntarily.

**JORDAN:** Each loss type needs different messaging. Missing a deadline deserves a root cause analysis. Network rejection might indicate weak evidence collection. Voluntary loss after reviewing merchant evidence might be the right call.

**ALEX:** Financial reconciliation happens automatically through Pismo's settlement process. But your UI should show the impact clearly. What was the disputed amount? What was recovered? What was lost? Show the math.

**JORDAN:** We also include a "Lessons Learned" section that surfaces patterns. If disputes with a certain reason code keep losing, maybe the evidence collection needs improvement. Data-driven feedback makes everyone better.

---

## [SLIDE 14] Visa Workflow
*Collaboration/Allocation forms, specific codes*

**ALEX:** Let's talk network specifics, starting with Visa. They have some unique requirements that affect your UI design, particularly around form submission.

**JORDAN:** Visa uses two special form types: Collaboration questionnaires and Allocation questionnaires. These are submitted via the forms endpoint before opening the dispute. Your UI needs to know when each form type is required.

**ALEX:** Collaboration forms are used for certain fraud disputes. They gather additional information about how the fraud was detected and what steps were taken. Allocation forms handle liability assignment for chip-related disputes.

**JORDAN:** Our Visa-specific form wizard detects the reason code and shows the appropriate questionnaire. The questions are structured, so we use radio buttons, checkboxes, and short text fields. Keep it scannable.

**ALEX:** Visa also has a unique workflow called PRE_ARB_ALLOCATION. This bypasses second presentment entirely and goes straight to arbitration for certain liability disputes. Your state machine handling needs to account for this path.

**JORDAN:** The reason codes for Visa follow a dot notation pattern. Ten dot X for fraud, eleven dot X for authorization issues, twelve dot X for processing errors, and thirteen dot X for consumer disputes. We group our UI accordingly.

**ALEX:** One more Visa quirk: they have the Visa Fraud Monitoring Program, or VFMP. Disputes flagged through this program have special requirements and often faster processing. Your UI should highlight VFMP cases.

---

## [SLIDE 15] Mastercard Workflow
*EBDF forms, TQR4 reports, specific codes*

**ALEX:** Next up is Mastercard, and they do things their own way. The big difference is the EBDF form, which stands for Electronic Batch Dispute File.

**JORDAN:** Every Mastercard dispute requires an EBDF submission. It's a structured data file that contains all the dispute details in Mastercard's format. Your backend handles the actual file generation, but your UI needs to collect all the required fields.

**ALEX:** Mastercard also uses TQR4 reports for reconciliation. These are separate from the dispute flow but impact settlement. If you're building a comprehensive disputes system, you'll need to integrate TQR4 data.

**JORDAN:** The Mastercard reason codes use a four-digit format starting with forty-eight. Common ones include forty-eight fifty-three for general cardholder disputes and forty-eight thirty-four for duplicate processing.

**ALEX:** One nice thing about Mastercard: their process is more linear than Visa. Second presentment leads to pre-arbitration, which leads to a final decision. No special allocation shortcuts to worry about.

**JORDAN:** Our Mastercard UI emphasizes the EBDF fields with inline validation. If a required field is missing, the operator sees the error immediately rather than after submission. Fail fast, fix fast.

**ALEX:** Watch out for dispute fees. Mastercard charges fees for certain dispute types and outcomes. These fees flow through a separate money exchange process outside the chargeback amounts. Track them carefully.

---

## [SLIDE 16] ELO Workflow
*Portal uploads, LATAM considerations*

**JORDAN:** Last but not least, ELO. This is a Brazilian card network, so if you're working in LATAM markets, pay close attention.

**ALEX:** The biggest difference with ELO is evidence handling. Unlike Visa and Mastercard where you upload files through the Pismo API, ELO requires evidence to be uploaded through their own portal manually.

**JORDAN:** Yes, you heard that right. Manual portal uploads. This means your UI needs to clearly indicate that evidence upload is an external step. We show a link to the ELO portal and a checklist of what needs to be uploaded there.

**ALEX:** The Pismo API still manages the dispute lifecycle and status transitions. You create the dispute, open it, and track its progress through Pismo. But the evidence piece lives outside your system.

**JORDAN:** Our ELO workflow screen has prominent callouts explaining this limitation. We use warning banners and confirmation dialogs to make sure operators don't miss the portal upload step. Forgetting it means losing the dispute.

**ALEX:** ELO reason codes follow a three-digit format. One hundred series for authorization issues, two hundred for processing errors, three hundred for consumer disputes, and four hundred for fraud.

**JORDAN:** For LATAM deployments, also consider Portuguese language support and Brazilian compliance requirements. Some documentation may need to be in Portuguese to be accepted by the network.

**ALEX:** ELO also has dispute fees similar to Mastercard. These get settled separately and need to be tracked in your financial reconciliation. Build your reporting with this in mind.

---

## [SLIDE 17] Building Your Dialogs
*UI patterns, Shadcn components, form requirements*

**JORDAN:** Alright developers, let's get practical. You've seen the workflow, you understand the states. Now let's talk about building the actual UI components.

**ALEX:** Your dialogs need to be state-aware. Pull the current dispute status from the API and render the appropriate component. PENDING state shows the edit form. OPENED state shows the status tracker. Terminal states show the summary.

**JORDAN:** We recommend these Shadcn components as your building blocks. Dialog for modal interactions. Card for content grouping. Badge for status indicators. Button for actions. Form components for data entry. AlertDialog for confirmations.

**ALEX:** For the timeline visualization, use a custom component that maps to the state groups. Show which phase the dispute is in, which states it's passed through, and what the possible next states are. Context is everything.

**JORDAN:** Action buttons should be smart. Grey out actions that aren't valid for the current state. Show tooltips explaining why an action is disabled. And always confirm destructive actions with a dialog.

**ALEX:** Form validation is critical. Each reason code has specific evidence requirements. Build a validation layer that checks whether all required documents are uploaded before allowing the OPEN event. Save your operators from preventable errors.

**JORDAN:** Also think about loading states and error handling. Network latency is real. API errors happen. Your UI should gracefully handle delays and surface meaningful error messages when things go wrong.

**ALEX:** One more pattern: optimistic updates with rollback. When an operator clicks an action, update the UI immediately while the API call is in flight. If the call fails, roll back the UI and show an error. It feels faster and more responsive.

---

## [SLIDE 18] Key Takeaways and Resources
*Summary, API links, next steps*

**ALEX:** We've covered a lot of ground. Let's wrap up with the key points you should take away from this presentation.

**JORDAN:** First, understand the state machine. The PRIMITIVE model has eight state groups with specific transitions between them. Map your UI to these groups and you'll have a solid foundation.

**ALEX:** Second, network differences matter. Visa has collaboration and allocation forms. Mastercard requires EBDF submissions. ELO needs manual portal uploads. Build your system to handle all three gracefully.

**JORDAN:** Third, evidence is everything. Strong documentation wins disputes. Weak documentation loses them. Your UI should guide operators toward collecting the right evidence for each dispute type and reason code.

**ALEX:** Fourth, deadlines are critical. Missing a response window means automatic loss. Build prominent countdown timers and notification systems to keep operators on track.

**JORDAN:** Fifth, design for the full lifecycle. Disputes can take months to resolve. Your UI needs to tell the complete story from creation to resolution, including every twist and turn along the way.

**ALEX:** For resources, the Pismo developer documentation is your best friend. Specifically the disputes overview page and the state machine reference. I'll drop those links in the presentation materials.

**JORDAN:** And don't forget to test with real scenarios. Create disputes in the sandbox environment, walk through each workflow path, and verify your UI handles every state correctly. Edge cases will find you in production if you don't find them first.

**ALEX:** Thanks for joining us on this deep dive into Pismo Disputes. Go build something great, and may all your chargebacks be accepted.

**JORDAN:** And if they're not, at least now you know how to handle it gracefully. Happy coding, everyone.

---

## Audio Generation Reference

### File Naming Convention
Each slide segment should be generated with this naming pattern:
```
slide{NN}_{speaker}_{segment}.mp3
```

Example:
- `slide01_alex_01.mp3`
- `slide01_jordan_01.mp3`
- `slide01_alex_02.mp3`
- `slide01_jordan_02.mp3`

### Edge TTS Commands
```bash
# Alex's lines (male voice)
edge-tts --voice en-US-GuyNeural --text "LINE_TEXT" --write-media slide{NN}_alex_{SEG}.mp3

# Jordan's lines (female voice)
edge-tts --voice en-US-JennyNeural --text "LINE_TEXT" --write-media slide{NN}_jordan_{SEG}.mp3
```

### Segment Count per Slide
| Slide | Alex Segments | Jordan Segments | Total |
|-------|---------------|-----------------|-------|
| 1 | 2 | 2 | 4 |
| 2 | 2 | 3 | 5 |
| 3 | 3 | 3 | 6 |
| 4 | 3 | 2 | 5 |
| 5 | 3 | 3 | 6 |
| 6 | 3 | 3 | 6 |
| 7 | 3 | 3 | 6 |
| 8 | 3 | 3 | 6 |
| 9 | 3 | 3 | 6 |
| 10 | 3 | 3 | 6 |
| 11 | 3 | 3 | 6 |
| 12 | 3 | 3 | 6 |
| 13 | 3 | 3 | 6 |
| 14 | 4 | 3 | 7 |
| 15 | 4 | 3 | 7 |
| 16 | 4 | 3 | 7 |
| 17 | 4 | 3 | 7 |
| 18 | 4 | 4 | 8 |

**Total Audio Segments: 110**
