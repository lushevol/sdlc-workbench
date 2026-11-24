const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

class CaseReporter {
  onTestCaseResult(test, result) {
    const directory = process.env.RUN_EVIDENCE_DIR;
    const identity = crypto.createHash("sha256").update(test.path + "\n" + result.fullName).digest("hex").slice(0, 12);
    fs.mkdirSync(path.join(directory, "cases"), { recursive: true });
    fs.writeFileSync(path.join(directory, "cases", `${identity}.json`), JSON.stringify({
      saved_at: new Date().toISOString(),
      test_file: test.path,
      binding: "../source-binding.json",
      ...result,
    }, null, 2) + "\n");
  }
}

module.exports = CaseReporter;
