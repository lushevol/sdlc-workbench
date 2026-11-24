const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

class CaseReporter {
  constructor() { this.completed = 0; }
  onTestCaseResult(test, result) {
    const directory = process.env.RUN_EVIDENCE_DIR;
    const identity = crypto.createHash("sha256").update(test.path + result.fullName).digest("hex").slice(0, 12);
    const sequence = String(++this.completed).padStart(3, "0");
    fs.mkdirSync(path.join(directory, "cases"), { recursive: true });
    fs.writeFileSync(path.join(directory, "cases", `${sequence}-${identity}.json`), JSON.stringify({
      saved_at: new Date().toISOString(), test_file: test.path, binding: "../source-binding.json", ...result,
    }, null, 2) + "\n");
  }
}

module.exports = CaseReporter;
