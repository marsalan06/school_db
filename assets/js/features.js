document.addEventListener('DOMContentLoaded', () => {
    const topSection = document.getElementById('top');
    const featuresSection = document.getElementById('features');
  
    if (topSection && featuresSection) {
      const topHeight = featuresSection.offsetHeight;
      featuresSection.style.marginTop = `-${topHeight}px`;
    }
  });
  