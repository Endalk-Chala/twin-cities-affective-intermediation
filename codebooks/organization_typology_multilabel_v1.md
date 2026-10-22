# Organization Typology — Multi-Label Codebook v1

## Purpose

Organizations in the Twin Cities immigrant/refugee communication ecosystem frequently span more than one institutional role. This typology therefore uses **multi-label classification** rather than forcing each organization into a single mutually exclusive category.

An organization may receive any number of applicable labels, provided each label is supported by public organizational evidence or documented program activity during or proximate to the study period.

## Analytical principle

The typology captures **organizational position and function**, not a single organizational identity. For example, one organization may simultaneously be `legal`, `advocacy`, `service`, and `community_rooted`.

Labels should not be inferred from news coverage alone. They should be coded from organizational mission, programs, official descriptions, and verified activity.

## Equal-weight membership rule

All labels coded as `verified` are treated as **equal-weight organizational memberships at the infrastructure stage**. No verified label is designated primary, secondary, dominant, or more important than another simply because it appears more central in an organization's public identity or is more visible in news coverage.

Operationally:

- a verified label represents membership in that organizational category;
- verified labels carry equal analytical weight by default;
- `type_status` records evidentiary certainty and must not be converted into an analytical weight;
- `probable` and `candidate` labels remain available for audit and sensitivity analysis but should not be silently treated as equivalent to verified memberships in primary analyses;
- media prominence, frequency of quotation, organizational size, budget, public visibility, or journalist characterization must not be used to up-weight a typology label;
- if a later statistical or network analysis requires weighting, collapsing, or a primary-type variable, that transformation must be derived separately from the unchanged multi-label bridge table and documented as an analysis-stage decision.

This rule ensures that any stronger relationship between an organizational role and an outcome such as source visibility, national amplification, or affective framing emerges from the observed data rather than from researcher-assigned hierarchy in the typology itself.

## Core labels

- `community_rooted` — embedded in, governed by, or primarily serving a specific immigrant, refugee, ethnic, racial, linguistic, or diasporic community.
- `ethnocultural` — explicitly organized around an ethnic, national-origin, cultural, or linguistic community.
- `refugee_resettlement` — provides formal refugee reception, resettlement, sponsorship, or post-arrival integration services.
- `immigrant_integration` — supports immigrant/refugee integration through orientation, navigation, education, employment, civic participation, or settlement assistance.
- `direct_service` — provides material or social services such as food, housing, employment, health navigation, education, transportation, case management, or basic-needs support.
- `legal` — provides legal representation, legal advice, legal information, rights education, or legal-system navigation.
- `advocacy` — engages in public-policy advocacy, rights advocacy, institutional accountability, or organized public pressure.
- `organizing` — builds collective participation, membership, mobilization, protest, mutual aid, rapid response, or community power.
- `faith_based` — formally affiliated with or substantially organized through a religious institution, faith network, or religious mission.
- `gender_based` — has a central mission addressing women, gender, gender-based violence, sexual violence, domestic violence, or gendered inequity.
- `health_wellbeing` — provides or centers physical health, mental health, trauma recovery, public health, or wellbeing services.
- `education_workforce` — centers education, language learning, credentialing, employment, workforce development, or career advancement.
- `housing_economic` — centers housing, economic development, financial capability, entrepreneurship, tenancy, or material economic stability.
- `youth_family` — centers children, youth, parents, caregivers, or family support.
- `civil_rights_human_rights` — centers civil liberties, human rights, anti-discrimination, or rights monitoring.
- `coalition_network` — primarily functions as a coalition, alliance, network, or coordinating body linking multiple organizations or constituencies.
- `media_information` — produces or distributes community information, media, public education, or information-access services as a substantial organizational function.
- `other` — analytically relevant institutional role not captured above; requires coder note.

## Coding structure

Use a separate organization-typology bridge table rather than a single delimited field in the master organization table.

One row = one organization × one typology label.

Recommended fields:

- `org_id`
- `organization`
- `type_label`
- `type_status`: `verified`, `probable`, `candidate`, `not_applicable`
- `evidence_basis`: `mission`, `programs`, `official_about_page`, `annual_report`, `government_or_partner_listing`, `other`
- `evidence_url`
- `evidence_note`
- `coding_date`

This normalized structure allows an organization to have multiple labels without creating wide, sparse tables and supports many-to-many analysis.

## Analytical use

The multi-label typology can later be joined to organization-news relations to compare:

- source visibility by organizational position;
- media-layer reach by organizational type;
- direct-quote probability by organizational role;
- source prominence across overlapping organizational functions;
- affective framing by role;
- local-to-national amplification by role combination;
- whether specific combinations, such as `legal + advocacy` or `community_rooted + direct_service`, occupy distinctive media positions.

## Important rule

Do not force a primary type for analysis unless a specific statistical model requires one. If a model requires simplification, derive a temporary analytic variable from the underlying multi-label data and document the derivation separately.
