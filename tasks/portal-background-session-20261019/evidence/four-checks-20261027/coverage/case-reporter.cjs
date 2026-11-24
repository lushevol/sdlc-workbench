const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

class CaseReporter {
  constructor() { this.count = 0; this.counts = {}; }
  onTestCaseResult(test, result) {
    const directory = process.env.RUN_EVIDENCE_DIR;
    const identity = crypto.createHash('sha256').update(test.path + '\n' + result.fullName + '\n' + this.count).digest('hex').slice(0, 12);
    const caseFile = path.join('cases', identity + '.json');
    fs.mkdirSync(path.join(directory, 'cases'), { recursive: true });
    fs.writeFileSync(path.join(directory, caseFile), JSON.stringify({
      saved_at: new Date().toISOString(), test_file: test.path,
      binding: '../source-binding.json', ...result,
    }, null, 2) + '\n');
    this.count += 1;
    this.counts[result.status] = (this.counts[result.status] || 0) + 1;
    fs.writeFileSync(path.join(directory, 'case-progress.json'), JSON.stringify({
      status: 'RUNNING', updated_at: new Date().toISOString(), completed_cases: this.count,
      counts: this.counts, last_case: caseFile, source_binding: 'source-binding.json',
    }, null, 2) + '\n');
  }
}
module.exports = CaseReporter;
