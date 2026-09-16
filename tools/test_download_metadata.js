const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const script = fs.readFileSync(path.join(__dirname, '../site/assets/js/download-metadata.js'), 'utf8');

function card(platform) {
  const fields = Object.fromEntries(['version', 'fileName', 'fileSize', 'sha256', 'nativeGitCommit']
    .map(name => [name, { textContent: 'fallback ' + name }]));
  const links = { downloadUrl: { href: 'existing-download' }, releaseUrl: { href: 'existing-release' } };
  const pending = { hidden: false };
  const available = { hidden: true };
  return {
    fields, links, pending, available,
    attributes: { 'data-sdk-platform': platform, 'data-manifest-url': platform || 'installer' },
    getAttribute(name) { return this.attributes[name]; },
    setAttribute(name, value) { this.attributes[name] = value; },
    querySelectorAll(selector) {
      if (selector === '[data-release-pending]') return [pending];
      if (selector === '[data-release-available]') return [available];
      const match = selector.match(/^\[data-(field|href)="([^"]+)"\]$/);
      return match ? [(match[1] === 'field' ? fields : links)[match[2]]] : [];
    }
  };
}

function metadata(platform) {
  const tag = 'nexatomtt-sdk-v0.1.0-preview.7';
  const file = tag + '-' + platform + (platform === 'windows-x64' ? '.zip' : '.tar.gz');
  const base = 'https://github.com/nexatom-research/nexatom-downloads/releases/';
  return {
    schemaVersion: 1, artifactName: 'nexatomtt-sdk', sdkVersion: '0.1.0-preview.7',
    channel: 'preview', distribution: 'public-preview', nativeApiVersion: '1', platform,
    nativeGitCommit: 'a'.repeat(40), sha256: 'b'.repeat(64), sizeBytes: 1234,
    fileName: file, releaseTag: tag, releaseUrl: base + 'tag/' + tag,
    downloadUrl: base + 'download/' + tag + '/' + file,
  };
}

async function refresh(cards, responses) {
  vm.runInNewContext(script, {
    document: { querySelectorAll: () => cards },
    fetch: async url => {
      const data = responses[url];
      return { ok: data !== undefined, json: async () => data };
    },
  });
  await new Promise(setImmediate);
}

test('Windows and Linux refresh independently with their own archive links', async () => {
  const windows = card('windows-x64');
  const linux = card('linux-x64');
  const winData = metadata('windows-x64');
  const linuxData = metadata('linux-x64');
  // SDK cards must not accidentally apply fields from the installer contract.
  winData.installerUrl = 'https://example.invalid/installer.exe';
  winData.version = 'wrong installer version';
  await refresh([windows, linux], { 'windows-x64': winData, 'linux-x64': linuxData });
  assert.equal(windows.links.downloadUrl.href, winData.downloadUrl);
  assert.equal(linux.links.downloadUrl.href, linuxData.downloadUrl);
  assert.equal(windows.fields.version.textContent, winData.sdkVersion);
  assert.equal(linux.fields.sha256.textContent, linuxData.sha256);
  assert.equal(linux.pending.hidden, true);
  assert.equal(linux.available.hidden, false);
});

test('unpublished Linux metadata leaves Windows working and Linux unavailable', async () => {
  const windows = card('windows-x64');
  const linux = card('linux-x64');
  await refresh([windows, linux], { 'windows-x64': metadata('windows-x64') });
  assert.equal(windows.attributes['data-metadata-status'], 'live');
  assert.equal(linux.attributes['data-metadata-status'], 'fallback');
  assert.equal(linux.pending.hidden, false);
  assert.equal(linux.available.hidden, true);
  assert.equal(linux.links.downloadUrl.href, 'existing-download');
});

test('wrong-platform, partial and mismatched metadata cannot enable a download', async () => {
  for (const change of [
    { platform: 'windows-x64' }, { sha256: null }, { sizeBytes: 0 },
    { nativeGitCommit: '' }, { downloadUrl: 'https://example.invalid/wrong.tar.gz' },
    { fileName: 'unpublished-placeholder.tar.gz' },
  ]) {
    const linux = card('linux-x64');
    await refresh([linux], { 'linux-x64': { ...metadata('linux-x64'), ...change } });
    assert.equal(linux.available.hidden, true);
    assert.equal(linux.fields.version.textContent, 'fallback version');
    assert.equal(linux.links.downloadUrl.href, 'existing-download');
  }
});

test('existing app installer metadata and offline fallback remain supported', async () => {
  const installer = card(null);
  await refresh([installer], { installer: { version: '1.0.4', sizeBytes: 100, installerUrl: 'existing-installer.exe' } });
  assert.equal(installer.fields.version.textContent, '1.0.4');
  assert.equal(installer.links.downloadUrl.href, 'existing-installer.exe');
  const offline = card('windows-x64');
  await refresh([offline], {});
  assert.equal(offline.fields.version.textContent, 'fallback version');
  assert.equal(offline.links.downloadUrl.href, 'existing-download');
});
