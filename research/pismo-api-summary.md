# Pismo Disputes API Summary

## Overview

The Pismo Disputes API enables card issuers to manage transaction disputes through card networks (Visa, Mastercard, ELO). It uses a state machine architecture called PRIMITIVE to guide customers through the dispute process.

## API Base Information

- **Base URL**: `https://api.pismo.io`
- **Authentication**: Bearer JWT token
- **Account Context**: x-account-id header (deprecated June 2025, now uses authorization header)

## Key Endpoints

### Create Dispute
```
POST /disputes/v1/networkauthorization-disputes
```
Creates a new dispute for a transaction. Returns dispute ID.

**Required Fields**:
- `transaction_id`: Original transaction identifier
- `dispute_reason_code`: Network-specific reason code
- `disputed_amount`: Amount being disputed
- `cardholder_name`: Name on card
- `merchant_name`: Merchant being disputed

### Update Dispute Status
```
PUT /disputes/v1/disputes/{id}/status
```
Transitions dispute to a new state.

**Events**:
- `OPEN`: Move from PENDING to OPENED
- `CANCEL`: Cancel the dispute
- `RESEND`: Retry after FAILED state
- `ISSUER_LOSS`: Accept the loss

### Submit Forms
```
POST /disputes/v1/disputes/{id}/forms
```
Submit network-specific questionnaires (Visa collaboration/allocation forms).

### Upload Evidence
```
POST /disputes/v1/disputes/{id}/files
```
Upload supporting documentation files.

**Supported Types**:
- PDF documents
- Image files (JPG, PNG)
- Transaction receipts
- Cardholder statements

### Get Possible States
```
GET /disputes/v1/disputes/{id}/states
```
Returns available state transitions for the current dispute status.

### Create Installment
```
POST /disputes/v1/disputes/{id}/installments
```
Link installment payments to an existing dispute.

## Dispute Types

1. **Merchant Error**
   - Incorrect pricing
   - Duplicate charges
   - Unconfirmed refunds

2. **Identity Fraud (True Fraud)**
   - Stolen identity
   - Data breach compromise
   - Lost/stolen card

3. **Chargeback Fraud (Friendly Fraud)**
   - Cardholder disputes via bank rather than merchant
   - Goods received but claimed otherwise

## Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad request (validation error) |
| 401 | Unauthorized (token expired) |
| 404 | Dispute not found |
| 409 | Conflict (invalid state transition) |
| 422 | Unprocessable entity |

## Events & Notifications

Dispute status changes trigger webhook events:
- Event type: `dispute.status.changed`
- Contains: dispute_id, new_status, previous_status, state_machine, group_status
- Delivery: Real-time webhook or file-based batch

## Recent Updates (2025)

- **January 2025**: New updatable fields: `disputed_amount`, `comment`, `first_installment_amount`
- **April 2025**: New Migrate disputes endpoint in Migrations API
- **June 2025**: x-account-id parameter removed, authorization header now required

## Sources

- [Pismo Disputes Overview](https://developers.pismo.io/pismo-docs/docs/disputes-overview)
- [Pismo Disputes State Machine](https://developers.pismo.io/pismo-docs/docs/disputes-state-machine)
