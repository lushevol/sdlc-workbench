const fs = require('fs');
const path = require('path');
const replacements = require('./replacements.json');

function transform(source, resourcePath) {
  const relativePath = path.relative(path.resolve(__dirname, '../local-mfe/source'), resourcePath).split(path.sep).join('/');
  const edits = replacements[relativePath] || [];
  let output = source;
  for (const edit of edits) {
    const count = output.split(edit.before).length - 1;
    if (count !== 1) throw new Error('Instrumentation anchor mismatch: ' + relativePath + ' / ' + edit.id + ' / ' + count);
    output = output.replace(edit.before, edit.after);
  }
  return output;
}
module.exports = function (source) { return transform(source, this.resourcePath); };
module.exports.transform = transform;
