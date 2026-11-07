# Page Acceptance — Checklists

Loaded on demand. Keep the skill's scope discipline; these lists expand steps 3–4, not the task.

## Choosing the boundary

Pick the boundary that this change could plausibly break, not the one easiest to run:

| Change | Boundary worth probing |
|---|---|
| New required field or validation rule | Submit empty, then submit an invalid format |
| New permission or menu entry | Load the page as a role without the permission |
| New list filter or sort | Filter to zero rows, then reset |
| New pagination or page-size control | Last page, then filter while on page > 1 |
| New status/enum control | One value rendered and one persisted after reload |
| New relationship selector | Record with no related data |
| Layout or styling change | Narrow viewport, long text, and an empty table |
| New dialog or drawer | Open, close, reopen — confirm reset/repopulate behavior |
| New export/download | Run it and confirm the file is non-empty and scoped |

## Create/read/update/delete loop

1. **Create** — fill every required field; add one optional value so the round trip is visible; use a unique marker such as `<feature>_<run-id>`.
2. **Verify create** — dialog or drawer closes, no error toast, the row appears at the expected position with the expected values.
3. **Read** — filter by the marker; confirm only matching rows remain and the total count agrees; reset and confirm the full list returns.
4. **Update** — open the record and read back every field before editing: stored values, defaults, and blank fields must be distinguishable. Change one field, save, confirm the list and a reload both show the new value.
5. **Delete** — trigger delete, confirm the secondary confirmation appears, confirm removal, then refresh to prove it is not a client-only removal.

If any step changes behavior outside the change under test (for example the list no longer sorts), record it as an observation rather than editing unrelated code.

## Form validation cases

- Required field left empty.
- Wrong format or length (digits in a name field, over-long text).
- Duplicate against a uniqueness rule, if the schema declares one.
- Whitespace-only value.
- Boundary number: zero, negative, and the declared maximum.
- Optional field cleared on edit, when the backend allows nulling.

## Table and state checks

- Empty result and empty initial load render a readable state.
- Loading state appears and resolves; no infinite spinner.
- Error state offers a way forward rather than a blank panel.
- Long values truncate or wrap without breaking row height.
- Action buttons match the role and the row state (disabled vs hidden).
- Pagination totals agree with filtered results.

## Evidence quality

- A screenshot proves appearance at one moment; a second screenshot after reload proves persistence.
- A network entry proves a request was made; the response body proves what it returned.
- A console entry proves an error exists; the stack trace and code path prove where.
- "No errors" is evidence only when the console and the network panel were actually read for the page under test.

## Reporting failures

State four things per failure: the step, the observable symptom, the request or console line that explains it, and the fix — or the reason a fix is out of scope. A failure report without the underlying request or console evidence is a guess.
