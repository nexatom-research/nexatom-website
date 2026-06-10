(() => {
  const images = Array.from(document.querySelectorAll("img[data-expand-image]"));

  if (!images.length) {
    return;
  }

  let activeTrigger = null;

  const dialog = document.createElement("div");
  dialog.className = "lightbox";
  dialog.setAttribute("role", "dialog");
  dialog.setAttribute("aria-modal", "true");
  dialog.setAttribute("aria-label", "Expanded image");
  dialog.hidden = true;
  dialog.innerHTML = `
    <button class="lightbox-close" type="button" aria-label="Close expanded image">Close</button>
    <figure class="lightbox-figure">
      <img class="lightbox-image" alt="">
      <figcaption class="lightbox-caption"></figcaption>
    </figure>
  `;
  document.body.appendChild(dialog);

  const closeButton = dialog.querySelector(".lightbox-close");
  const lightboxImage = dialog.querySelector(".lightbox-image");
  const caption = dialog.querySelector(".lightbox-caption");

  const getCaption = (image) => {
    const figure = image.closest("figure");
    return image.dataset.expandCaption || figure?.querySelector("figcaption")?.textContent?.trim() || image.alt || "";
  };

  const open = (image) => {
    activeTrigger = document.activeElement;
    lightboxImage.src = image.currentSrc || image.src;
    lightboxImage.alt = image.alt || "";
    caption.textContent = getCaption(image);
    caption.hidden = !caption.textContent;
    dialog.hidden = false;
    document.body.classList.add("lightbox-open");
    closeButton.focus();
  };

  const close = () => {
    dialog.hidden = true;
    lightboxImage.removeAttribute("src");
    document.body.classList.remove("lightbox-open");
    activeTrigger?.focus();
    activeTrigger = null;
  };

  images.forEach((image) => {
    const wrapper = document.createElement("span");
    wrapper.className = "expandable-image-wrap";
    image.parentNode.insertBefore(wrapper, image);
    wrapper.appendChild(image);

    const button = document.createElement("button");
    button.className = "image-expand-button";
    button.type = "button";
    button.textContent = "⤢";
    button.setAttribute("aria-label", image.dataset.expandLabel || `Expand image: ${image.alt}`);
    wrapper.appendChild(button);

    image.classList.add("expandable-image");
    image.addEventListener("click", () => open(image));
    button.addEventListener("click", () => open(image));
  });

  closeButton.addEventListener("click", close);
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) {
      close();
    }
  });
  document.addEventListener("keydown", (event) => {
    if (!dialog.hidden && event.key === "Escape") {
      close();
    }
  });
})();
