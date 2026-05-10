document.addEventListener("DOMContentLoaded", function () {
  var btn = document.createElement("button");
  btn.id = "pdf-export-btn";
  btn.title = "Export as PDF";
  btn.setAttribute("aria-label", "Export as PDF");
  btn.onclick = function () { window.print(); };
  btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>';
  document.body.appendChild(btn);
});
