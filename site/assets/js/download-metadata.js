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
    var platform = root.getAttribute('data-sdk-platform');
    if (platform) {
      var version = data.sdkVersion;
      var extension = platform === 'windows-x64' ? '.zip' : '.tar.gz';
      var tag = 'nexatomtt-sdk-v' + version;
      var fileName = tag + '-' + platform + extension;
      var releaseBase = 'https://github.com/nexatom-research/nexatom-downloads/releases/';
      if (!data || data.schemaVersion !== 1 || data.artifactName !== 'nexatomtt-sdk' ||
          data.channel !== 'preview' || data.distribution !== 'public-preview' ||
          data.nativeApiVersion !== '1' || data.platform !== platform ||
          !/^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$/.test(version || '') ||
          /(?:^|[-.+])dev(?:$|[-.+])/i.test(version) ||
          !/^[0-9a-f]{40}$/.test(data.nativeGitCommit || '') ||
          !/^[0-9a-f]{64}$/.test(data.sha256 || '') ||
          !Number.isSafeInteger(data.sizeBytes) || data.sizeBytes <= 0 ||
          data.fileName !== fileName || data.releaseTag !== tag ||
          data.downloadUrl !== releaseBase + 'download/' + tag + '/' + fileName ||
          data.releaseUrl !== releaseBase + 'tag/' + tag) {
        throw new Error('SDK metadata does not identify a complete platform release');
      }
    }
    var version = platform ? data.sdkVersion : (data.version || data.sdkVersion);
    var downloadUrl = platform ? data.downloadUrl : (data.installerUrl || data.downloadUrl);
    var releaseUrl = data.releaseUrl || releaseUrlFromDownload(downloadUrl);

    setText(root, 'version', version);
    setText(root, 'fileName', data.fileName);
    setText(root, 'fileSize', formatBytes(Number(data.sizeBytes)));
    setText(root, 'sha256', data.sha256);
    setText(root, 'nativeGitCommit', data.nativeGitCommit);
    setHref(root, 'downloadUrl', downloadUrl);
    setHref(root, 'releaseUrl', releaseUrl);
    root.querySelectorAll('[data-release-pending]').forEach(function (node) { node.hidden = true; });
    root.querySelectorAll('[data-release-available]').forEach(function (node) { node.hidden = false; });
    root.setAttribute('data-metadata-status', 'live');
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
