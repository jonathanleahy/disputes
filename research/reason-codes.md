# Network Reason Codes Reference

## Visa Reason Codes

### Fraud (10.x)
| Code | Description | Evidence Required |
|------|-------------|-------------------|
| 10.1 | EMV Liability Shift Counterfeit Fraud | Chip transaction proof |
| 10.2 | EMV Liability Shift Non-Counterfeit Fraud | Chip transaction proof |
| 10.3 | Other Fraud - Card Present | Cardholder statement |
| 10.4 | Other Fraud - Card Not Present | Cardholder statement, IP logs |
| 10.5 | Visa Fraud Monitoring Program | VFMP notification |

### Authorization (11.x)
| Code | Description | Evidence Required |
|------|-------------|-------------------|
| 11.1 | Card Recovery Bulletin | Card status at time of transaction |
| 11.2 | Declined Authorization | Authorization log |
| 11.3 | No Authorization | Authorization log showing no auth |

### Processing Errors (12.x)
| Code | Description | Evidence Required |
|------|-------------|-------------------|
| 12.1 | Late Presentment | Transaction date proof |
| 12.2 | Incorrect Transaction Code | Transaction details |
| 12.3 | Incorrect Currency | Original receipt |
| 12.4 | Incorrect Account Number | Account documentation |
| 12.5 | Incorrect Amount | Original receipt, statement |
| 12.6 | Duplicate Processing | Both transaction records |
| 12.7 | Invalid Data | Transaction data |

### Consumer Disputes (13.x)
| Code | Description | Evidence Required |
|------|-------------|-------------------|
| 13.1 | Merchandise/Services Not Received | Shipping records, delivery proof |
| 13.2 | Cancelled Recurring Transaction | Cancellation proof |
| 13.3 | Not as Described | Product description, photos |
| 13.4 | Counterfeit Merchandise | Expert assessment |
| 13.5 | Misrepresentation | Marketing materials |
| 13.6 | Credit Not Processed | Return/refund documentation |
| 13.7 | Cancelled Merchandise/Services | Cancellation proof |

---

## Mastercard Reason Codes

### Authorization (48xx)
| Code | Description | Evidence Required |
|------|-------------|-------------------|
| 4807 | Warning Bulletin File | Card status |
| 4808 | Authorization Required | Auth log |
| 4812 | Account Number Not On File | Account docs |
| 4834 | Duplicate Processing | Transaction records |
| 4837 | No Cardholder Authorization | Cardholder statement |

### Point of Interaction Error (48xx)
| Code | Description | Evidence Required |
|------|-------------|-------------------|
| 4831 | Transaction Amount Differs | Receipt, statement |
| 4842 | Late Presentment | Transaction date |

### Cardholder Dispute (48xx)
| Code | Description | Evidence Required |
|------|-------------|-------------------|
| 4841 | Cancelled Recurring | Cancellation proof |
| 4853 | Cardholder Dispute | Cardholder statement |
| 4854 | Cardholder Dispute - Not Elsewhere | Varies |
| 4855 | Goods/Services Not Provided | Delivery proof |
| 4859 | Addendum, No-show | Booking records |
| 4860 | Credit Not Processed | Refund records |
| 4863 | Cardholder Does Not Recognize | Cardholder statement |

### Fraud (48xx)
| Code | Description | Evidence Required |
|------|-------------|-------------------|
| 4849 | Questionable Merchant Activity | Investigation docs |
| 4870 | Chip Liability Shift | EMV data |
| 4871 | Chip/PIN Liability Shift | EMV + PIN data |

---

## ELO Reason Codes

### Authorization
| Code | Description |
|------|-------------|
| 101 | Transaction Not Authorized |
| 102 | Expired Card |
| 103 | Card Not On File |

### Processing Errors
| Code | Description |
|------|-------------|
| 201 | Duplicate Transaction |
| 202 | Incorrect Amount |
| 203 | Late Presentment |

### Consumer Disputes
| Code | Description |
|------|-------------|
| 301 | Merchandise Not Received |
| 302 | Service Not Rendered |
| 303 | Credit Not Processed |
| 304 | Quality Dispute |

### Fraud
| Code | Description |
|------|-------------|
| 401 | Card Not Present Fraud |
| 402 | Card Present Fraud |
| 403 | Identity Theft |

---

## Code Selection UI Considerations

### Grouping Strategy
Organize reason codes in the UI by:
1. **Top Level**: Network (Visa, Mastercard, ELO)
2. **Second Level**: Category (Fraud, Authorization, Processing, Consumer)
3. **Third Level**: Specific reason code

### Smart Defaults
- Pre-select most common codes based on dispute type
- Show "Recently Used" codes for operators
- Highlight codes with higher win rates

### Validation Rules
- Ensure selected code matches dispute type
- Validate evidence requirements are met
- Warn if code has historically low success rate
