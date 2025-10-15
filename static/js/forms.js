// Form image upload functionality
document.addEventListener('DOMContentLoaded', function () {
  const imageSlots = document.querySelectorAll('.image-slot');
  let mainImageIndex = null;

  imageSlots.forEach((slot, index) => {
    const input = slot.querySelector('input[type="file"]');
    const isMainInput = slot.querySelector(
      'input[type="checkbox"][name$="-is_main"]',
    );

    slot.addEventListener('click', function (e) {
      if (
        !e.target.classList.contains('btn-remove') &&
        !e.target.classList.contains('btn-main')
      ) {
        input.click();
      }
    });

    input.addEventListener('change', function (e) {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
          displayImage(slot, e.target.result, index);
        };
        reader.readAsDataURL(file);
      }
    });
  });

  function displayImage(slot, src, index) {
    slot.classList.add('has-image');

    const fileInput = slot.querySelector('input[type="file"]');
    const isMainInput = slot.querySelector(
      'input[type="checkbox"][name$="-is_main"]',
    );

    slot.innerHTML = `
      <img src="${src}" alt="Preview" class="image-preview">
      <div class="image-controls">
        <button type="button" class="btn-main" onclick="setMainImage(${index})">Principal</button>
        <button type="button" class="btn-remove" onclick="removeImage(${index})">×</button>
      </div>
    `;

    slot.appendChild(fileInput);
    slot.appendChild(isMainInput);

    if (mainImageIndex === null) {
      setMainImage(index);
    }
  }

  window.setMainImage = function (index) {
    document
      .querySelectorAll('.main-image-indicator')
      .forEach((el) => el.remove());
    document.querySelectorAll('.btn-main').forEach((btn) => {
      btn.classList.remove('active');
      btn.textContent = 'Principal';
    });

    const slot = document.querySelector(`[data-form-index="${index}"]`);
    const isMainInput = slot.querySelector(
      'input[type="checkbox"][name$="-is_main"]',
    );
    const mainBtn = slot.querySelector('.btn-main');

    if (isMainInput) {
      document
        .querySelectorAll('input[type="checkbox"][name$="-is_main"]')
        .forEach((input) => {
          input.checked = false;
        });

      isMainInput.checked = true;
      mainBtn.classList.add('active');
      mainBtn.textContent = 'Principal';

      const indicator = document.createElement('div');
      indicator.className = 'main-image-indicator';
      indicator.textContent = 'PRINCIPAL';
      slot.appendChild(indicator);

      mainImageIndex = index;
    }
  };

  window.removeImage = function (index) {
    const slot = document.querySelector(`[data-form-index="${index}"]`);
    const input = slot.querySelector('input[type="file"]');
    const isMainInput = slot.querySelector(
      'input[type="checkbox"][name$="-is_main"]',
    );

    slot.classList.remove('has-image');
    slot.innerHTML = `
      <div class="upload-placeholder">
        <i>📷</i>
        <div>Clique para<br>adicionar foto</div>
      </div>
    `;

    input.value = '';
    isMainInput.checked = false;
    slot.appendChild(input);
    slot.appendChild(isMainInput);

    if (mainImageIndex === index) {
      mainImageIndex = null;
      const slotsWithImages = document.querySelectorAll(
        '.image-slot.has-image',
      );
      if (slotsWithImages.length > 0) {
        const firstSlotIndex =
          slotsWithImages[0].getAttribute('data-form-index');
        setMainImage(parseInt(firstSlotIndex));
      }
    }

    const newInput = slot.querySelector('input[type="file"]');
    newInput.addEventListener('change', function (e) {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
          displayImage(slot, e.target.result, index);
        };
        reader.readAsDataURL(file);
      }
    });

    slot.addEventListener('click', function (e) {
      if (
        !e.target.classList.contains('btn-remove') &&
        !e.target.classList.contains('btn-main')
      ) {
        newInput.click();
      }
    });
  };
});
