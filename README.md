# PROG103_FinalProject_BSEM1201F_Group3
An open-source Clinic Queue Management System built in Python using Tkinter. Features robust client-side input validation, architectural separation of GUI and business logic, secure local JSON data interoperability, and an administrative privacy-masked authentication system. Final Project for PROG103.

# UNIVERSITY / Limkokwing Creative Technology
### Faculty of Information and Communication Technology

---

#  CLINIC QUEUE MANAGEMENT SYSTEM
**COURSE:** PROG103 - Final Project  
**SECTION:** BSEM1201F  
**GROUP:** Group 3  
**DATE OF SUBMISSION:** June 12, 2026  

---

## GROUP MEMBERS & PROJECT CONTRIBUTIONS

| Student Name | Student ID | Core Project Role | GitHub Username |

| Gibril Bangura | `905005708` | UI Design & Interface Architecture | @banguragibril |

| Sharon Mary Koroma| `905006201` | Input Validation & Data Serialization | @ramathasharon |

| Abdul Aziz Sesay | `905005987` | Security Masking & Compliance Documentation | @zizcodes2025 |


---

# Clinic Queue Management System
**Course:** PROG103 Final Project  
**Class/Group:** BSEM1201F - Group 3  
**License:** MIT Open Source License  

---

##  Project Overview
This Clinic Queue Management System is an open-source administrative desktop application built in Python using Tkinter. It stream-lines the patient check-in workflow, processes waiting lines sequentially, tracks real-time clinic queue metrics on an interactive dashboard, and aggregates patient notes dynamically based on their appointment type.

---

##  Advanced Architectural Layout & Quality (Section 8)
To meet professional standard workflows, the architecture highlights several core engineering principles:

* **Separation of GUI and Logic:** The system architecture is completely decoupled. `clinic_queue_system.py` handles the presentation layer and GUI controls exclusively, while `backend.py` isolates data manipulation, record serialization, and input sanitation functions.
* **Robust Input Validation:** The backend rigorously sanitizes user strings prior to state mutation. It features explicit format validation rules for Patient Names, Dates of Birth (YYYY-MM-DD), Phone Numbers, Emails, and unique Ticket IDs using regular expressions (`re`).
* **Clean Code & Meaningful Naming:** Functions and variables use highly explicit, descriptive naming conventions (e.g., `validate_emergency_phone()`, `load_data_bridge()`, `current_patient`) accompanied by structured structural comments.

---

##  Data, Privacy & Compliance Framework (Section 7)
This application was engineered with conscious adherence to modern digital healthcare data management baselines:

### 1. Data Accessibility
Queue data is retained dynamically via local data streaming. Authorized clinic staff can explicitly view historical and current logs on demand via the user interface or by accessing the structured runtime state directly.

### 2. Interoperability
The system saves data into standard, widely adopted JavaScript Object Notation (`clinic_records.json`). This ensures that the structured output can be seamlessly integrated, processed, or exported to larger Electronic Health Record (EHR) databases or third-party analytical pipelines without proprietary restrictions.

### 3. Basic Privacy Considerations
To protect administrative access from "shoulder surfing" in high-traffic clinical areas, the entry system masks passwords (`show="*"`) and features a dynamic visual visibility toggle.

### 4. Ethical Use of User Data
Patient medical data is handled under strict ethical constraints. Records are retained strictly locally on internal clinic storage volumes rather than being broadcasted across unencrypted external public networks, mitigating external data exposure risks.

---

##  Installation & Setup
1. Clone this repository to your local system.
2. Ensure you have Python 3.x installed.
3. Make sure the `icons/` asset folder resides in the root directory.
4. Launch the application by executing the interface script:
   ```bash
   python clinic_queue_system.py
