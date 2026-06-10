(() => {
  const videos = Array.from(document.querySelectorAll("[data-scroll-video]"));

  if (!videos.length || !("IntersectionObserver" in window)) {
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const video = entry.target;
        if (entry.isIntersecting && entry.intersectionRatio >= 0.55) {
          video.play().catch(() => {
            // Browsers may still block autoplay in some user settings.
          });
        } else {
          video.pause();
        }
      });
    },
    {
      threshold: [0, 0.55, 1],
    }
  );

  videos.forEach((video) => observer.observe(video));
})();
