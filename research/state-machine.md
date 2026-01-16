# Pismo PRIMITIVE State Machine

## Overview

The PRIMITIVE state machine is Pismo's core architecture for managing dispute workflows. It uses events to transition disputes between statuses, enabling issuers to build their own state machine on top of the framework.

## State Groups

| Group | Purpose | States |
|-------|---------|--------|
| **OPEN** | Initial dispute state | PENDING |
| **CARDNETWORK_CHARGEBACK** | Active with card network | OPENED, CHARGEBACK_CREATED, CHARGEBACK_PENDING_DOCUMENTATION |
| **DENIED** | Dispute canceled by issuer | CANCELED |
| **FAILED** | Processing failures | FAILED, FAILED_PRE_ARBITRATION, FAILED_DOCUMENTATION, FILED_IN_ERROR, FAILED_ON_CLOSE |
| **LOSS** | Issuer loses dispute | EXPIRED, CHARGEBACK_REJECTED, CHARGEBACK_CLOSED, PRE_ARBITRATION_DECLINED, ISSUER_LOSS |
| **WON** | Issuer wins dispute | CHARGEBACK_ACCEPTED, PRE_ARBITRATION_ACCEPTED, CHARGEBACK_REJECT_COLLABORATION |
| **CARDNETWORK_SECOND_PRESENTMENT** | Acquirer contests chargeback | SECOND_PRESENTMENT |
| **CARDNETWORK_PREARBITRATION** | Escalation phase | PRE_ARBITRATION_OPENED, PRE_ARB_ALLOCATION_OPENED |

## Complete State List

### Initial States
- **PENDING**: Dispute created, awaiting submission to network

### Active States
- **OPENED**: Submitted to card network, awaiting response
- **CHARGEBACK_CREATED**: Network accepted, chargeback in progress
- **CHARGEBACK_PENDING_DOCUMENTATION**: Additional docs required

### Contest States
- **SECOND_PRESENTMENT**: Acquirer/merchant contesting the chargeback
- **PRE_ARBITRATION_OPENED**: Escalated to pre-arbitration
- **PRE_ARB_ALLOCATION_OPENED**: Visa allocation workflow (bypasses second presentment)

### Terminal States - Win
- **CHARGEBACK_ACCEPTED**: Acquirer accepted the chargeback (issuer wins)
- **PRE_ARBITRATION_ACCEPTED**: Won at pre-arbitration
- **CHARGEBACK_REJECT_COLLABORATION**: Won via Visa collaboration

### Terminal States - Loss
- **EXPIRED**: Deadline missed (issuer loses)
- **CHARGEBACK_REJECTED**: Network rejected chargeback
- **CHARGEBACK_CLOSED**: Closed without resolution (loss)
- **PRE_ARBITRATION_DECLINED**: Lost at pre-arbitration
- **ISSUER_LOSS**: Issuer accepted the loss

### Terminal States - Failure
- **FAILED**: Network submission failed (can RESEND)
- **FAILED_PRE_ARBITRATION**: Pre-arb submission failed
- **FAILED_DOCUMENTATION**: Documentation submission failed
- **FILED_IN_ERROR**: Dispute filed incorrectly
- **FAILED_ON_CLOSE**: Failed during closure

### Terminal States - Canceled
- **CANCELED**: Issuer canceled the dispute

## Key Transitions

### Happy Path (Issuer Wins)
```
PENDING
  → OPENED (OPEN event)
    → CHARGEBACK_CREATED (network accepts)
      → CHARGEBACK_ACCEPTED (acquirer accepts loss)
```

### Contested Path
```
CHARGEBACK_CREATED
  → SECOND_PRESENTMENT (acquirer contests)
    → PRE_ARBITRATION_OPENED (issuer escalates)
      → PRE_ARBITRATION_ACCEPTED (issuer wins)
      OR
      → PRE_ARBITRATION_DECLINED (issuer loses)
```

### Failure Recovery
```
OPENED
  → FAILED (network rejects)
    → OPENED (RESEND event - retry)
```

### Cancellation
```
PENDING
  → CANCELED (CANCEL event)
```

### Expiration
```
SECOND_PRESENTMENT
  → EXPIRED (deadline missed - 30-45 days depending on network)
```

## Events

| Event | Description | From States |
|-------|-------------|-------------|
| OPEN | Submit dispute to network | PENDING |
| CANCEL | Cancel the dispute | PENDING, OPENED |
| RESEND | Retry failed submission | FAILED |
| ISSUER_LOSS | Accept loss | SECOND_PRESENTMENT, PRE_ARBITRATION_OPENED |
| PRE_ARBITRATION | Escalate to pre-arb | SECOND_PRESENTMENT |

## State Machine Diagram

```
                                    ┌─────────────────┐
                                    │     PENDING     │
                                    └────────┬────────┘
                                             │ OPEN
                          CANCEL ┌───────────▼───────────┐ FAILED
                       ┌─────────│       OPENED          │─────────┐
                       │         └───────────┬───────────┘         │
                       ▼                     │                     ▼
                 ┌──────────┐                │              ┌──────────┐
                 │ CANCELED │                │              │  FAILED  │
                 └──────────┘                │              └────┬─────┘
                                             │                   │ RESEND
                                             │                   │
                            ┌────────────────▼────────────────┐  │
                            │      CHARGEBACK_CREATED         │◄─┘
                            └─────────────┬───────────────────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
                    ▼                     ▼                     ▼
          ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
          │ CHARGEBACK_     │   │    SECOND_      │   │ CHARGEBACK_     │
          │    ACCEPTED     │   │  PRESENTMENT    │   │   REJECTED      │
          │     (WIN)       │   └────────┬────────┘   │    (LOSS)       │
          └─────────────────┘            │            └─────────────────┘
                                         │
                         ┌───────────────┼───────────────┐
                         │               │               │
                         ▼               ▼               ▼
               ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
               │   EXPIRED   │  │  PRE_ARB_   │  │ ISSUER_LOSS │
               │   (LOSS)    │  │   OPENED    │  │   (LOSS)    │
               └─────────────┘  └──────┬──────┘  └─────────────┘
                                       │
                               ┌───────┴───────┐
                               │               │
                               ▼               ▼
                    ┌─────────────────┐ ┌─────────────────┐
                    │   PRE_ARB_      │ │   PRE_ARB_      │
                    │    ACCEPTED     │ │   DECLINED      │
                    │     (WIN)       │ │    (LOSS)       │
                    └─────────────────┘ └─────────────────┘
```

## Deadlines

| Transition | Deadline |
|------------|----------|
| OPENED → response | 5-7 business days |
| SECOND_PRESENTMENT → action | 30-45 days (network dependent) |
| PRE_ARBITRATION → response | 30-45 days (network dependent) |

Missing a deadline results in automatic EXPIRED status (issuer loss).
