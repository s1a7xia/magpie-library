# Structured memory mirror

This directory mirrors the user's three current active global preferences from
Magpie structured memory. It is a readable configuration mirror, not a live
memory database and not a replacement for the encrypted Magpie backup.

Included:

- `m_c0e6bf94134e.md`: RuoYi-Vue-Plus reuse-first and coding-style consistency.
- `m_e0827147ced5.md`: simplest sufficient relational data model.
- `m_e6a950c6126c.md`: first ship a runnable closed loop; use project state and Git as facts for large projects.

Not included:

- removed or inactive memory entries;
- use counters and local write state from `meta.json`;
- credentials, login state, synchronization configuration, conversation history, or private project data.

Restore these entries through the Magpie memory mechanism or copy the Markdown
files into the local structured-memory directory after checking paths and
formats for the installed Magpie version. Do not treat this mirror as a
guarantee that the target Magpie store has already been rebuilt.
