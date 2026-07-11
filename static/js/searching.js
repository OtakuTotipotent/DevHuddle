function toggleFAQ(id, iconId) {
  const element = document.getElementById(id);
  const icon = document.getElementById(iconId);
  if (element.classList.contains("hidden")) {
    element.classList.remove("hidden");
    icon.style.transform = "rotate(180deg)";
  } else {
    element.classList.add("hidden");
    icon.style.transform = "rotate(0deg)";
  }
}

// 🔍 Isolated Client-Side Support Search Bar Engine
document
  .getElementById("support-search-input")
  .addEventListener("input", function (e) {
    const query = e.target.value.toLowerCase().trim();

    // Target all blocks that contain searchable information
    const categoryCards = document.querySelectorAll(
      ".grid-cols-1.md\\:grid-cols-3 > div",
    );
    const faqBlocks = document.querySelectorAll(
      ".lg\\:col-span-2 > .bg-gray-800",
    );

    // Filter Getting Started Category Cards
    categoryCards.forEach((card) => {
      const cardText = card.innerText.toLowerCase();
      if (cardText.includes(query)) {
        card.style.display = "";
      } else {
        card.style.display = "none";
      }
    });

    // Filter FAQs
    faqBlocks.forEach((block) => {
      const heading = block.querySelector("button").innerText.toLowerCase();
      const answer = block
        .querySelector('div[id^="faq"]')
        .innerText.toLowerCase();

      if (heading.includes(query) || answer.includes(query)) {
        block.style.display = "";
        // Automatically reveal the hidden text content block if matches are found
        if (query.length > 1) {
          block.querySelector('div[id^="faq"]').classList.remove("hidden");
          block.querySelector('span[id^="icon"]').style.transform =
            "rotate(180deg)";
        }
      } else {
        block.style.display = "none";
      }
    });
  });
