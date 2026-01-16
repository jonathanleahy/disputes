# Pismo Disputes Workflow Diagrams

## Network-Specific Workflows

### Visa Workflow

```
Cardholder reports dispute
         │
         ▼
┌─────────────────────┐
│   Create Dispute    │  POST /disputes
│   (PENDING)         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Submit Visa Forms   │  POST /disputes/{id}/forms
│ - Collaboration     │  (questionnaires)
│ - Allocation        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Upload Evidence     │  POST /disputes/{id}/files
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Open Dispute      │  PUT /disputes/{id}/status
│   (OPENED)          │  event: OPEN
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌────────┐  ┌────────────┐
│ FAILED │  │ CHARGEBACK │
│        │  │  CREATED   │
└───┬────┘  └─────┬──────┘
    │             │
    │ RESEND      │
    └─────────────┤
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌────────┐ ┌───────────┐ ┌──────────┐
│ACCEPTED│ │  SECOND   │ │ REJECTED │
│ (WIN)  │ │PRESENTMENT│ │  (LOSS)  │
└────────┘ └─────┬─────┘ └──────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ PRE_ARB_OPENED  │ Visa Allocation
        │       or        │ (bypasses 2nd presentment)
        │ PRE_ARB_ALLOC   │
        └────────┬────────┘
                 │
         ┌───────┴───────┐
         │               │
         ▼               ▼
   ┌──────────┐   ┌──────────┐
   │ ACCEPTED │   │ DECLINED │
   │  (WIN)   │   │  (LOSS)  │
   └──────────┘   └──────────┘
```

**Visa-Specific Features:**
- Collaboration questionnaires (form submission)
- Allocation questionnaires (form submission)
- PRE_ARB_ALLOCATION workflow (bypasses second presentment)
- Reason codes: Fraud (CNP), Authorization, Processing Error, Consumer Disputes

### Mastercard Workflow

```
Cardholder reports dispute
         │
         ▼
┌─────────────────────┐
│   Create Dispute    │  POST /disputes
│   (PENDING)         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Submit EBDF Form   │  POST /disputes/{id}/forms
│  (Electronic Batch  │
│   Dispute File)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Upload Evidence     │  POST /disputes/{id}/files
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Open Dispute      │  PUT /disputes/{id}/status
│   (OPENED)          │
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌────────┐  ┌────────────┐
│ FAILED │  │ CHARGEBACK │
│        │  │  CREATED   │
└───┬────┘  └─────┬──────┘
    │ RESEND      │
    └─────────────┤
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌────────┐ ┌───────────┐ ┌──────────┐
│ACCEPTED│ │  SECOND   │ │ REJECTED │
│ (WIN)  │ │PRESENTMENT│ │  (LOSS)  │
└────────┘ └─────┬─────┘ └──────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  PRE_ARB_OPENED │ Standard escalation
        └────────┬────────┘
                 │
         ┌───────┴───────┐
         │               │
         ▼               ▼
   ┌──────────┐   ┌──────────┐
   │ ACCEPTED │   │ DECLINED │
   │  (WIN)   │   │  (LOSS)  │
   └──────────┘   └──────────┘
```

**Mastercard-Specific Features:**
- EBDF form submission (Electronic Batch Dispute File)
- TQR4 reconciliation reports
- Reason codes (e.g., 4853 for cardholder disputes)
- Dispute fees (money exchange outside chargeback flow)

### ELO Workflow

```
Cardholder reports dispute
         │
         ▼
┌─────────────────────┐
│   Create Dispute    │  POST /disputes
│   (PENDING)         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Upload Evidence to  │  ⚠️ VIA ELO PORTAL
│ ELO Portal (manual) │  (not via Pismo API)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Open Dispute      │  PUT /disputes/{id}/status
│   (OPENED)          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Standard Flow      │
│  (same as above)    │
└─────────────────────┘
```

**ELO-Specific Features:**
- Evidence uploaded via ELO portal (not API)
- Custom dispute codes with messaging
- Dispute fees similar to Mastercard
- Brazil/LATAM focused

## Core Workflow Summary

### Phase 1: Dispute Creation
1. Cardholder contacts issuer
2. Issuer creates dispute via API (status: PENDING)
3. Issuer uploads evidence files
4. Issuer submits network-specific forms
5. Issuer opens dispute (status: OPENED)

### Phase 2: Network Processing
6. Pismo submits to card network
7. Network processes and responds
8. Status updates: CHARGEBACK_CREATED or FAILED

### Phase 3: Resolution
9. If acquirer accepts: CHARGEBACK_ACCEPTED (issuer wins)
10. If acquirer contests: SECOND_PRESENTMENT
11. Issuer can escalate to PRE_ARBITRATION
12. Final resolution: ACCEPTED or DECLINED

### Phase 4: Terminal States
- **WIN**: CHARGEBACK_ACCEPTED, PRE_ARBITRATION_ACCEPTED
- **LOSS**: EXPIRED, REJECTED, DECLINED, ISSUER_LOSS
- **CANCELED**: Dispute withdrawn by issuer

## UI Workflow Considerations

### Dialog Requirements by State

| State | Required UI Elements |
|-------|---------------------|
| PENDING | Create form, reason selector, amount input |
| OPENED | Status display, timeline, cancel button |
| CHARGEBACK_CREATED | Network response, countdown timer, action buttons |
| SECOND_PRESENTMENT | Deadline alert, evidence review, escalate button |
| PRE_ARBITRATION_OPENED | Final submission form, evidence summary |
| TERMINAL | Resolution summary, financial impact, close button |

### Action Buttons by State

| State | Available Actions |
|-------|-------------------|
| PENDING | Open, Cancel |
| OPENED | Cancel |
| FAILED | Resend, Cancel |
| CHARGEBACK_CREATED | (await network) |
| SECOND_PRESENTMENT | Escalate, Accept Loss |
| PRE_ARBITRATION_OPENED | (await network) |
| TERMINAL | Close, Export |
