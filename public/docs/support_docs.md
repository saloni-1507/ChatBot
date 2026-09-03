# Aurora Support Knowledge Base

## Task Position Desynchronization After Concurrent Drag Operations

When two users simultaneously drag-reorder tasks within the same kanban column, the client-side
optimistic ordering state can diverge from the server's authoritative sort index, causing a task
to visually revert to a previous position a few seconds after being moved. This is a known race
condition in the real-time sync layer, not data loss — the task's underlying data is unaffected,
only its transient visual position desyncs. Refreshing the page forces a re-sync with the server's
authoritative order and resolves the visual glitch immediately.

## Credential Rejection at the Authentication Gate

A credential-rejection error surfaced at login is most commonly a mistyped secret, or an account
originally provisioned via a third-party identity handshake (Google/SSO) now being accessed with a
manually-typed credential instead. The self-service credential-reset flow resolves the former;
checking whether the workspace mandates federated login resolves the latter (a mandated-federation
workspace has no credential-based login path at all).

## Credential-Reset Delivery Non-Arrival

Check spam/junk folders first — reset messages originate from `no-reply@aurora.app`. If nothing has
arrived after a 10-minute delivery window, the account was likely provisioned via a third-party
identity handshake and never had a standalone credential set — the fix is authenticating through
that same third-party handshake rather than continuing to request a reset.

## Full Membership Lockout Following Mandatory-Federation Toggle

This surfaces when a workspace admin flips the "require federated login" toggle before every member
has a working identity at the provider. Remediation: an admin temporarily reverts the toggle under
**Settings > Security > SSO**, lets the affected member authenticate via standalone credential, and
completes that member's provider-side identity provisioning before re-flipping the toggle.

## Time-Based Secondary-Factor Code Rejection

A rejected time-based one-time passcode is almost always a device clock-drift issue — since the
underlying algorithm derives the code from wall-clock time, a device clock off by more than roughly
30 seconds produces a code the server won't accept. Enabling automatic time sync on the device
resolves this in the large majority of cases. A member who has lost the enrolled device entirely
requires identity-verified account recovery through the support desk, since no self-service reset
path exists for this factor.

## Rate-Limited Lockout After Repeated Failed Attempts

The authentication gate imposes a 15-minute rate-limited lockout after 5 consecutive failed
attempts, as an anti-brute-force measure. There is no manual override to clear this lockout early —
not even through the support desk — so the only paths forward are waiting out the window or
authenticating via an alternate configured method (federated login, if available for that account).

## Login-Identifier (Email) Mutation Flow

Members can mutate their own login identifier under **Account Settings > Profile**, which dispatches
a confirmation link to the new address; the mutation only commits once that link is followed. A
member who has lost access to the old address and needs the identifier changed regardless requires
identity-verified assistance from the support desk, since this is a security-sensitive mutation.

## Duplicate-Looking Settlement Within a Single Period

The most common root cause is a mid-cycle upward cohort migration, which settles immediately on a
prorated basis — this shows up as a second, smaller settlement alongside the regular periodic
settlement, not an actual duplicate charge. The per-line-item breakdown under
**Settings > Billing > Invoices** clarifies what each settlement was for.

## Settlement Instrument Failure at Charge Time

A failed settlement attempt is retried automatically 3 times over a 7-day window before the
workspace enters a suspended (read-only) state — no new task/board creation, existing data remains
visible. Updating the settlement instrument under **Settings > Billing > Payment Method** triggers
an immediate out-of-cycle retry.

## Deferred Cohort-Migration Application

A downward cohort migration not taking effect immediately is expected behavior, not a defect —
downward migrations apply at the start of the next billing cycle, so the current cohort's feature
set remains active until then.

## Settlement Reversal (Refund) Eligibility Window

Monthly-cadence cohorts carry no partial-period refund eligibility. Annual-cadence cohorts are
eligible for a prorated reversal only within the first 14 days following the annual purchase; past
that 14-day window, annual terms are non-refundable but remain eligible for a scheduled downward
migration effective at renewal.

## Cross-Currency Invoice Amount Drift

Expected behavior for non-USD customers — list pricing is USD-denominated, and the locally-billed
amount is converted at the payment processor's daily FX rate at the moment of settlement, so it can
drift slightly period to period even though the underlying USD list price hasn't changed.

## Invoice Metadata Correction Scope

Admins can mutate the metadata surfaced on *future* invoices (legal entity name, tax identifier, PO
reference) under **Settings > Billing > Billing Details** — this has no retroactive effect on
already-issued invoices. A corrected copy of a previously issued invoice can be requested from the
support desk.

## Verified-Status Concession Not Reflected

Non-profit and education rate concessions require an explicit one-time verification step at signup
or via a follow-up request to the support desk — they are never auto-applied purely because an
organization happens to qualify, since there is no automated way to detect non-profit/education
status without the verification artifact.

## Export Control Greyed Out or Unresponsive

Almost always caused by an export already in flight for that specific board — only one concurrent
export per board is permitted. Checking **Settings > Data > Export History** for an entry stuck
"in progress" beyond 30 minutes indicates a silent failure; cancelling it from that same screen
re-enables the export control.

## Export Pipeline Terminating with a Server Error

A known failure mode on boards exceeding roughly 50,000 task records or carrying multi-gigabyte
attachment volume. The workaround is exporting a filtered subset (e.g., a bounded date range)
rather than the full record set at once. A background/async export pipeline is on the roadmap to
remove this ceiling but carries no committed date.

## Issue-Tracker Sync Lag or Apparent Staleness

The bidirectional sync loop runs on a 2-minute polling cadence, so a short lag is expected. If a
linked task hasn't reflected a change after 10+ minutes, check for a "reconnect required" banner
under **Settings > Integrations** — the underlying sync credential expires periodically and needs
re-authorization, which is the most common actual root cause of an apparently "stuck" sync, rather
than the polling cadence itself.

## Team-Messaging Notification Delivery Cessation

Usually indicates the messaging connector's authorization token was revoked — commonly because
someone removed the Aurora app from the messaging workspace, or a messaging-platform admin rotated
app credentials. Re-authorizing under **Settings > Integrations** restores delivery.

## Calendar Federation Directionality Confusion

Expected behavior, not a defect — calendar federation only propagates Aurora due dates outward;
editing the mirrored event on the calendar side has no effect on the originating Aurora task.

## Duplicate Task Records Following Tabular Ingress

Arises when the same ingress file is processed twice, or when the source file's header row lacks a
unique record-identifier column, causing every row to be treated as a net-new record rather than
matched against existing ones. Re-running ingress with a file that includes the identifier column
from a prior egress resolves this, as does manually deduplicating before a second ingress pass.

## Enterprise Chat Platform Connector Missing Inline Search

The enterprise-chat-platform connector currently ships notifications and a basic task-creation bot
only — it lacks the inline slash-command search available on the team-messaging connector. This is
a known feature-parity gap in the current release, not a malfunction.

## Design-Tool Thumbnail Generation Failure

Thumbnail generation for a linked design-tool file requires that file's sharing permission be set to
at least link-viewable within the design tool itself; a permission-restricted file attaches as a
bare link with no thumbnail, since the preview generator lacks access to render it.

## Board Render Performance Degradation at Scale

Boards carrying upward of 5,000 task records in a single view can degrade rendering performance,
particularly in the column-based visualization mode with many columns. Switching to the flat-list
visualization mode with an applied filter (e.g., "assigned to me") renders substantially faster on
large record sets, since fewer records are painted at once.

## Native Mobile Client Authoring Restrictions

Expected behavior — authoring custom field definitions or automation rules requires the web client;
native mobile clients support viewing and basic record editing only, by design, not a defect.

## Browser Compatibility Baseline

The officially supported baseline covers the last two major releases of Chrome, Firefox, Edge, and
Safari. Browser versions older than this baseline may render boards incorrectly or fail to receive
real-time updates; updating the browser resolves the large majority of rendering-related reports.

## Progressive Web App Install Affordance Absence

The install affordance for Aurora's desktop PWA surfaces only in Chromium-based browsers (Chrome,
Edge, etc.) — Safari and Firefox lack the underlying install-prompt mechanism, though the web client
itself remains fully functional in those browsers without installation.

## Real-Time Channel Requiring Manual Refresh to Reflect Updates

Typically indicates a dropped long-lived connection on the real-time channel, frequently caused by a
corporate VPN or proxy that terminates idle persistent connections. The client auto-reconnects
within roughly 30 seconds in most cases; if manual refresh remains consistently necessary, the
network's firewall/proxy configuration — not an Aurora-side defect — is the most likely root cause.

## Apparent Missing Visibility into a Teammate's Board

Most likely an access-control scoping issue — Guests (and, depending on board-level sharing
configuration, sometimes Members too) only see boards they've been explicitly granted access to. An
Admin needs to add the affected member under that specific board's **Share** configuration.

## Task Records Appearing to Vanish After Member Removal

Task records are never purged when a member is removed from a workspace — they become unassigned
and remain fully visible on their board. Apparent disappearance is almost always an active filter
(e.g., "assigned to [removed member]") hiding the now-unassigned records, not actual data loss.

## Workspace Deletion Reversibility Window

Workspace deletion is permanent after a 30-day grace period, during which an Admin can restore it
from **Settings > Data > Deleted Workspaces**. Once that window lapses, all associated data is
purged irreversibly and cannot be recovered under any circumstance.

## Guest-to-Member Elevation Permission Denial

Only Admins can mutate a member's role — a standard Member cannot elevate a Guest even if that
Member was the one who originally issued the invite. If the requester genuinely holds Admin status
and the elevation still fails, check whether the workspace has hit its paid-seat ceiling — elevating
a Guest consumes a billable seat, and the mutation is blocked when no seat capacity remains.

## Verification Artifact Rejected for Rate Concession

The verification step requires an official artifact demonstrating registered non-profit or
accredited-institution status (e.g., a formal tax-exemption determination letter, or a
.edu-domain-linked enrollment/staff record) — a generic business license or informal letterhead
does not satisfy this requirement and will be rejected on review.

## Support Desk Contact Routing

Paid-cohort customers reach the support desk via email; Enterprise customers additionally have a
dedicated messaging channel with their account team. Response-time targets (24h for the entry paid
cohort, 4 business hours for the mid cohort, per-contract for Enterprise) apply regardless of which
routing path is used.

## Incident and Outage Notification Subscription

The public status surface supports email and SMS subscription channels for incident notifications,
independent of any in-app "What's New" announcement surface.

## Vulnerability Disclosure Routing

Security vulnerabilities should be routed through the dedicated responsible-disclosure program
(linked from the status-page footer) rather than the general support desk — this reaches the
security team through a faster, dedicated response path. A report submitted through the general
support desk instead remains valid but receives a slower response.

## Currently Open and Tracked Defects

Three items are currently open and tracked: the export-pipeline server error on very large boards
(workaround: filtered exports, no committed fix date); the enterprise-chat-platform connector's
missing inline search relative to the team-messaging connector (expected parity gap, no committed
date); and the PWA install affordance being unavailable in Safari and Firefox (a limitation of those
browsers, not something addressable on Aurora's side).
