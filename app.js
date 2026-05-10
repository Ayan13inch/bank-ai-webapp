document.getElementById("uploadBtn").addEventListener("click", upload);

async function upload() {
  const f = document.getElementById("file").files[0];
  const out = document.getElementById("out");
  if (!f) {
    out.textContent = "Please choose a file first.";
    return;
  }
  out.textContent = "Uploading and parsing...";
  const form = new FormData();
  form.append("statement", f);

  try {
    const resp = await fetch("/upload", { method: "POST", body: form });
    const data = await resp.json();
    if (!resp.ok) {
      out.textContent = "Error: " + (data.error || resp.statusText);
      return;
    }
    if (Array.isArray(data.transactions)) {
      if (data.transactions.length === 0) {
        out.textContent = "No transactions found.";
        return;
      }
      // Render a simple table if possible
      const keys = Object.keys(data.transactions[0]);
      let html = "<table><thead><tr>";
      keys.forEach(k => html += `<th>${escapeHtml(k)}</th>`);
      html += "</tr></thead><tbody>";
      data.transactions.forEach(row => {
        html += "<tr>";
        keys.forEach(k => html += `<td>${escapeHtml(String(row[k] ?? ""))}</td>`);
        html += "</tr>";
      });
      html += "</tbody></table>";
      out.innerHTML = html;
    } else {
      out.textContent = JSON.stringify(data, null, 2);
    }
  } catch (err) {
    out.textContent = "Upload failed: " + err.message;
  }
}

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, function(m) {
    return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[m];
  });
}
