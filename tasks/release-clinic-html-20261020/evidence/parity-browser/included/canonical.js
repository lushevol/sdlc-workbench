// ── Remediation annotation system ──
var _remName = localStorage.getItem('tda_rem_name') || '';
var _REM_TYPE_LABELS = {resolved:'Resolved', unresolved:'Unresolved', false_positive:'False Positive', workaround:'Workaround'};

function remSetName() {
  var n = prompt('Enter your name (will appear on all annotations in this session):', _remName);
  if (n !== null) { _remName = n.trim(); localStorage.setItem('tda_rem_name', _remName); }
  _updateToolbar();
}

function _updateToolbar() {
  var info = document.getElementById('remToolbarInfo');
  var totalMandatory = document.querySelectorAll('[data-rem-mandatory="true"]').length;
  var missingMandatory = _getMandatoryUnannotated().length;
  var mandatoryHtml = '';
  if (totalMandatory > 0) {
    mandatoryHtml = missingMandatory > 0
      ? ' &mdash; <strong style="color:#ffd9d9;">' + (totalMandatory - missingMandatory) + '/' + totalMandatory + ' mandatory CRITICAL/MODERATE annotations complete (' + missingMandatory + ' remaining)</strong>'
      : ' &mdash; <strong>' + totalMandatory + '/' + totalMandatory + ' mandatory CRITICAL/MODERATE annotations complete &#9989;</strong>';
  }
  if (_remName) {
    var count = document.querySelectorAll('.rem-recorded').length;
    info.innerHTML = '&#128221; Reviewer: <strong>' + _escHtml(_remName) + '</strong> &mdash; ' + count + ' annotation(s) recorded.' + mandatoryHtml;
  } else {
    info.innerHTML = '&#128221; Remediation mode &mdash; set your name before annotating.' + mandatoryHtml;
  }
  var exportBtn = document.querySelector('.rem-export-btn');
  if (exportBtn) exportBtn.classList.toggle('locked', missingMandatory > 0);
}

function _getMandatoryUnannotated() {
  var missing = [];
  document.querySelectorAll('[data-rem-mandatory="true"]').forEach(function(f) {
    if (!f.querySelector('.rem-recorded')) missing.push(f);
  });
  return missing;
}

function _escHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function _formatTs(d) {
  var pad = function(n){return n<10?'0'+n:n;};
  return d.getFullYear()+'-'+pad(d.getMonth()+1)+'-'+pad(d.getDate())+' '+pad(d.getHours())+':'+pad(d.getMinutes());
}

document.addEventListener('DOMContentLoaded', function() {
  var findings = document.querySelectorAll('.finding');
  findings.forEach(function(f, idx) {
    if (f.querySelector('.rem-btn')) return; // already injected (e.g. re-opened annotated export)
    if (f.closest('.looksGood')) return; // no remediation needed for passing checks
    var isCritOrMod = !!(f.closest('.section.critical') || f.closest('.section.moderate'));
    var isSentinel = /^none identified/i.test(f.textContent.trim());
    var isMandatory = isCritOrMod && !isSentinel;
    if (isMandatory) f.setAttribute('data-rem-mandatory', 'true');
    var id = 'rem-' + idx;
    var btn = document.createElement('button');
    btn.className = 'rem-btn';
    btn.textContent = (isMandatory ? '\uD83D\uDD12 ' : '') + '\uD83D\uDCDD Remediate';
    if (isMandatory) btn.title = 'Mandatory: this CRITICAL/MODERATE finding must be annotated before the report can be saved.';
    btn.onclick = function() { remOpen(id, btn); };
    var panel = document.createElement('div');
    panel.className = 'rem-panel';
    panel.id = id;
    panel.innerHTML =
      '<label>Reviewer name</label>' +
      '<input type="text" id="'+id+'-name" placeholder="Your name" />' +
      '<label>Type of Remediation</label>' +
      '<select id="'+id+'-type">' +
      '<option value="">-- Select --</option>' +
      '<option value="resolved">Resolved</option>' +
      '<option value="unresolved">Unresolved</option>' +
      '<option value="false_positive">False Positive</option>' +
      '<option value="workaround">Workaround</option>' +
      '</select>' +
      '<label>Remediation / response note</label>' +
      '<textarea id="'+id+'-note" placeholder="Describe the remediation applied or the reason this finding does not apply..."></textarea>' +
      '<div class="rem-actions">' +
      '<button class="rem-save" onclick="remSave(\'' + id + '\')">' +
      'Save Annotation</button>' +
      '<button class="rem-cancel" onclick="remClose(\'' + id + '\')">' +
      'Cancel</button></div>';
    f.appendChild(btn);
    f.appendChild(panel);
  });
  _updateToolbar();
});

function remOpen(id) {
  var panel = document.getElementById(id);
  if (!panel) return;
  var isOpen = panel.classList.contains('open');
  document.querySelectorAll('.rem-panel.open').forEach(function(p){ p.classList.remove('open'); });
  if (!isOpen) {
    panel.classList.add('open');
    var nameField = document.getElementById(id + '-name');
    if (nameField && !nameField.value && _remName) nameField.value = _remName;
    panel.querySelector('textarea').focus();
  }
}

function remClose(id) {
  var panel = document.getElementById(id);
  if (panel) panel.classList.remove('open');
}

function remSave(id) {
  var nameField = document.getElementById(id + '-name');
  var typeField = document.getElementById(id + '-type');
  var noteField = document.getElementById(id + '-note');
  var name = (nameField ? nameField.value.trim() : '') || _remName || 'Unknown';
  var remType = typeField ? typeField.value : '';
  var note = noteField ? noteField.value.trim() : '';
  if (!remType) { alert('Please select a Type of Remediation before saving.'); return; }
  if (!note) { alert('Please enter a remediation note before saving.'); return; }
  if (name) { _remName = name; localStorage.setItem('tda_rem_name', name); }
  var ts = _formatTs(new Date());
  var typeLabel = _REM_TYPE_LABELS[remType] || remType;
  var recorded = document.createElement('div');
  recorded.className = 'rem-recorded';
  recorded.innerHTML =
    '<div class="rem-meta" data-resolution="' + remType + '" data-reviewer="' + _escHtml(name) + '" data-timestamp="' + ts + '">' +
    '<span class="rem-status-badge rem-status-' + remType + '">' + typeLabel + '</span>' +
    ' &nbsp;&middot;&nbsp; Reviewer: <strong>' + _escHtml(name) + '</strong>' +
    ' &nbsp;&middot;&nbsp; ' + ts + '</div>' +
    '<div class="rem-note"><strong>Remediation note:</strong> ' + _escHtml(note).replace(/\n/g, '<br>') + '</div>';
  var panel = document.getElementById(id);
  var f = panel.closest('.finding');
  panel.classList.remove('open');
  panel.parentNode.insertBefore(recorded, panel.nextSibling);
  if (f) f.classList.remove('rem-missing');
  if (noteField) noteField.value = '';
  if (typeField) typeField.value = '';
  _updateToolbar();
}

function remExport() {
  var missing = _getMandatoryUnannotated();
  if (missing.length > 0) {
    missing.forEach(function(f){ f.classList.add('rem-missing'); });
    missing[0].scrollIntoView({behavior: 'smooth', block: 'center'});
    alert('Cannot save: ' + missing.length + ' CRITICAL/MODERATE finding(s) still need an annotation.\n\nEvery CRITICAL/MODERATE observation must be annotated (Resolved / Unresolved / False Positive / Workaround, with a note) before the report can be exported. The affected finding(s) are now highlighted in red below \u2014 click "Remediate" on each one, save an annotation, then try Save Annotated Report again.');
    return;
  }
  document.querySelectorAll('.rem-panel.open').forEach(function(p){ p.classList.remove('open'); });
  var html = '<!DOCTYPE html>\n' + document.documentElement.outerHTML;
  var blob = new Blob([html], {type: 'text/html;charset=utf-8'});
  var a = document.createElement('a');
  var title = document.title.replace(/[^a-zA-Z0-9_\-. ]/g, '_').replace(/ /g, '_');
  a.href = URL.createObjectURL(blob);
  a.download = 'Annotated_' + title + '.html';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(a.href);
}
