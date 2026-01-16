# Evidence Requirements by Dispute Type

## General Evidence Categories

### Cardholder Documentation
- Signed cardholder statement/affidavit
- Photo ID (for identity fraud)
- Police report (for theft)
- Communication records with merchant

### Transaction Documentation
- Original receipt/invoice
- Transaction authorization log
- Point-of-sale data
- IP address/geolocation (CNP transactions)

### Merchant Communication
- Cancellation requests
- Refund requests
- Customer service correspondence
- Return receipts

### Delivery/Shipping
- Tracking numbers
- Delivery confirmation
- Signed delivery receipts
- Shipping carrier records

---

## Evidence by Dispute Type

### Fraud - Card Not Present (CNP)
| Required | Supporting |
|----------|------------|
| Cardholder statement | IP address logs |
| Transaction details | Device fingerprint |
| | AVS/CVV mismatch data |

### Fraud - Card Present
| Required | Supporting |
|----------|------------|
| Cardholder statement | Police report |
| EMV chip data | Surveillance footage |
| Card status at time | ATM logs |

### Fraud - Lost/Stolen Card
| Required | Supporting |
|----------|------------|
| Cardholder statement | Police report |
| Card reported lost date | Fraud alert records |
| Transaction timestamps | |

### Merchandise Not Received
| Required | Supporting |
|----------|------------|
| Cardholder statement | Shipping records |
| Expected delivery date | Tracking data |
| | Merchant communication |

### Service Not Rendered
| Required | Supporting |
|----------|------------|
| Cardholder statement | Service agreement |
| Service date/location | Cancellation attempts |
| | Merchant communication |

### Duplicate Processing
| Required | Supporting |
|----------|------------|
| Both transaction records | Bank statements |
| Cardholder statement | Authorization logs |

### Credit Not Processed
| Required | Supporting |
|----------|------------|
| Return/refund proof | Return receipt |
| Cardholder statement | Merchant communication |
| Credit promise date | Refund policy |

### Not As Described
| Required | Supporting |
|----------|------------|
| Product description | Photos of received item |
| Cardholder statement | Expert assessment |
| | Return attempt proof |

### Cancelled Recurring
| Required | Supporting |
|----------|------------|
| Cancellation request | Confirmation email |
| Cardholder statement | Account screenshots |
| Billing date after cancel | |

---

## Network-Specific Requirements

### Visa Additional Forms
- **Collaboration Questionnaire**: Required for certain fraud disputes
- **Allocation Questionnaire**: Required for liability disputes
- Forms submitted via `/disputes/{id}/forms` endpoint

### Mastercard Additional Forms
- **EBDF (Electronic Batch Dispute File)**: Required for all disputes
- TQR4 reconciliation reports for settlement

### ELO Special Requirements
- Evidence uploaded via ELO portal (not API)
- Custom message codes required
- Brazil-specific compliance documents may be needed

---

## File Format Requirements

| Format | Max Size | Use Case |
|--------|----------|----------|
| PDF | 10MB | Documents, statements, forms |
| JPG/PNG | 5MB | Receipts, photos, screenshots |
| TIFF | 10MB | Scanned documents |

### Best Practices
1. Ensure all text is legible
2. Remove personal data not related to dispute
3. Organize multi-page documents logically
4. Name files descriptively (e.g., `cardholder_statement_20240115.pdf`)

---

## UI Considerations for Evidence Upload

### Upload Flow
1. Show required documents checklist based on reason code
2. Allow drag-and-drop upload
3. Preview uploaded files
4. Validate file format/size before API call
5. Show upload progress
6. Confirm successful uploads

### Document Checklist Component
```
[ ] Cardholder Statement (Required)
[ ] Transaction Receipt (Required)
[ ] Police Report (If applicable)
[ ] Merchant Communication (Optional)
[ ] Delivery Proof (If applicable)
```

### Status Indicators
- Missing required documents
- Documents pending upload
- Documents successfully uploaded
- Documents rejected (reason shown)
