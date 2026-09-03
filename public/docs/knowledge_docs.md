# Aurora Product Knowledge Base

## Org Genesis and Vertical Positioning

Aurora is a project-management platform for software and cross-functional teams, built around
boards, tasks, and lightweight automation. Aurora was built to be fast to adopt (a new workspace
can be productive within a day) while still scaling to enterprise governance needs (SSO, SCIM,
audit logs) as a company grows. Aurora was founded in 2019 and is used by teams ranging from
5-person startups to 5,000-person enterprises across engineering, marketing, and operations teams.

## Tiered Entitlement Structure: Free Cohort

The entry-level entitlement cohort caps a workspace at 5 seats, 3 boards, and 1,000 total task
records, with community-only support channels and no integration connectors. Custom field
definitions are unavailable at this tier. Activity retention is bounded to a 7-day lookback window.

## Tiered Entitlement Structure: Starter Cohort

The Starter cohort is priced at $9 per seat per billing period (monthly cadence) or $7.20 per seat
per billing period (annual cadence, a 20% rate reduction). Board and task record counts are
unbounded. Activity retention extends to a 30-day lookback window. Support is routed through email
with a 24-hour response-time target. Tabular (CSV) data egress is included.

## Tiered Entitlement Structure: Team Cohort

The Team cohort is priced at $19 per seat per billing period (monthly) or $15.20 per seat per
billing period (annual). Beyond everything in the Starter cohort, this tier unlocks: custom field
definitions (text, numeric, single/multi-value dropdown, date, boolean checkbox); third-party
connector access for Slack and Jira; one-directional calendar federation with Google Calendar;
a rules-engine automation ceiling of 50 concurrently active rules per workspace; guest-seat
provisioning up to 10 external collaborators; programmatic API access throttled at 1,000 calls per
rolling hour; a 4-business-hour support response-time target; PDF data egress; and unbounded
activity retention.

## Tiered Entitlement Structure: Enterprise Cohort

The Enterprise cohort uses custom, sales-negotiated pricing. Beyond everything in the Team cohort,
this tier adds: federated identity login (SSO), automated identity lifecycle sync (SCIM), a named
account manager, a contractual 99.9% uptime commitment, immutable audit trails, network-level IP
allowlisting, configurable data-retention governance policies, an unbounded automation-rule
ceiling, unbounded guest-seat provisioning, and a raised programmatic throttle of 10,000 calls per
rolling hour (further negotiable for verified high-volume integration partners).

## Entitlement Transition Timing (Cohort Migration)

An upward cohort migration (upgrade) takes effect immediately, with the price difference prorated
against the remainder of the current billing cycle. A downward cohort migration (downgrade) is
deferred until the *start of the next* billing cycle — the workspace retains its current cohort's
feature set until the cycle boundary is reached. An annual-term workspace that schedules a downward
migration before its term completes receives no refund for the unused portion; the migration is
queued to apply once the annual term lapses.

## Verified-Status Rate Concessions

A 30% rate concession applies to the Team and Enterprise cohorts for organizations with verified
non-profit registration status, established via a one-time document upload at signup or a
follow-up request to the sales desk. A separate 50% concession on the Team cohort applies to
accredited academic institutions with a verifiable .edu domain or equivalent credential. Neither
concession is auto-applied by domain heuristics or self-attestation — both require the explicit
verification step regardless of underlying eligibility.

## Billing Cadence and Settlement Instruments

Invoice generation occurs on the same calendar day each period as the original signup date (or the
nearest following business day, when that date doesn't exist in a given month — e.g. the 31st).
Accepted settlement instruments are credit/debit card universally, plus wire transfer or ACH with
net-30 terms exclusively for the Enterprise cohort. PayPal and cryptocurrency are not accepted
settlement instruments. All list pricing is USD-denominated; non-USD customers are billed an
equivalent converted at the payment processor's daily FX rate at the moment of settlement, which
can cause the exact charged local-currency amount to drift slightly period to period even though
the USD list price is static.

## Federated Identity Login Availability

Federated identity login (the mechanism by which a member authenticates through their
organization's identity provider rather than an Aurora-native credential) is gated to the
Enterprise cohort. Configuration lives under **Settings > Security > SSO**. Once a test
authentication succeeds, an admin may toggle "Require SSO for all members," which disables
credential-based authentication workspace-wide — any member lacking a provisioned identity at the
provider is locked out until an admin completes their provisioning, so this toggle should only be
flipped after confirming every member has a working provider-side identity.

## Supported Federation Standards for Login

The federated login capability speaks two standards: **SAML 2.0** and **OIDC** (OpenID Connect).
Either standard interoperates with any conformant identity provider — Okta, Azure AD, Google
Workspace, and OneLogin are commonly used examples. Provisioning a SAML-backed provider requires
uploading that provider's metadata XML descriptor. Provisioning an OIDC-backed provider instead
requires entering a client ID, client secret, and discovery URL. Legacy directory protocols such as
LDAP or Kerberos are not among the supported federation standards.

## Automated Identity Lifecycle Sync (Directory Provisioning)

Automated identity lifecycle sync is a distinct Enterprise-only capability from federated login
itself — the lifecycle-sync layer governs account provisioning/deprovisioning, while the login
layer governs authentication. With lifecycle sync enabled, the upstream identity provider can push
account creation on hire, role/attribute updates on change, and account deactivation on departure,
removing manual workspace-membership upkeep. (This capability is commonly referred to by its
underlying protocol acronym in enterprise IT circles.)

## Secondary Authentication Factor (TOTP-Based)

A secondary, time-based one-time-passcode authentication factor is available on every cohort
including the free entry tier — this layer is independent of and unrelated to federated login.
Each member configures this individually under **Account Settings > Security**. A workspace using
federated login can still permit individual members to layer on this secondary factor, though
doing so is uncommon since federated login already centralizes authentication trust at the
provider.

## Third-Party Attestation and Cryptographic Posture

Aurora holds a SOC 2 Type II attestation report, available on request to Enterprise customers.
ISO 27001 certification is in progress, targeted for completion within the current fiscal year.
Data at rest is encrypted under AES-256; data in transit is encrypted under TLS 1.2 or higher.

## Network-Level Access Restriction

Restricting workspace reachability to an admin-specified set of network address ranges is an
Enterprise-exclusive capability — any authentication attempt originating outside the configured
ranges is rejected before credentials are even evaluated.

## Data Locality and Cross-Border Processing Posture

Aurora's primary infrastructure footprint runs in AWS us-east-1. Enterprise customers may request
processing exclusively within AWS eu-west-1 at no additional cost, arranged via a coordinated
workspace migration with the Enterprise onboarding team, typically completing within 5 business
days. Aurora maintains a GDPR-compliant posture for EU customers and will countersign a Data
Processing Addendum on request for any paid cohort.

## Regulated Health-Data Suitability

Aurora does not offer a compliance configuration suitable for protected health information (PHI)
under HIPAA, regardless of cohort — no workspace should be used to store PHI.

## Connector Catalog: Team Messaging

The team-messaging connector posts task-lifecycle notifications into a designated channel and
exposes inline slash commands (`/aurora create`, `/aurora search`) for creating or locating tasks
without context-switching away from the messaging client. Gated to the Team cohort and above.

## Connector Catalog: Issue Tracker Bidirectional Sync

The issue-tracker connector maintains bidirectional field sync (status, assignee, comment thread)
between a linked Aurora task and its counterpart issue. Gated to the Team cohort and above. The
sync loop runs on a 2-minute polling cadence rather than a push-based real-time channel.

## Connector Catalog: Calendar Federation

Tasks carrying a due date surface on a linked calendar via one-directional federation (Aurora is
the source of truth; the calendar is a read-only mirror) — edits made on the calendar side do not
propagate back to the originating task. Gated to the Team cohort and above.

## Connector Catalog: Source-Control Lifecycle Linking

Linking a pull/merge request to a task drives automatic status transitions: the task moves to
"In Review" when the request opens and "Done" when it merges. Gated to the Team cohort and above.

## Connector Catalog: Workflow Automation Hub

The generic workflow-automation-hub connector (available on every paid cohort, Starter and above)
bridges Aurora into a broader third-party automation ecosystem. Usage through this connector counts
against the same programmatic throttle ceiling as direct API calls.

## Connector Catalog: Enterprise Chat Platform Parity Gap

The enterprise-chat-platform connector (distinct from the team-messaging connector above) currently
ships with a reduced feature surface — task-lifecycle notifications and a minimal task-creation bot
only, released after the team-messaging connector and not yet at feature parity. Specifically, the
inline slash-command search capability present in the team-messaging connector has not shipped here.
Gated to the Team cohort and above.

## Connector Catalog: Design-Tool Link Previews

Attaching a design-tool file link to a task auto-generates a thumbnail preview, gated to any paid
cohort — contingent on the linked file's sharing permission being set to at least
link-viewable, since the preview generator cannot render a file it lacks permission to access.

## Programmatic Access Throttling Tiers

Programmatic (REST) access is unlocked starting at the Team cohort; the Starter cohort cannot reach
the API surface directly. Throttle ceilings are 1,000 calls/hour on Team and 10,000 calls/hour on
Enterprise (negotiable upward for verified high-volume integration partners). Credentials are
minted under **Settings > API** and scoped at the workspace level rather than the individual-user
level.

## Board Visualization Modes

A board's underlying task set can be rendered in three visualization modes — a flat list, a
drag-and-drop column layout, and a due-date-plotted calendar. All three modes read from the same
underlying record set; switching modes is a pure re-render, not a data fork or filter.

## Custom Field Type Palette

Custom field definitions (gated to Team and above) support six primitive types: single-line text,
numeric, single-select dropdown, multi-select dropdown, date, and boolean checkbox — each
independently markable as required or optional per board.

## Rules-Engine Automation Model

The automation subsystem follows a trigger-condition-action model (e.g., "when a task transitions
to Done, reassign it to the board owner and post to the team-messaging connector"). Active-rule
ceilings are 50 per workspace on Team, unbounded on Enterprise. Rules live under each board's
**Automation** tab and can be paused without being deleted.

## Reporting Surfaces and Egress Formats

Reporting surfaces include burndown visualizations (completion velocity against a target date) and
workload distribution views (per-assignee task load, useful for spotting overallocation). Reports
can egress as tabular CSV (Starter and above) or paginated PDF (Team and above) from any board's
**Export** menu, or be scheduled for automatic email delivery on a daily/weekly/monthly cadence
(Team and above).

## Access-Control Role Hierarchy

Every workspace member holds exactly one of three roles: Admin, Member, or Guest. Admins govern
billing, connector, and security configuration. Members can create/edit boards and tasks but cannot
touch workspace-level configuration. Guests (Team cohort and above) are scoped to explicitly
assigned boards only — no visibility into unassigned boards, the full member roster, or workspace
settings.

## Native Mobile Client Feature Parity

Native mobile clients (iOS and Android) cover core board/task operations, push notifications, and
offline-capable viewing with sync-on-reconnect. Custom field definitions and automation-rule
authoring are view-only on mobile and require the web client to author. A tablet-optimized
split-view client ships as a separate download from the phone client.

## Desktop Delivery Model

No native Windows or macOS binary exists. The recommended desktop-equivalent experience is
installing the web client as a PWA (Progressive Web App) via the browser's native install affordance.

## Cross-Workspace Search Scope

Search operates at the workspace scope (not scoped to a single board) and supports faceting by
assignee, due date, custom-field value, and board. Result sets are implicitly filtered to boards the
searching member can access.

## Per-Event Notification Channel Matrix

Notification routing is configured per-member under **Account Settings > Notifications**, across
four channels (email, in-app, mobile push, team-messaging connector if linked), each independently
toggleable per event category: assignment, due-date approach, comment mention, and watched-task
status change.

## Bulk Data Egress and Ingress Pathways

Full-workspace egress (all boards, tasks, comments, attachments) is available to Admins under
**Settings > Data > Export Workspace**, delivered as a downloadable archive within minutes for
small workspaces or up to an hour for very large ones. Ingress pathways cover a basic CSV
task-list format and a purpose-built importer for one third-party board tool that preserves board/
list/card structure as Aurora boards/tasks/statuses. A second importer, for a different popular
project tool, is in a beta/request-access state.

## Effort-Logging Subsystem

Effort logging (built into Team and Enterprise cohorts) lets members record time against a task
either via manual entry or a start/stop timer; workload and reporting surfaces can be filtered to
show logged hours per assignee or per board.

## Accelerator Key Bindings

Accelerator key bindings are available throughout the web client (press `?` for the full reference)
for high-frequency actions — task creation (`c`), self-assignment (`a`), and quick search (`/`).

## Assistive-Technology Conformance Target

The web client targets WCAG 2.1 AA conformance, with full keyboard-only navigation and
screen-reader-tested labeling across core board/task interactions. A formal conformance report
(VPAT) is available to Enterprise customers on request.

## Interface Localization Coverage

The client chrome is localized into English, Spanish, French, German, Japanese, and Portuguese.
User-generated content (task titles, descriptions, comments) is never machine-translated — only
surrounding chrome elements (menus, buttons, labels) shift language, driven by the browser's locale
setting or a manual override under **Account Settings > Language**.

## Availability Commitment and Historical Uptime

The public status surface exposes real-time and historical availability data. Only the Enterprise
cohort carries a contractual 99.9% availability commitment with service credits for breaches,
detailed in the Enterprise contract — sub-Enterprise cohorts carry no contractual guarantee, though
observed availability is consistent across cohorts since they share the same underlying
infrastructure.

## Initial Workspace Bootstrapping Flow

A freshly created workspace walks through a guided bootstrap flow: teammate invitation, first-board
creation (blank canvas or a template — software-sprint, marketing-campaign, and general
task-tracking templates ship by default), and an optional 15-minute onboarding call for Team/
Enterprise signups, bookable from the welcome email. Most teams report full workflow migration off
their prior tool within the first week.

## Multi-Tenant Account Membership

A single login credential can hold membership across multiple independently billed workspaces
(e.g., a consultant serving several client organizations) — billing, cohort selection, and invoicing
are all scoped per-workspace, not per-account. No self-service tool exists to merge two workspaces
into one; the support org can perform a manual data migration for Enterprise customers on request.

## Trial-Period Mechanics for Paid Cohorts

The Team and Enterprise cohorts offer a 14-day full-feature trial requiring no settlement instrument
up front. On trial expiry without a settlement instrument added, the workspace reverts automatically
to the free entry cohort (not a surprise charge) — any data exceeding that cohort's caps becomes
read-only until either a settlement instrument is added or the workspace is trimmed under the free
cohort's limits.

## Guest-to-Member Role Elevation

An Admin can elevate a Guest to full Member status at any point from the workspace roster view,
which simultaneously lifts the board-level access restriction that guest status carries.

## Release Cadence and Change Visibility

Aurora ships product changes on a roughly biweekly cadence; the in-app "What's New" surface (bell
icon, top right) shows the trailing 90 days of changes. Recent notable additions include the
enterprise-chat-platform connector, the design-tool link-preview connector, and WCAG 2.1 AA
accessibility work across board/task views.

## Forward-Looking Roadmap Disclosure

Publicly disclosed forward work includes a native desktop binary (currently PWA-only) and general
availability for the second project-tool importer (currently beta/request-access) — neither carries
a committed date and neither should be represented to a customer as a firm delivery date.
