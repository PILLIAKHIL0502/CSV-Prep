# 🔍 Sparta TrackWise - Complete Technical Guide
## Enterprise Quality Management System for CMC Operations

**Version:** 1.0 Final  
**Last Updated:** December 2025  
**Target Audience:** Quality Engineers, CMC Scientists, QMS Administrators  
**Industry Focus:** Pharmaceutical & Life Sciences

---

## Table of Contents

1. [TrackWise Overview](#section-1)
2. [System Architecture](#section-2)
3. [Core Quality Modules](#section-3)
4. [CAPA Management](#section-4)
5. [Deviation Management](#section-5)
6. [Change Control](#section-6)
7. [Audit Management](#section-7)
8. [Integration & APIs](#section-8)
9. [Reporting & Analytics](#section-9)

---

<a name="section-1"></a>
## 1. TrackWise Overview

### 🎯 What is Sparta TrackWise?

**TrackWise** is Sparta Systems' enterprise Quality Management System (QMS) designed for regulated industries, particularly pharmaceutical and medical device manufacturing.

**Core Capabilities:**
```
✅ CAPA (Corrective & Preventive Action)
✅ Deviation Management
✅ Change Control
✅ Audit Management (Internal & External)
✅ Non-Conformance Management
✅ Complaint Handling
✅ Risk Management
✅ Document Control (optional)
✅ Training Management
✅ Supplier Quality Management
```

---

### 📊 TrackWise Architecture

```mermaid
graph TB
    subgraph "User Access"
        A1[Web Browser]
        A2[Mobile App]
        A3[Email Notifications]
    end
    
    subgraph "Application Layer"
        B1[Web Server - IIS]
        B2[TrackWise Application]
        B3[Workflow Engine]
        B4[Notification Engine]
        B5[Reporting Engine]
    end
    
    subgraph "Data Layer"
        C1[(SQL Server Database)]
        C2[(Document Repository)]
        C3[(Audit Trail Store)]
    end
    
    subgraph "Integration"
        D1[REST API]
        D2[SOAP Web Services]
        D3[File Import/Export]
        D4[SAP Connector]
    end
    
    A1 --> B1
    A2 --> B1
    A3 --> B4
    B1 --> B2
    B2 --> B3
    B2 --> B4
    B2 --> B5
    B2 --> C1
    B2 --> C2
    B2 --> C3
    B2 --> D1
    B2 --> D2
    B2 --> D3
    D1 --> D4
    
    style B2 fill:#E74C3C,color:#fff
    style C1 fill:#F39C12,color:#fff
```

---

<a name="section-4"></a>
## 4. CAPA Management

### 🔄 CAPA Workflow

```mermaid
stateDiagram-v2
    [*] --> Initiated
    Initiated --> Investigation: Assign
    Investigation --> Root_Cause_Analysis: Investigate
    Root_Cause_Analysis --> CAPA_Planning: RCA Complete
    CAPA_Planning --> Approval: Submit
    Approval --> CAPA_Planning: Reject
    Approval --> Implementation: Approve
    Implementation --> Verification: Complete
    Verification --> Effectiveness: Verify
    Effectiveness --> Closed: Effective
    Effectiveness --> Implementation: Not Effective
    Closed --> [*]
    
    note right of Investigation
        Gather evidence
        Interview personnel
        Review records
    end note
    
    note right of Root_Cause_Analysis
        5 Whys, Fishbone
        Identify true root cause
        Document findings
    end note
    
    note right of Effectiveness
        30-60-90 day checks
        Monitor KPIs
        Verify no recurrence
    end note
```

---

### 📋 CAPA Record Structure

```yaml
CAPA Record: CAPA-2025-001

Header Information:
  CAPA Number: CAPA-2025-001
  Title: "OOS Investigation - Aspirin Assay"
  Type: Corrective Action
  Priority: High
  Status: In Implementation
  Initiator: Jane QC Analyst
  Initiation Date: 2025-01-20
  Due Date: 2025-03-20 (60 days)
  
Problem Statement:
  Description: |
    Three consecutive batches (LOT-2025-001, 002, 003) failed
    aspirin assay specification. Results: 94.2%, 94.5%, 94.8%
    (Specification: 95.0-105.0%). Trend indicates systematic issue.
  
  Impact Assessment:
    Patient Safety: Low (within therapeutic range)
    Product Quality: Medium (fails release spec)
    Regulatory: High (trend of failures)
    Business: High (3 batches on hold, $150K)
    
  Affected Products:
    - Aspirin 500mg Tablets
    - Aspirin 325mg Tablets
    
Investigation:
  Investigator: John Sr. Scientist
  Investigation Start: 2025-01-21
  Investigation End: 2025-01-28
  
  Timeline of Events:
    - 2025-01-15: Batch LOT-2025-001 tested, failed (94.2%)
    - 2025-01-17: Batch LOT-2025-002 tested, failed (94.5%)
    - 2025-01-19: Batch LOT-2025-003 tested, failed (94.8%)
    - 2025-01-20: CAPA initiated
    
  Data Collected:
    - Raw chromatograms (all batches)
    - Instrument logs (HPLC-001)
    - Standard preparation logs
    - Calibration records
    - Environmental monitoring data
    
Root Cause Analysis:
  Method: 5 Whys + Fishbone Diagram
  
  5 Whys:
    1. Why did assay fail? → Peaks areas lower than expected
    2. Why were peak areas low? → Detector response decreased
    3. Why did response decrease? → Lamp intensity degraded
    4. Why did lamp degrade? → Exceeded recommended usage hours
    5. Why was lamp not replaced? → PM schedule not followed
    
  Root Cause: 
    "HPLC UV lamp exceeded 2,000 hour usage limit (actual: 2,450 hrs)
     due to missed preventive maintenance. Lamp intensity decreased
     by 15%, causing artificially low assay results."
  
  Evidence:
    - Lamp log shows 2,450 hours usage
    - PM schedule shows missed maintenance (due 12/15/24)
    - Lamp intensity check: 75% of specification (should be >90%)
    - Retest with new lamp: All batches pass (98.5%, 98.8%, 99.1%)
    
Corrective Actions:
  CA-001:
    Description: "Replace UV lamp immediately"
    Owner: QC Supervisor
    Due Date: 2025-01-22
    Status: Complete
    Completion Date: 2025-01-21
    Evidence: Work order #12345, new lamp serial #UV-2025-001
    
  CA-002:
    Description: "Retest all affected batches with new lamp"
    Owner: QC Analyst
    Due Date: 2025-01-25
    Status: Complete
    Completion Date: 2025-01-23
    Evidence: COA showing passing results
    
Preventive Actions:
  PA-001:
    Description: "Implement automated PM alerts in CMMS"
    Owner: IT Manager
    Due Date: 2025-02-15
    Status: In Progress (75%)
    Details: |
      - Email alerts at 1,800 hours (90% of limit)
      - Mandatory work order creation at 1,900 hours
      - System lock at 2,000 hours (cannot use instrument)
    
  PA-002:
    Description: "Quarterly review of all PM schedules"
    Owner: QA Manager
    Due Date: Ongoing (Start 2025-03-01)
    Status: Planned
    Frequency: Quarterly
    
  PA-003:
    Description: "Update SOP to include lamp intensity check"
    Owner: QC Manager
    Due Date: 2025-02-28
    Status: In Progress
    Document: SOP-QC-HPLC-001 (Rev 4.0)
    
Verification:
  Verification Plan:
    - Verify CA-001: Lamp installed correctly
    - Verify CA-002: Retesting complete, results documented
    - Verify PA-001: System tested with mock PM due dates
    - Verify PA-002: Calendar entries created
    - Verify PA-003: SOP updated and effective
    
  Verification Status: In Progress
  Verified By: [Pending]
  
Effectiveness Check:
  Schedule:
    - 30-day check: 2025-02-20
    - 60-day check: 2025-03-20
    - 90-day check: 2025-04-20
    
  Metrics to Monitor:
    - HPLC assay OOS rate (target: 0%)
    - PM completion on-time rate (target: 100%)
    - Lamp hours at replacement (target: <2,000)
    
  30-Day Check Results: [Pending]
  60-Day Check Results: [Pending]
  90-Day Check Results: [Pending]
  
Approvals:
  Investigation Approved:
    Approver: QA Manager
    Date: 2025-01-28
    Signature: [E-Sign]
    
  CAPA Plan Approved:
    Approver: Quality Director
    Date: 2025-01-30
    Signature: [E-Sign]
    
Linked Records:
  - Deviations: DEV-2025-005, DEV-2025-006, DEV-2025-007
  - Change Controls: CHG-2025-023 (SOP update)
  - OOS Investigations: OOS-2025-001, 002, 003
  - Training: TRN-2025-045 (Updated SOP training)
```

---

<a name="section-5"></a>
## 5. Deviation Management

### 🚨 Deviation Workflow

```mermaid
sequenceDiagram
    participant Operator
    participant TW as TrackWise
    participant Sup as Supervisor
    participant QA as QA Reviewer
    participant Invest as Investigator
    participant QAM as QA Manager
    
    Operator->>TW: Report Deviation
    Note over Operator,TW: Event: Temperature excursion<br/>Equipment: Incubator INC-001
    
    TW->>Sup: Notification: New Deviation
    Sup->>TW: Review & Classify
    Note over Sup,TW: Severity: Major<br/>GxP Impact: Yes
    
    Sup->>TW: Assign Investigator
    TW->>Invest: Task: Investigation
    
    Invest->>TW: Document Investigation
    Note over Invest,TW: Root Cause: Thermostat failure<br/>Duration: 2 hours<br/>Impact: 1 batch affected
    
    Invest->>TW: Propose Disposition
    Note over Invest,TW: Batch LOT-2025-005: REJECT<br/>Reason: Outside validated range
    
    TW->>QA: Review Investigation
    QA->>TW: Request Additional Testing
    
    Invest->>TW: Complete Additional Tests
    Note over Invest,TW: Potency test: 92% (spec: 90-110%)<br/>Impurities: Within limits
    
    QA->>TW: Approve Investigation
    
    TW->>QAM: Final Disposition
    QAM->>TW: Disposition: REJECT batch
    QAM->>TW: CAPA Required: Yes
    
    TW->>TW: Auto-create CAPA
    TW->>TW: Close Deviation
```

---

<a name="section-6"></a>
## 6. Change Control

### 🔄 Change Control Process

```mermaid
graph TD
    Start([Initiate Change]) --> A{Change Type?}
    
    A -->|Standard| B1[Auto-Approved]
    A -->|Minor| B2[Fast Track]
    A -->|Major| B3[Full Assessment]
    
    B1 --> C1[Implement]
    
    B2 --> D1[QA Review]
    D1 --> E1{Approved?}
    E1 -->|Yes| C1
    E1 -->|No| F1[Reject]
    
    B3 --> D2[Impact Assessment]
    D2 --> D3[Risk Assessment]
    D3 --> D4[Testing Plan]
    D4 --> D5[CAB Review]
    D5 --> E2{Approved?}
    
    E2 -->|No| F1
    E2 -->|Yes| C2[Testing]
    
    C2 --> G1[Execute Tests]
    G1 --> G2{Pass?}
    G2 -->|No| H1[Investigate]
    H1 --> C2
    G2 -->|Yes| C1
    
    C1 --> I[Implementation]
    I --> J[Verification]
    J --> K[Effectiveness]
    K --> L{Effective?}
    L -->|No| I
    L -->|Yes| M([Close])
    
    F1 --> M
    
    style Start fill:#3498DB,color:#fff
    style M fill:#2ECC71,color:#fff
    style F1 fill:#E74C3C,color:#fff
```

---

## 📊 TrackWise Reporting

### Standard Reports

```yaml
Quality Metrics Dashboard:
  
  CAPA Metrics:
    - Open CAPAs by Age: >30 days (15), >60 days (5), >90 days (2)
    - CAPA Closure Rate: 85% on-time (Target: >90%)
    - Average Time to Close: 45 days (Target: <60 days)
    - CAPAs by Root Cause: Human Error (35%), Equipment (25%), Process (20%)
    
  Deviation Metrics:
    - Deviations by Month: Jan (45), Feb (38), Mar (42)
    - Deviation Trend: Stable (no significant increase)
    - Major Deviations: 8 (Target: <10/month)
    - Time to Investigation: 3.2 days avg (Target: <5 days)
    
  Change Control Metrics:
    - Changes Implemented: 25 (This month)
    - Change Success Rate: 96% (Target: >95%)
    - Average Approval Time: 12 days (Target: <15 days)
    - Emergency Changes: 2 (Target: <5%)
    
  Audit Metrics:
    - Internal Audits Complete: 12/12 (100%)
    - Findings by Severity: Critical (0), Major (5), Minor (18)
    - Finding Closure Rate: 92% (Target: >90%)
    - Overdue Findings: 3 (Target: 0)
```

---

## 🎉 Conclusion

TrackWise provides:

✅ **Comprehensive QMS** for CMC operations  
✅ **Integrated quality modules** (CAPA, Deviation, Change)  
✅ **Workflow automation** reduces manual effort  
✅ **Complete audit trail** for compliance  
✅ **Robust reporting** for metrics & trends  
✅ **Configurable** to company processes  

**Market Position:** Leading QMS in pharma  
**Typical Implementation:** 9-12 months  
**User Base:** 500+ pharma companies globally  

---

**End of TrackWise QMS Guide**
