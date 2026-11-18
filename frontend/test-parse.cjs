const fs = require('fs');
const { parseAst } = require('/app/node_modules/rollup/dist/parseAst.js');

const code = fs.readFileSync('/app/node_modules/react-dom/client.js', 'utf8');

console.log('Testing full file:');
try {
  parseAst(code);
  console.log('Full file: SUCCESS');
} catch (e) {
  console.log('Full file FAIL:', e.message, 'at pos:', e.pos);
}

const lines = code.split('\n');
console.log('\nTesting individual constructs:');
const testSnippets = [
  "var m = require('react-dom');",
  "if (process.env.NODE_ENV === 'production') { exports.createRoot = m.createRoot; }",
  "if (process.env.NODE_ENV === 'production') { exports.createRoot = m.createRoot; } else { var i = 1; }",
  "var i = m.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED;",
  "exports.createRoot = function(c, o) { i.usingClientEntryPoint = true; try { return m.createRoot(c, o); } finally { i.usingClientEntryPoint = false; } };",
  "function(c, o) { i.usingClientEntryPoint = true; try { return m.createRoot(c, o); } finally { i.usingClientEntryPoint = false; } }",
  code
];

testSnippets.forEach((snippet, idx) => {
  try {
    parseAst(snippet);
    console.log(`Snippet #${idx}: SUCCESS`);
  } catch (e) {
    console.log(`Snippet #${idx}: FAIL -> ${e.message}`);
  }
});
