const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const placeholderIcon = placeholderImage;
var previewImages = document.getElementsByClassName('preview-image');

// Utility function to prevent default browser behavior
function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}

// Preventing default browser behavior when dragging a file over the container
dropArea.addEventListener('dragover', preventDefaults);
dropArea.addEventListener('dragenter', preventDefaults);
dropArea.addEventListener('dragleave', preventDefaults);
// Handling button file uploads
fileInput.addEventListener('change', handleUpload);

// Handling dropping files into the area
dropArea.addEventListener('drop', handleDrop);

function handleUpload() {
  const fileList = this.files;

  if (previewImages.length < 1 && fileList.length < 2) {
    handleFiles(fileList);
  } else {
    fileInput.value = '';
    clearPreviews();
  }
}

function handleDrop(e) {
  e.preventDefault();
  
  const files = e.dataTransfer.files;

  if (previewImages.length < 1 && files.length < 2) {
    handleFiles(files);
  } else {
    fileInput.value = ''; 
    clearPreviews();
  }
}

function handleFiles(files) {
  for (const file of files) {
    const reader = new FileReader();
    reader.readAsDataURL(file);

    reader.onloadend = function (e) {
      const preview = document.createElement('img');

      if (isValidFileType(file)) {
        preview.src = e.target.result;
      } else {
        fileInput.value = '';
        clearPreviews();
        return;
      }

      preview.classList.add('preview-image');
      document.getElementById('preview-container').appendChild(preview);
    };
  }
}

function clearPreviews() {
  for (let i = 0; i < previewImages.length; i++) {
    previewImages.item(i).remove();   
  }
  fileInput.value = '';
}

function isValidFileType(file) {
  const allowedTypes = ['image/jpeg', 'image/png'];
  return allowedTypes.includes(file.type);
}

dropArea.addEventListener('dragover', () => {
  dropArea.classList.add('drag-over');
});

dropArea.addEventListener('dragleave', () => {
  dropArea.classList.remove('drag-over');
});
