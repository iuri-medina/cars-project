// Image carousel functionality
document.addEventListener('DOMContentLoaded', function () {
  let currentSlide = 0;
  const slides = document.querySelectorAll('.carousel img');
  const indicators = document.querySelectorAll('.indicator');

  const activeSlide = document.querySelector('.carousel img.active');
  if (activeSlide) {
    currentSlide = parseInt(activeSlide.getAttribute('data-slide')) || 0;
  }

  function updateSlide(index) {
    slides.forEach((slide) => slide.classList.remove('active'));
    indicators.forEach((indicator) => indicator.classList.remove('active'));

    if (slides[index]) {
      slides[index].classList.add('active');
    }
    if (indicators[index]) {
      indicators[index].classList.add('active');
    }

    const currentCounter = document.getElementById('current-image');
    if (currentCounter) {
      currentCounter.textContent = index + 1;
    }

    currentSlide = index;
  }

  window.showSlide = function (index) {
    if (index >= 0 && index < slides.length) {
      updateSlide(index);
    }
  };

  window.nextSlide = function () {
    const nextIndex = (currentSlide + 1) % slides.length;
    updateSlide(nextIndex);
  };

  window.prevSlide = function () {
    const prevIndex = (currentSlide - 1 + slides.length) % slides.length;
    updateSlide(prevIndex);
  };

  document.addEventListener('keydown', function (e) {
    if (slides.length > 1) {
      if (e.key === 'ArrowRight') nextSlide();
      if (e.key === 'ArrowLeft') prevSlide();
    }
  });
});
