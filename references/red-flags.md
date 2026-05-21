# Skill Vetting — Red Flag Patterns Reference

## Critical Reject Patterns (Immediate Block)

### Data Exfiltration
```
🚨 PATTERN: curl/wget/requests to unknown domains
🚨 PATTERN: Sending JSON/file contents to external APIs
🚨 PATTERN: base64 encoding of payload data
🚨 PATTERN: Reading credential files and transmitting elsewhere
🚨 PATTERN: Accessing ~/.ssh, ~/.aws, ~/.git-credentials, ~/.netrc
```

### Code Execution Risks
```
🚨 PATTERN: eval(), exec(), new Function() with string input
🚨 PATTERN: Dynamic import of externally-sourced code
🚨 PATTERN: subprocess with shell=True and external variables
🚨 PATTERN: Opening and executing received payloads
```

### System Modification
```
🚨 PATTERN: Writing to system paths outside workspace
🚨 PATTERN: Modifying /etc/, /usr/bin/, Windows System32
🚨 PATTERN: Registry modifications on Windows
🚨 PATTERN: Installing packages/dependencies without declared deps
```

### Obfuscation / Suspicious Encoding
```
🚨 PATTERN: Base64-encoded strings decoded and executed
🚨 PATTERN: Variable names like $a, $b, $x1 (minified JS)
🚨 PATTERN: String concatenation to build commands/URLs
🚨 PATTERN: Remote code fetch and immediate exec
```

### Credential / Identity Theft
```
🚨 PATTERN: Requesting existing API keys or tokens
🚨 PATTERN: Creating credential files with specific naming patterns
🚨 PATTERN: Accessing browser cookies, localStorage session data
🚨 PATTERN: Keylogger patterns (keyboard event listeners)
```

## Medium Risk Patterns (Review Carefully)

### Over-broad Permissions
```
🟡 PATTERN: Requests read access to entire home directory
🟡 PATTERN: Requests write access to multiple unrelated directories
🟡 PATTERN: Declares no file scope (should be explicit)
```

### External Network Access
```
🟡 PATTERN: Network calls to analytics or telemetry services
🟡 PATTERN: Phoning home to a domain unrelated to the skill's purpose
🟡 PATTERN: User agent or client ID tracking
```

### Dependency Issues
```
🟡 PATTERN: pip install / npm install without pinned dependencies
🟡 PATTERN: Installing from GitHub refs (not release tags)
🟡 PATTERN: Auto-installing missing packages
```

### Suspicious File Operations
```
🟡 PATTERN: glob/rglob over broad directory scopes
🟡 PATTERN: Reading multiple config files in sequence
🟡 PATTERN: Writing to paths outside the skill's own directory
```

## File Type Risk Assessment

| File Type | Risk Level | Review Focus |
|-----------|-----------|--------------|
| SKILL.md | 🟡 MEDIUM | Tool declarations, env vars, permissions |
| scripts/*.py | 🟡-🔴 MEDIUM-HIGH | Network calls, file I/O, system calls |
| scripts/*.sh | 🟡-🔴 MEDIUM-HIGH | Shell commands, downloads, env vars |
| scripts/*.js | 🟡-🔴 MEDIUM-HIGH | eval(), dynamic code, network |
| references/*.md | 🟢 LOW | Usually documentation only |
| templates/* | 🟢 LOW | Usually safe, review if dynamic |
| hooks/** | 🔴 HIGH | Execution on events, check what triggers |
| assets/* | 🟡 MEDIUM | Review if binary/executable |
| _meta.json | 🟢 LOW | Metadata only |
| .clawhub/* | 🟢 LOW | Hub metadata |

## Environment Variables to Watch

**Safe (declared purpose):**
- `TAVILY_API_KEY` — explicit web search purpose
- `GITHUB_TOKEN` — declared GitHub API usage
- `OPENAI_API_KEY` — declared LLM usage

**Suspicious:**
- Any credential variable without clear declared purpose
- Generic names like `API_KEY`, `SECRET`, `TOKEN` without explanation
- Reading existing env vars and retransmitting

## Safe Patterns (Green Flags)

```
✅ Explicit, minimal file scope declaration
✅ All dependencies listed in header or docs
✅ Network endpoints are well-known trusted services
✅ Uses only stdlib Python (no pip install needed)
✅ No eval/exec/dynamic code
✅ File operations scoped to skill directory or workspace
✅ Open source with readable source code
✅ Known author with track record
✅ Recent update (within 6 months)
```

## Severity Decision Tree

```
Start: New skill detected
│
├─ Is it from a known-trusted source (in-repo, known author)?
│   └─ YES → 🟢 LOW risk, basic review sufficient
│
├─ Does it request credentials or key storage access?
│   └─ YES → 🔴 HIGH risk, human approval mandatory
│
├─ Does it have ANY critical reject pattern?
│   └─ YES → ⛔ EXTREME risk, DO NOT INSTALL
│
├─ Does it make network calls?
│   └─ YES → Check endpoints. Untrusted? → 🔴 HIGH
│           → Trusted service with declared purpose? → 🟡 MEDIUM
│
├─ Does it modify system files?
│   └─ YES → 🔴 HIGH risk, human approval mandatory
│
├─ Is the code obfuscated or encoded?
│   └─ YES → 🔴 HIGH risk, require human approval
│
└─ Default: 🟡 MEDIUM risk, full review required
```
