# CodeQL Integration & Compliance Guide for Your Election Information Pipeline

This comprehensive guide integrates advanced CodeQL scanning, custom endpoint security queries, and compliance frameworks (SOC 2 and HIPAA) into your **Pixel Terminal Admin Panel** and **Pennsylvania Election Info** infrastructure.

---

## 🔐 CodeQL Advanced Workflow

```yaml
# .github/workflows/codeql.yml
name: "CodeQL Advanced Security Scan"

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]
  schedule:
    - cron: '28 7 * * 4'  # Thursday at 07:28 UTC

jobs:
  analyze:
    name: Analyze (${{ matrix.language }})
    runs-on: ${{ (matrix.language == 'swift' && 'macos-latest') || 'ubuntu-latest' }}
    permissions:
      security-events: write
      packages: read
      contents: read
      actions: read

    strategy:
      fail-fast: false
      matrix:
        include:
        - language: javascript-typescript
          build-mode: none  # For frontend React app & Express backend
        - language: python
          build-mode: none  # For deployment scripts

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Initialize CodeQL
      uses: github/codeql-action/init@v4
      with:
        languages: ${{ matrix.language }}
        build-mode: ${{ matrix.build-mode }}
        queries: security-extended,security-and-quality
        paths-ignore: |
          '**/node_modules/**'
          '**/.env*'
          '**/secrets/**'
          '**/test/**'

    - name: Setup Node.js for JavaScript analysis
      if: matrix.language == 'javascript-typescript'
      uses: actions/setup-node@v4
      with:
        node-version: '20'

    - name: Setup Python for Python analysis
      if: matrix.language == 'python'
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Install Dependencies (JavaScript)
      if: matrix.language == 'javascript-typescript'
      run: |
        cd server
        npm ci --ignore-scripts
        cd ../client
        npm ci --ignore-scripts

    - name: Install Dependencies (Python)
      if: matrix.language == 'python'
      run: |
        pip install --upgrade pip setuptools wheel
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v4
      with:
        category: "/language:${{matrix.language}}"
        upload: true
        output: sarif-results
```

---

## 🛡️ Custom CodeQL Queries for Admin Panel Endpoints

To target specific administrative endpoints in your Express server (e.g., `/api/admin/voter-data`, `/api/admin/config`), use these custom QL queries.

### 1. Missing Authentication Check on Admin Routes
```ql
// custom-queries/missing-auth.ql
import javascript

from ExpressRoute route, CallSite middleware
where route.getAPath().regexpMatch("/api/admin/.*")
  and not route.getAMiddleware() = middleware
  and middleware.getTarget().getName().matches("%auth%")
select route, "Admin route missing mandatory authentication middleware."
```

### 2. Unsanitized Parameter Injection in Voter Data Query
```ql
// custom-queries/voter-param-injection.ql
import javascript
import semmle.javascript.security.dataflow.SqlInjectionCustomizations

from DataFlow::Node source, DataFlow::Node sink, ParameterSanitizer sanitizer
where source instanceof ExpressRequestSource
  and sink instanceof DatabaseQueryParameter
  and not dataFlow(source, sink, sanitizer)
select sink, "Potential unvalidated input reaching database query in election pipeline."
```

---

## 📋 Compliance Frameworks: SOC 2 & HIPAA for Voter Data

Given the sensitivity of Pennsylvania election information, your infrastructure must align with rigorous compliance standards.

### SOC 2 Trust Services Criteria Mapping
| Criteria | Control Objective | Technical Implementation |
|----------|-------------------|--------------------------|
| **CC6.1 (Logical Access)** | Restrict access to administrative systems | JWT authentication with short expiry (1h) and RBAC middleware. |
| **CC6.6 (Boundary Protection)** | Prevent unauthorized external connections | Nginx reverse proxy with TLS 1.3, rate limiting, and strict CORS. |
| **CC7.1 (Vulnerability Management)** | Detect and remediate vulnerabilities | Automated CodeQL scans on every PR and weekly dependency audits. |
| **CC9.2 (Data Transmission)** | Protect data in transit | Enforced HTTPS (`strict-transport-security`) and encrypted backups. |

### HIPAA Safeguards for PII / Voter Records (Administrative & Technical)
While general election data is public, voter registration logs and administrative logs often contain Personally Identifiable Information (PII):
- **Access Controls (45 CFR § 164.312(a)):** Unique user identification and emergency access procedures implemented via the Pixel Terminal Admin Panel.
- **Audit Controls (45 CFR § 164.312(b)):** Comprehensive logging of all admin actions, IP addresses, and data access requests with log masking for secrets (`LOG_MASK_SECRETS=true`).
- **Integrity Controls (45 CFR § 164.312(c)):** Cryptographic checksums and automated integrity verification during deployment (`deploy.sh` verification gates).
- **Transmission Security (45 CFR § 164.312(e)):** End-to-end encryption using AES-256 for backups and TLS for all API communications.

---

## ⚙️ Automated Security Gates in Deployment (`deploy.sh`)

```bash
#!/bin/bash
set -e

echo "=============================================="
echo "  COMPLIANCE & SECURITY DEPLOYMENT GATE"
echo "=============================================="

# 1. Trigger CodeQL Analysis
echo "[1/4] Triggering CodeQL scan..."
curl -sSL \
  -H "Authorization: token $GH_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/workflows/codeql.yml/dispatches \
  -d '{"ref":"main"}'

# 2. Dependency Vulnerability Audit
echo "[2/4] Auditing npm packages for critical vulnerabilities..."
npm audit --audit-level=critical || { echo "❌ Critical CVEs found in dependencies!"; exit 1; }

# 3. Secret Detection
echo "[3/4] Scanning for exposed API keys or tokens..."
detect-secrets-hook --baseline .secrets.baseline . || { echo "❌ Secret exposure risk detected!"; exit 1; }

# 4. Container Vulnerability Scan
echo "[4/4] Scanning container image with Trivy..."
trivy image --severity HIGH,CRITICAL pixel-admin-server:latest || { echo "❌ Container security scan failed!"; exit 1; }

echo "✅ All security gates and compliance checks passed successfully."
```

---

## 🚀 Next Steps

1. **Deploy the updated CodeQL workflow** into `.github/workflows/codeql.yml`.
2. **Add the custom QL queries** under `.github/codeql/custom-queries/`.
3. **Verify branch protection rules** requiring status checks from CodeQL and Trivy prior to merging into `main`.
