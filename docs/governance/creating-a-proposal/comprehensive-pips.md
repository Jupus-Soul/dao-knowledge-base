---
title: "Comprehensive PIPs"
description: "Format for Projects Outside the Ecosystem Fund, requiring multiple funding proposals."
---

## Overview

When a project requires funds exceeding the 5% Vault limit established by the Ecosystem Fund (PIP-4, currently 11,204,716 ATLAS as of 12-Jul-2025), it should be structured as a Comprehensive PIP, which breaks the project down into phases consistent with the 5% limit per PIP. Each proposal phase can request up to the full ecosystem fund limit and will be voted on separately.

## Structure for Comprehensive PIPs

### 1. Proposal Plan (not separately voted on, included with each phase)

A Proposal Plan must be created that includes:

**1.1 Proposal Plan Header**

* Title format: "PIP-\[X]: \[Project Name] - Comprehensive PIP"
* Author(s) of the overall project

**1.2 Proposal Plan Content**

* Total Project Summary: Complete overview of the entire project spanning all phases
* Total Project Motivation: Comprehensive explanation of why the entire project is needed
* Proposal Plan Specification: High-level technical and functional requirements for the complete project
* Proposal Plan Stakeholder Impact: Impact analysis covering the whole project scope
* Proposal Plan Timeline: Overall project timeline showing how all phases interconnect (up to 1 year)
* Total Cost Breakdown:
  * Complete financial summary of all phases
  * Justification for exceeding single-proposal limits
  * Total project cost and expected ROI/benefits
* Proposals Dependencies: Clear mapping of how the phases depend on each other
* Risk Assessment: 
  * Consequences for failure to fund subsequent phases
  * Project-wide risks and mitigation strategies

## 2. Phase Requirements (each phase is a separately voted PIP)

**2.1 Naming Convention**

* Format: "PIP-\[X]: \[Project Name] - Phase \[Y] - \[Description]"
* Example: "PIP-15: Atlas Trading Platform - Phase 1 - Core Infrastructure"

**2.2 Phase PIP Structure**\
\
Each phase PIP must contain all nine standard format sections:

1. Header (referencing Comprehensive PIP)
2. Summary (specific to this phase)
3. Motivation (phase-specific rationale)
4. Specification (detailed phase requirements)
5. Stakeholder Impact (phase-specific impacts)
6. Implementation Details (phase execution plan)
7. Timeline (phase-specific timeline with dependencies)
8. Cost & Resource Allocation (Ecosystem Fund)
9. Additional Details (phase-specific conflicts/versions)

**2.3 Additional Phase PIP Requirements**

* **Proposal Plan Reference:** Clear reference to the [Proposal Plan](#1-proposal-plan-not-separately-voted-on-included-with-each-phase)
* **Phase Dependencies:** Explicit listing of which previous phases must be complete
* **Phase Deliverables:** Functional completion of features or deliverables for each phase

### 3. Voting and Approval Rules

**Conditional Approvals:**

* Each phase PIP vote is an independent vote
* Rejection of any phase proposal does not automatically cancel the remaining phases.
* Authors may propose modified versions of a rejected phase PIP 
* There must be at least thirty days between the voting of the phases

### 4. Documentation Standards

**Cross-Reference Requirements:**

* All phase PIPs must reference the [Proposal Plan](#1-proposal-plan-not-separately-voted-on-included-with-each-phase)
* Precise dependency mapping between phases
* Consistent terminology and definitions across all documents\
  \
  —

### Notes: - The [**Proposal Plan**](#1-proposal-plan-not-separately-voted-on-included-with-each-phase) is not voted on; it is referenced for clarity.
