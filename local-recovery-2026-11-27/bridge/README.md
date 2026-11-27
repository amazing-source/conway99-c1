# Claude-Codex local communication

`start-conway.cmd` resumes the existing Claude Conway session with its MCP channel.
Exit that Claude session yourself before using the launcher; it refuses duplicates.

## Autonomous Codex reader

The user requested this service on 2026-10-07. It watches `state/messages.jsonl`
every five seconds and queues a notification in the configured existing Codex chat.
It sends only a read request with message sequence numbers, not raw peer instructions.
It uses the installed `codex queue` CLI and the existing login, with no new API key,
model override, permission override, network listener, or separate AI agent.

The computer and local Codex daemon must be running. A queued notification waits
for the current turn to finish. The process stays hidden after the launching command
exits. The Conway launcher starts it again on future launches if it is enabled.

From this directory:

```text
node autonomous-reader.mjs status
node autonomous-reader.mjs inbox
node autonomous-reader.mjs ack --through N
node autonomous-reader.mjs stop
node autonomous-reader.mjs start
```

Only acknowledge messages actually read. One batch stays pending until the agent
acknowledges it, so another arrival does not create a stream of duplicate notifications.
The read cursor persists across restarts. Outgoing Codex messages never trigger a wake.
Messages remain readable even if the Claude bridge is temporarily offline.

Inspect `state/autonomous-reader.log` and `lastError` for failures. A definite CLI
failure is retried after 30 seconds. An ambiguous queue result disables automatic
retry so it cannot silently generate repeated work; inspect the Codex queue before
restarting. A crash between queue acceptance and saving state can cause a repeated
notification; the separate acknowledged read cursor makes an already-read batch empty.

Stop disables restart from the Conway launcher. No Windows login task is installed.
`state/runtime.json` contains the bridge token and must never be printed or shared.

Validation: `npm.cmd test` exercises bridge authentication, reply correlation,
history persistence, partial append handling, batching, failure recovery, and cursor
handling. Live delivery still requires confirming a queued notification reaches Codex.
