(function () {
  function formatBytes(bytes) {
    if (!Number.isFinite(bytes)) return '';
    return bytes.toLocaleString('en-US') + ' bytes / ' + (bytes / 1000000).toFixed(2) + ' MB';
  }

  function releaseUrlFromDownload(url) {
    var match = String(url || '').match(/\/releases\/download\/([^/]+)\//);
    return match ? 'https://github.com/nexatom-research/nexatom-downloads/releases/tag/' + match[1] : '';
  }

  function setText(root, field, value) {
    if (value === undefined || value === null || value === '') return;
    root.querySelectorAll('[data-field="' + field + '"]').forEach(function (node) {
      node.textContent = value;
    });
  }

  function setHref(root, field, value) {
    if (!value) return;
    root.querySelectorAll('[data-href="' + field + '"]').forEach(function (node) {
      node.href = value;
    });
  }

  function applyMetadata(root, data) {
    var version = data.version || data.sdkVersion;
    var downloadUrl = data.installerUrl || data.downloadUrl;
    var releaseUrl = data.releaseUrl || releaseUrlFromDownload(downloadUrl);

    setText(root, 'version', version);
    setText(root, 'fileName', data.fileName);
    setText(root, 'fileSize', formatBytes(Number(data.sizeBytes)));
    setText(root, 'sha256', data.sha256);
    setText(root, 'nativeGitCommit', data.nativeGitCommit);
    setHref(root, 'downloadUrl', downloadUrl);
    setHref(root, 'releaseUrl', releaseUrl);
  }

  document.querySelectorAll('[data-manifest-url]').forEach(function (root) {
    fetch(root.getAttribute('data-manifest-url'), { cache: 'no-store' })
      .then(function (response) {
        if (!response.ok) throw new Error('metadata request failed');
        return response.json();
      })
      .then(function (data) { applyMetadata(root, data); })
      .catch(function () {
        root.setAttribute('data-metadata-status', 'fallback');
      });
  });
}());