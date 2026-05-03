document.addEventListener("DOMContentLoaded", () => {
  const TOC_HIDDEN = ["📎 Customer Files", "📸 Screenshots"];
  const toc = document.querySelector(".md-sidebar--secondary");

  function updateToc() {
    const active = document.querySelector(".tabbed-labels > label.tabbed-label--active, .tabbed-labels > label[aria-selected='true']");
    const label = active ? active.textContent.trim() : "";
    if (toc) toc.style.visibility = TOC_HIDDEN.some(t => label.includes(t)) ? "hidden" : "";
  }

  document.querySelectorAll(".tabbed-labels label").forEach(label => {
    label.addEventListener("click", () => setTimeout(updateToc, 50));
  });

  updateToc();
});
