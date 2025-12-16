# 📚 SAP Terminology, Abbreviations & Definitions
## Complete Reference for Pharmaceutical Manufacturing

**Version:** 1.0 Final  
**Last Updated:** December 2025  
**Purpose:** Master reference for SAP terms, abbreviations, and pharma-specific concepts

---

## Table of Contents

1. [SAP Modules & Components](#modules)
2. [SAP Technical Terms](#technical)
3. [SAP Transactions (T-Codes)](#tcodes)
4. [SAP Tables](#tables)
5. [Integration & Middleware](#integration)
6. [Pharmaceutical Specific Terms](#pharma)
7. [Validation & Compliance](#validation)
8. [Common Acronyms A-Z](#acronyms)

---

<a name="modules"></a>
## 1. SAP Modules & Components

### Core SAP Modules

**ABAP** - Advanced Business Application Programming
- SAP's proprietary programming language
- Used for custom development, reports, enhancements
- Example: Custom program to export production orders

**BASIS** - Business Application Software Integrated Solution
- Technical foundation of SAP
- System administration, user management, transport management
- Includes database administration, performance tuning

**BW/4HANA** - Business Warehouse for S/4HANA
- Data warehousing and analytics
- Replaces older SAP BW
- Runs on SAP HANA database

**EWM** - Extended Warehouse Management
- Advanced warehouse management
- Replaces older WM (Warehouse Management)
- Supports complex warehouse operations, automation

**FICO** - Financial Accounting and Controlling
- **FI**: Financial Accounting (external reporting)
- **CO**: Controlling (internal cost management)
- General ledger, accounts payable/receivable, cost centers

**HR / HCM** - Human Resources / Human Capital Management
- Employee master data, payroll, time management
- Organizational management, training

**MM** - Materials Management
- Procurement, inventory management
- Purchase requisitions, purchase orders, goods receipt
- Vendor management, invoice verification

**PM** - Plant Maintenance
- Equipment management, preventive maintenance
- Work orders, calibration schedules
- Critical for GMP compliance

**PP** - Production Planning
- Manufacturing execution, production orders
- MRP (Material Requirements Planning)
- BOM (Bill of Materials), routing management

**QM** - Quality Management
- Inspection planning, quality control
- Certificates of Analysis (COA)
- Integration with LIMS

**S/4HANA** - SAP Business Suite 4 SAP HANA
- Latest generation of SAP ERP
- Runs only on SAP HANA in-memory database
- Simplified data model (less tables)

**SAP GUI** - SAP Graphical User Interface
- Desktop client application
- Transaction-code based navigation
- Classic SAP interface

**SAP Fiori** - Modern UX for SAP
- Web and mobile-friendly interface
- Role-based apps, tile-based launchpad
- HTML5-based, responsive design

**SD** - Sales and Distribution
- Order management, pricing, shipping
- Customer master data
- Integration with PP for make-to-order

---

### Specialized Modules

**ATTP** - Advanced Track and Trace for Pharmaceuticals
- Serialization compliance (DSCSA, EU FMD)
- Aggregation (pallet, case, bottle)
- Track and trace throughout supply chain

**EHS** - Environment, Health & Safety
- Dangerous goods management
- Safety data sheets (SDS)
- Regulatory reporting

**SolMan** - Solution Manager
- Application lifecycle management
- System monitoring, change management
- Service desk, testing management

**GRC** - Governance, Risk & Compliance
- Access control, segregation of duties
- Risk management, audit management
- Compliance monitoring

**MDG** - Master Data Governance
- Central master data management
- Workflow for master data changes
- Data quality rules

---

<a name="technical"></a>
## 2. SAP Technical Terms

**BAPI** - Business Application Programming Interface
- Standard SAP function module
- Used for integration with external systems
- Example: BAPI_PRODORD_CREATE (create production order)

**BDC** - Batch Data Communication
- Method to automate data entry into SAP
- Simulates user entering data via transactions
- Used for data migration, batch updates

**CDS** - Core Data Services
- Modern way to define database views
- Enhanced with annotations for analytics
- Used in S/4HANA extensively

**Client** - Logical partition within SAP system
- Separate dataset within same database
- Example: Client 100 (DEV), Client 200 (QA), Client 300 (PROD)
- Highest level of data isolation

**CMOD / SMOD** - Customer Modifications
- User exits for custom code
- Enhancement spots defined by SAP
- Allows customization without modifying standard

**DDIC** - Data Dictionary
- Repository of SAP data structures
- Tables, views, data elements, domains
- Transaction: SE11

**Function Module** - Reusable piece of code
- Similar to a function in programming
- Can be called from programs, screens, interfaces
- Example: BAPI_GOODSMVT_CREATE

**IDoc** - Intermediate Document
- SAP's format for data exchange
- Structured document (segments, fields)
- Used for SAP ↔ Non-SAP integration

**IMG** - Implementation Guide
- Configuration workbench
- Tree structure of all config activities
- Transaction: SPRO

**Logical System** - Identifier for a system
- Used in distribution scenarios
- Example: SAPDEV (Development), SAPPRD (Production)
- Configured in SM59, BD54

**NetWeaver** - SAP technology platform
- Application server (ABAP, Java)
- Integration (PI/PO)
- Portal, Business Intelligence

**OData** - Open Data Protocol
- REST-based protocol
- JSON/XML data format
- Used for SAP Fiori, external integrations

**Package** - Collection of related development objects
- Organizes code, tables, etc.
- Example: Z_MES_INTERFACE (custom MES integration)
- Local packages (start with $TMP) vs transportable

**Program** - ABAP code executable
- Report programs (output data)
- Function groups (contain function modules)
- Module pools (for screens)

**RFC** - Remote Function Call
- Call SAP function from external system OR
- Call external function from SAP
- Synchronous or asynchronous

**SAPscript / Smart Forms** - Form design tools
- Create printable forms (PO, invoices, labels)
- Smart Forms are newer, XML-based

**SE## Transactions** - Development transactions
- SE11: Data Dictionary
- SE16: Data Browser
- SE37: Function Builder
- SE38: ABAP Editor
- SE80: Object Navigator

**SM## Transactions** - System admin transactions
- SM04: User List
- SM12: Lock Entries
- SM37: Job Overview
- SM59: RFC Destinations
- SM66: Global Work Process Overview

**ST## Transactions** - Performance/test transactions
- ST03: Workload Analysis
- ST22: ABAP Dump Analysis
- STMS: Transport Management System

**T-Code** - Transaction Code
- Short code to execute a function
- Example: MM01 (Create Material), CO01 (Create Production Order)
- Faster than navigating menus

**Table** - Database table in SAP
- Transparent table: One-to-one with DB table
- Pool table: Many SAP tables in one DB table
- Cluster table: Related data stored together

**Transport** - Package of changes moved between systems
- DEV → QA → PROD
- Contains config, code, data
- Managed via Transport Request

**User Exit** - Hook for custom code
- SAP provides empty function module
- Customer writes code in it
- Example: EXIT_SAPLCOOI_001

**Variant** - Saved selection screen values
- For reports, transactions
- Speeds up repetitive tasks
- Example: Production order list for Plant 0001

**Workbench** - Development environment
- ABAP Workbench (SE80)
- Customizing Workbench (SPRO)

---

<a name="tcodes"></a>
## 3. Key SAP Transactions (T-Codes)

### Material Master (MM)

| T-Code | Description | Use Case |
|--------|-------------|----------|
| MM01 | Create Material Master | Create new API, excipient, finished good |
| MM02 | Change Material Master | Update material description, storage conditions |
| MM03 | Display Material Master | View material data |
| MM04 | Display Changes to Material | Audit trail of material master changes |
| MM60 | List of Materials | Search for materials by criteria |

### Procurement (MM)

| T-Code | Description | Use Case |
|--------|-------------|----------|
| ME21N | Create Purchase Order | Order raw materials from supplier |
| ME22N | Change Purchase Order | Update quantity, delivery date |
| ME23N | Display Purchase Order | Review PO details |
| ME2N | Purchase Orders by Vendor | List all POs for a supplier |
| ME51N | Create Purchase Requisition | Request materials needed |
| ME52N | Change Purchase Requisition | Update PR |
| ME53N | Display Purchase Requisition | View PR |

### Inventory Management (MM)

| T-Code | Description | Use Case |
|--------|-------------|----------|
| MIGO | Goods Receipt/Issue | Unified transaction for all goods movements |
| MB01 | Post Goods Receipt | Receive materials from PO |
| MB1A | Goods Issue | Issue materials to production |
| MB1B | Transfer Posting | Move materials between storage locations |
| MB1C | Other Goods Receipts | Receipt without PO (returns, etc.) |
| MB51 | Material Document List | Search goods movements |
| MB52 | List of Warehouse Stocks | Current stock by storage location |
| MB53 | Display Plant Stock Availability | Stock overview for plant |
| MMBE | Stock Overview | Complete stock view (all plants, locations) |
| MI01 | Create Physical Inventory Doc | Cycle count |
| MI04 | Enter Inventory Count | Record counted quantities |
| MI07 | Post Inventory Difference | Adjust stock to count |

### Batch Management (MM)

| T-Code | Description | Use Case |
|--------|-------------|----------|
| MSC1N | Create Batch | Manual batch creation (usually automatic) |
| MSC2N | Change Batch | Update batch characteristics (expiry, etc.) |
| MSC3N | Display Batch | View batch details |
| MSC4N | Batch Where-Used | Where is batch used in production? |

### Production Planning (PP)

| T-Code | Description | Use Case |
|--------|-------------|----------|
| CO01 | Create Production Order | Manufacture tablets |
| CO02 | Change Production Order | Update quantity, dates |
| CO03 | Display Production Order | View order details |
| CO08 | Order List | Search production orders |
| CO40 | Convert Planned Order | Convert from MRP to production order |
| CO11N | Enter Confirmation | Confirm operation completion |
| CO12 | Display Confirmation | View confirmation |
| CO13 | Change Confirmation | Update confirmation |
| CO15 | Confirm and Goods Receipt | Final confirmation + GR in one step |
| CO88 | Order Reports | Various order reports |

### BOM & Routing (PP)

| T-Code | Description | Use Case |
|--------|-------------|----------|
| CS01 | Create BOM | Create bill of materials |
| CS02 | Change BOM | Update ingredients, quantities |
| CS03 | Display BOM | View BOM |
| CS12 | BOM Explosion | Multi-level BOM view |
| CS15 | BOM Comparison | Compare two BOMs |
| CA01 | Create Routing | Create production steps |
| CA02 | Change Routing | Update operations |
| CA03 | Display Routing | View routing |
| CR01 | Create Work Center | Define production resource |
| CR02 | Change Work Center | Update work center |

### MRP (PP)

| T-Code | Description | Use Case |
|--------|-------------|----------|
| MD01 | Total Planning | Run MRP for all materials |
| MD02 | Single-Item Planning | Run MRP for one material |
| MD03 | Collective Planning | Run MRP for group |
| MD04 | Stock/Requirements List | See demand vs supply |
| MD05 | MRP List | Detailed MRP results |
| MD16 | Requirements Planning | Planning overview |

### Quality Management (QM)

| T-Code | Description | Use Case |
|--------|-------------|----------|
| QA01 | Create Inspection Lot | QC testing for batch |
| QA02 | Change Inspection Lot | Update lot |
| QA03 | Display Inspection Lot | View lot |
| QA11 | Record Results | Enter test results |
| QA12 | Display Results | View results |
| QA32 | Usage Decision | Approve or reject batch |
| QA33 | Display Usage Decision | View decision |
| QE01 | Create Q Notification | Quality issue/deviation |

### Plant Maintenance (PM)

| T-Code | Description | Use Case |
|--------|-------------|----------|
| IE01 | Create Equipment | Register new tablet press |
| IE02 | Change Equipment | Update equipment data |
| IE03 | Display Equipment | View equipment |
| IH01 | Create Functional Location | Define area/location |
| IW31 | Create Maintenance Order | Schedule PM |
| IW32 | Change Maintenance Order | Update PM order |
| IW33 | Display Maintenance Order | View PM order |
| IP01 | Create Maintenance Plan | Preventive maintenance schedule |
| IP02 | Change Maintenance Plan | Update PM plan |

### Warehouse Management (WM/EWM)

| T-Code | Description | Use Case |
|--------|-------------|----------|
| /SCWM/PRDI | Inbound Delivery Processing | EWM goods receipt |
| /SCWM/PRDO | Outbound Delivery Processing | EWM goods issue |
| /SCWM/MON | EWM Monitor | Overall warehouse status |
| LT01 | Create Transfer Order | WM putaway |
| LS22 | Picking List | WM picking |

### System Administration

| T-Code | Description | Use Case |
|--------|-------------|----------|
| SU01 | User Maintenance | Create/change users |
| SU10 | Mass User Changes | Bulk user updates |
| PFCG | Role Maintenance | Create/change authorization roles |
| SM04 | User List | Who's logged in? |
| SM12 | Lock Entries | See locked objects |
| SM37 | Job Overview | Background jobs status |
| SM50 | Work Process Overview | System performance |
| SM59 | RFC Destinations | Configure external connections |
| ST22 | ABAP Dump Analysis | Troubleshoot errors |
| STMS | Transport Management | Promote changes DEV→QA→PRD |

### Development

| T-Code | Description | Use Case |
|--------|-------------|----------|
| SE11 | Data Dictionary | Tables, structures, domains |
| SE16 | Data Browser | View table data |
| SE37 | Function Builder | Create/view function modules |
| SE38 | ABAP Editor | Write ABAP programs |
| SE80 | Object Navigator | Main development environment |
| SE93 | Maintain Transaction | Create custom T-Codes |

---

<a name="tables"></a>
## 4. Key SAP Tables

### Material Master

| Table | Description | Key Fields |
|-------|-------------|------------|
| MARA | General Material Data | MATNR (Material Number) |
| MARC | Plant Data for Material | MATNR, WERKS (Plant) |
| MARD | Storage Location Data | MATNR, WERKS, LGORT (Storage Loc) |
| MBEW | Material Valuation | MATNR, BWKEY (Valuation Area) |
| MVKE | Sales Data | MATNR, VKORG (Sales Org) |
| MAKT | Material Descriptions | MATNR, SPRAS (Language) |

### Procurement

| Table | Description | Key Fields |
|-------|-------------|------------|
| EBAN | Purchase Requisition | BANFN (PR Number) |
| EKKO | Purchase Order Header | EBELN (PO Number) |
| EKPO | Purchase Order Items | EBELN, EBELP (Item) |
| EKET | Schedule Line | EBELN, EBELP, ETENR |
| LFA1 | Vendor Master (General) | LIFNR (Vendor Number) |
| LFB1 | Vendor Master (Company Code) | LIFNR, BUKRS |
| LFM1 | Vendor Master (Purchasing Org) | LIFNR, EKORG |

### Inventory

| Table | Description | Key Fields |
|-------|-------------|------------|
| MSEG | Material Document Segment | MBLNR (Mat Doc), MJAHR (Year) |
| MKPF | Material Document Header | MBLNR, MJAHR |
| MCHB | Batch Stock | MATNR, WERKS, CHARG (Batch) |
| MCH1 | Batch Master | MATNR, CHARG |

### Production

| Table | Description | Key Fields |
|-------|-------------|------------|
| AUFK | Order Master Data | AUFNR (Order Number) |
| AFKO | Order Header | AUFNR |
| AFPO | Order Items | AUFNR, POSNR (Item) |
| AFRU | Confirmations | AUFNR, RUECK (Conf Number) |
| JEST | Object Status | OBJNR (Object Number) |

### BOM & Routing

| Table | Description | Key Fields |
|-------|-------------|------------|
| MAST | Material to BOM Link | MATNR, WERKS, STLNR (BOM) |
| STKO | BOM Header | STLTY (BOM Category), STLNR |
| STPO | BOM Items | STLTY, STLNR, STLKN (Item) |
| MAPL | Material to Routing | MATNR, WERKS, PLNTY, PLNNR |
| PLKO | Routing Header | PLNTY, PLNNR, PLNAL |
| PLPO | Operations | PLNTY, PLNNR, PLNAL, PLNFL |

### Quality Management

| Table | Description | Key Fields |
|-------|-------------|------------|
| QALS | Inspection Lot | PRUEFLOS (Inspection Lot) |
| QAVE | Usage Decision | PRUEFLOS |
| QAMB | Inspection Lot Stock | PRUEFLOS, MATNR |

### Change Documents (Audit Trail)

| Table | Description | Key Fields |
|-------|-------------|------------|
| CDHDR | Change Document Header | OBJECTCLAS, OBJECTID, CHANGENR |
| CDPOS | Change Document Items | CHANGENR, FNAME (Field), VALUE_NEW, VALUE_OLD |

### User & Authorization

| Table | Description | Key Fields |
|-------|-------------|------------|
| USR01 | User Master Record | BNAME (Username) |
| USR02 | Logon Data | BNAME |
| USR21 | User Address | BNAME, ADDRNUMBER |
| AGR_USERS | Assignment of Roles to Users | UNAME, AGR_NAME (Role) |
| AGR_1251 | Authorization Data | AGR_NAME, OBJECT (Auth Object) |

---

<a name="integration"></a>
## 5. Integration & Middleware Terms

**API** - Application Programming Interface
- Interface for system-to-system communication
- REST APIs (JSON), SOAP APIs (XML)
- Example: MES calls SAP API to create confirmation

**EDI** - Electronic Data Interchange
- Standardized exchange of business documents
- Purchase orders, invoices
- Used for B2B integration with trading partners

**ESB** - Enterprise Service Bus
- Middleware architecture pattern
- Central hub for integrations
- Examples: MuleSoft, Dell Boomi, SAP PO

**IDoc** - Intermediate Document
- SAP's integration format
- Consists of segments (hierarchical structure)
- Example: LOIPRO (Production Order), MATMAS (Material Master)

**Middleware** - Software between SAP and other systems
- Transformation, routing, error handling
- Examples: SAP PO/PI, MuleSoft, Informatica, Dell Boomi

**OData** - Open Data Protocol
- RESTful protocol for CRUD operations
- Used by SAP Gateway, Fiori apps
- JSON or XML format

**PI/PO** - Process Integration / Process Orchestration
- SAP's integration platform
- Message mapping, routing, monitoring
- Being replaced by SAP Integration Suite (cloud)

**RFC** - Remote Function Call
- Synchronous call to SAP function module
- Can be called from external system via SDK
- Examples: Python pyrfc, Java JCo

**SAP Gateway** - Exposes SAP functionality as OData services
- Enables Fiori apps, external integrations
- Transaction: /IWFND/MAINT_SERVICE

**Web Service** - SOAP or REST service
- WSDL for SOAP (older)
- OpenAPI/Swagger for REST (modern)

---

<a name="pharma"></a>
## 6. Pharmaceutical Specific Terms

**21 CFR Part 11** - FDA regulation for electronic records
- Electronic signatures
- Audit trails
- System validation

**API** - Active Pharmaceutical Ingredient
- The drug substance
- Example: Acetaminophen in Tylenol
- Requires traceability, COA

**Batch** - Quantity of product made in single run
- Batch number for traceability
- Critical for recalls
- SAP Field: CHARG

**BPR** - Batch Production Record
- Paper or electronic record of manufacturing
- Lists ingredients, steps, results
- In SAP: Production Order + Confirmations

**CAPA** - Corrective Action / Preventive Action
- Response to deviations, OOS results
- Documented in QM notification or external system

**cGMP** - current Good Manufacturing Practices
- FDA regulations (21 CFR 210, 211)
- Quality system requirements
- Enforced via inspections

**COA** - Certificate of Analysis
- Test results for batch
- Supplier provides for raw materials
- QC generates for finished goods

**Deviation** - Unplanned departure from procedure
- Example: Equipment failure, OOS result
- Documented in SAP QM or external QMS

**DSCSA** - Drug Supply Chain Security Act
- US serialization law
- Track and trace for pharma products
- SAP ATTP module addresses

**EBR** - Electronic Batch Record
- Digital version of BPR
- MES system typically
- Integrates with SAP

**Excipient** - Inactive ingredient
- Example: Starch, cellulose in tablet
- SAP Material Type: HIBE (Semi-Finished)

**FEFO** - First Expired, First Out
- Inventory management strategy
- Critical for pharma (expiration dates)
- SAP EWM supports

**FIFO** - First In, First Out
- Inventory management strategy
- For materials without expiration tracking

**GMP** - Good Manufacturing Practices
- Quality system for manufacturing
- Includes documentation, training, validation

**GxP** - Umbrella term for GMP, GLP, GCP
- Regulated quality practices
- **GMP**: Manufacturing
- **GLP**: Laboratory
- **GCP**: Clinical

**IPC** - In-Process Control
- Testing during manufacturing
- Example: Tablet weight check every 15 min
- Results recorded in MES, may interface to LIMS

**LIMS** - Laboratory Information Management System
- Manages lab samples, tests, results
- Integrates with SAP QM
- Examples: LabWare, Thermo SampleManager

**MES** - Manufacturing Execution System
- Controls shop floor operations
- Electronic batch records
- Examples: Siemens Opcenter, Rockwell FactoryTalk, Emerson Syncade

**OOS** - Out of Specification
- Test result outside acceptance criteria
- Requires investigation
- May reject batch

**Qualified Person (QP)** - EU regulatory requirement
- Authorized to release batch
- Electronic signature in SAP

**Recall** - Removal of product from market
- Requires complete traceability
- SAP batch genealogy critical

**Retest Date** - Date to re-evaluate material
- For raw materials, intermediates
- Blocks usage after retest date

**Serialization** - Unique ID for each package
- Required by DSCSA, EU FMD
- SAP ATTP module
- Example: Serial number on bottle

**Shelf Life** - Time material remains acceptable
- From manufacturing date to expiry
- Configured in SAP material master

**SOP** - Standard Operating Procedure
- Written instructions for tasks
- Controlled documents in SAP DMS or external QMS

**Traceability** - Ability to trace materials forward/backward
- Which API batch used in which finished good?
- Which patients received affected batch?
- SAP batch genealogy

**UDI** - Unique Device Identifier
- For medical devices
- Similar to serialization

**Validation** - Documented evidence system does what it's supposed to
- IQ, OQ, PQ
- Required for GxP systems

---

<a name="validation"></a>
## 7. Validation & Compliance Terms

**CSV** - Computer System Validation
- Validation of computerized systems
- Required by 21 CFR Part 11, EU Annex 11

**GAMP** - Good Automated Manufacturing Practice
- Industry guide for validation
- Published by ISPE
- GAMP 5: Risk-based validation

**IQ** - Installation Qualification
- Verify system installed correctly
- Check configurations, infrastructure

**OQ** - Operational Qualification
- Verify system functions correctly
- Test each feature

**PQ** - Performance Qualification
- Verify system works in actual use
- End-to-end workflows with real users

**CSA** - Computer Software Assurance
- FDA's modern approach to validation
- Focus on critical functions
- Less documentation, more critical thinking

**Traceability Matrix** - Links requirements to tests
- Requirements → Design → Test Cases
- Proves all requirements tested

**Change Control** - Managed process for changes
- Impact assessment
- Testing
- Approval before production

**Regression Testing** - Re-test after changes
- Ensure no unintended impacts
- Scope based on risk

**Data Integrity** - ALCOA+ principles
- Attributable, Legible, Contemporaneous, Original, Accurate
- Plus: Complete, Consistent, Enduring, Available

---

<a name="acronyms"></a>
## 8. Common SAP Acronyms (A-Z)

**A**
- **ABAP**: Advanced Business Application Programming
- **ALE**: Application Link Enabling (distributed SAP systems)
- **API**: Active Pharmaceutical Ingredient OR Application Programming Interface
- **ATTP**: Advanced Track and Trace for Pharmaceuticals
- **ATP**: Available to Promise (stock check)

**B**
- **BAPI**: Business Application Programming Interface
- **BDC**: Batch Data Communication
- **BI**: Business Intelligence
- **BOM**: Bill of Materials
- **BOPF**: Business Object Processing Framework
- **BPR**: Batch Production Record
- **BW**: Business Warehouse

**C**
- **CAPA**: Corrective Action / Preventive Action
- **CDS**: Core Data Services
- **cGMP**: current Good Manufacturing Practices
- **COA**: Certificate of Analysis
- **CRM**: Customer Relationship Management
- **CSV**: Computer System Validation

**D**
- **DMS**: Document Management System
- **DSCSA**: Drug Supply Chain Security Act

**E**
- **EBR**: Electronic Batch Record
- **EDI**: Electronic Data Interchange
- **EHS**: Environment, Health & Safety
- **ERP**: Enterprise Resource Planning
- **ESB**: Enterprise Service Bus
- **EWM**: Extended Warehouse Management

**F**
- **FDA**: Food and Drug Administration
- **FEFO**: First Expired, First Out
- **FI**: Financial Accounting
- **FIFO**: First In, First Out
- **FI/CO**: Finance and Controlling

**G**
- **GAMP**: Good Automated Manufacturing Practice
- **GI**: Goods Issue
- **GMP**: Good Manufacturing Practices
- **GR**: Goods Receipt
- **GRC**: Governance, Risk & Compliance
- **GUI**: Graphical User Interface
- **GxP**: Good [Manufacturing/Laboratory/Clinical] Practices

**H**
- **HANA**: High-Performance Analytic Appliance
- **HCM**: Human Capital Management
- **HR**: Human Resources

**I**
- **IDoc**: Intermediate Document
- **IMG**: Implementation Guide
- **IPC**: In-Process Control
- **IQ**: Installation Qualification
- **ISPE**: International Society for Pharmaceutical Engineering

**L**
- **LIMS**: Laboratory Information Management System
- **LSMW**: Legacy System Migration Workbench

**M**
- **MARA**: Material Master table (General Data)
- **MARC**: Material Master table (Plant Data)
- **MARD**: Material Master table (Storage Location)
- **MDG**: Master Data Governance
- **MES**: Manufacturing Execution System
- **MM**: Materials Management
- **MRP**: Material Requirements Planning
- **MSEG**: Material Document table

**N**
- **NTP**: Network Time Protocol (for timestamps)

**O**
- **OData**: Open Data Protocol
- **OOS**: Out of Specification
- **OQ**: Operational Qualification

**P**
- **PI/PO**: Process Integration / Process Orchestration
- **PM**: Plant Maintenance
- **PO**: Purchase Order
- **PP**: Production Planning
- **PQ**: Performance Qualification
- **PR**: Purchase Requisition

**Q**
- **QA**: Quality Assurance
- **QC**: Quality Control
- **QM**: Quality Management
- **QP**: Qualified Person

**R**
- **RBAC**: Role-Based Access Control
- **RFC**: Remote Function Call
- **ROH**: Raw Material (Material Type)

**S**
- **S/4HANA**: SAP Business Suite 4 SAP HANA
- **SAP**: Systems, Applications, and Products in Data Processing
- **SCADA**: Supervisory Control and Data Acquisition
- **SCM**: Supply Chain Management
- **SD**: Sales and Distribution
- **SDS**: Safety Data Sheet
- **SolMan**: Solution Manager
- **SOP**: Standard Operating Procedure
- **SPRO**: Customizing (IMG)

**T**
- **T-Code**: Transaction Code

**U**
- **UDI**: Unique Device Identifier
- **UoM**: Unit of Measure
- **URS**: User Requirements Specification

**V**
- **VMS**: Vendor-Managed Inventory

**W**
- **WM**: Warehouse Management (older, replaced by EWM)
- **WHO**: World Health Organization

**Z**
- **Z-Table**: Custom table (starts with Z or Y)
- **Z-Program**: Custom program

---

## Quick Reference: SAP Data Flow

```
PROCUREMENT FLOW:
PR (ME51N) → PO (ME21N) → GR (MIGO) → IR (MIRO)

PRODUCTION FLOW:
Demand → MRP (MD01) → Planned Order → 
Production Order (CO01) → Release (CO02) → 
Material Issue (MB1A) → Execution → 
Confirmation (CO11N) → Goods Receipt (MB31) → 
QM Inspection (QA01) → Usage Decision (QA32)

QUALITY FLOW:
GR/Production → Inspection Lot (QA01) → 
Sample to LIMS → Testing → 
Results to SAP (QA11) → 
Usage Decision (QA32) → 
Stock Status Updated

MAINTENANCE FLOW:
Equipment (IE03) → Maintenance Plan (IP01) → 
Maintenance Order (IW31) → 
Execution → Confirmation → 
Technical Complete (IW32)
```

---

## Material Types

```
ROH    - Raw Material (Rohstoff)
HALB   - Semi-Finished Product
FERT   - Finished Product
HIBE   - Trading Goods
VERP   - Packaging Material
UNBW   - Non-Valuated Material
ERSA   - Spare Parts
```

---

## Movement Types (Goods Movements)

```
101  - Goods Receipt for Purchase Order
102  - Goods Receipt for PO - Reversal
122  - Return Delivery to Vendor
161  - Returns for Purchase Order
201  - Goods Issue for Cost Center
202  - Goods Issue for Cost Center - Reversal
221  - Project Issue
261  - Goods Issue to Production Order
262  - Goods Issue to Production Order - Reversal
311  - Transfer Posting (Storage Location)
551  - Withdrawal from stock (scrapping)
561  - Initial entry of stock (initial upload)
601  - Goods Receipt from Delivery
```

---

**END OF SAP TERMINOLOGY GUIDE**

---

This guide contains 200+ terms, abbreviations, and definitions specific to SAP in pharmaceutical manufacturing. Use Ctrl+F to search for specific terms.
