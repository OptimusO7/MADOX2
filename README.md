
# MADOX V2 — Educational Penetration Testing Tool

> ⚠️ **Disclaimer — Read Carefully**  
> MADOX V2 is provided **strictly for educational, research, and controlled penetration-testing training**.  
> Do **NOT** use this tool on systems you do not own or do not have explicit written permission to test.  
> The author and contributors accept **no responsibility** for misuse. Misuse may be illegal and unethical.

---

## 🚀 Overview

**MADOX V2** is a penetration-testing simulation tool built for security awareness training, classroom demonstrations, and red-team exercises.  
It demonstrates key concepts used in social engineering / credential-harvesting scenarios in a **safe, local, controlled** environment:

- Website cloning techniques (demonstration only — do not use for fraud)  
- Hosting cloned pages via a local HTTP server for analysis and training  
- Simulated credential-capture workflow to teach detection & mitigation

> Purpose: **education and defensive awareness** — help defenders and trainees recognize attack patterns and improve security posture.

---

## ⚡ Features

- Create simple demonstration clones of static pages for training
- Serve cloned content locally with a minimal HTTP server
- Simulate credential submission without sending data to third parties (local capture for analysis)
- Lightweight: few dependencies (primarily `wget` for content retrieval)

---

## 🧰 Requirements

- **Windows:** `setup.exe` (bundles/installs required utilities like `wget`) — run setup before first use  
- **Linux:** `wget` (and shell permissions to execute the provided binary/script)

> Minimal system requirements; designed to run on typical modern development machines.

---

## 🖥️ Installation & Quick Start

### Windows (first-time)
1. Run the bundled installer:  
   ```powershell
   setup.exe
   ```
   - This installs required utilities (e.g., `wget`) and prepares files.
2. Launch the program:  
   ```powershell
   madox.exe
   ```

### Linux
1. Ensure `wget` is installed:
   ```bash
   sudo apt update && sudo apt install wget -y
   ```
2. Make the binary/script executable (if needed) and run it:
   ```bash
   chmod +x madoxV2_linux
   ./madoxV2_linux
   ```

---

## 📦 Typical Workflow

1. **Prepare a controlled target environment** — a local VM, staging web server, or isolated network used only for training.  
2. **Clone a simple public page** for demonstration (local copy only) — the tool uses `wget` to fetch static assets for offline training.  
3. **Start the local HTTP server** via the tool — trainees will access the hosted page on `http://localhost:PORT`.  
4. **Simulate credential submission** — captured data is kept locally for analysis and demonstration.  
5. **Discuss detection & defenses** with your audience: indicators, logs, network artifacts, browser warnings, and mitigation strategies.

---

## 🔒 Safety & Ethical Guidelines

- Only run MADOX V2 in isolated test environments or with **explicit written authorization** from the system owner.  
- Do not capture, store, or transmit real credentials from users who have not consented. Use **test accounts** only.  
- Do not deploy cloned or simulated pages on public internet-facing systems. Use local/private networks or virtual lab environments.  
- After training, remove any cloned pages/resources and securely delete captured test data.

---

## ✅ Recommended Training Scenarios

- **Blue Team Exercise:** Host a cloned page locally. Let defenders inspect network traffic and server logs to find indicators of credential capture.  
- **User Awareness Class:** Show how a cloned page may look convincing and teach students how to verify URLs, check TLS, and use MFA.  
- **Red vs Blue Drill:** Run a controlled simulation where red team demonstrates techniques and blue team responds with detection & containment.

---

## 🧩 File Structure (example)
```
madox-v2/
├── README.md
├── setup.exe                # Windows installer (placeholder)
├── madox.exe                # Windows runtime (placeholder)
├── madoxV2_linux            # Linux binary/script (placeholder)
├── templates/               # Example static page templates for training
├── captured/                # Local folder where simulated captures are stored
└── docs/                    # Additional docs & usage notes
```

---

## 🛠️ Troubleshooting

- **`wget` not found (Linux):**  
  Install with `sudo apt install wget -y`.
- **Permission denied executing binary:**  
  Run `chmod +x madoxV2_linux` then execute.
- **Server port in use:**  
  Ensure no other service uses the configured port; change the port or stop the other service.

---

## 📜 License & Legal

This project is provided **for educational purposes only**. Unauthorized use against live systems, networks, or people is illegal and unethical.

**By using this tool you agree to only run it in environments where you have explicit permission.**  
If you want to include a license file, consider one that reflects your intent (for example, a custom "educational use only" policy). This repository does **not** grant rights to perform illegal or malicious activities.

---

## 🤝 Contributing

Contributions that enhance the educational value of this tool are welcome (examples: improved templates, defensive detection guides, sanitized example logs).  
When contributing, please:

- Keep examples **safe and non-malicious**  
- Include clear instructions and testing notes  
- Never add features that facilitate unauthorized real-world attacks

---

## 📫 Contact & Reporting

If you find a bug, unsafe behavior, or have suggestions for improving training value, open an issue or contact the author:  
`your.email@gmail.com` — replace with actual contact in repo.

---

## 🧾 Changelog (placeholder)
- **v2.0** — Core simulation features, cross-platform binaries, updated training templates.  
- (Add subsequent updates here.)

---

Thank you for using MADOX V2 to strengthen security awareness and defensive capabilities. Use it responsibly — teach, learn, and defend.
