const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const placeholderIcon = placeholderImage;

// Utility function to prevent default browser behavior
function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}

// Preventing default browser behavior when dragging a file over the container
dropArea.addEventListener('dragover', preventDefaults);
dropArea.addEventListener('dragenter', preventDefaults);
dropArea.addEventListener('dragleave', preventDefaults);

// Handling dropping files into the area
dropArea.addEventListener('drop', handleDrop);

function handleDrop(e) {
    e.preventDefault();
  
    // Getting the list of dragged files
    const files = e.dataTransfer.files;
  
    // Checking if there are any files
    if (files.length < 2) {
      // Assigning the files to the hidden input from the first step
      fileInput.files = files;
  
      // Processing the files for previews (next step)
      handleFiles(files);
    }
}
  
function handleFiles(files) {
    for (const file of files) {
      // Initializing the FileReader API and reading the file
      const reader = new FileReader();
      reader.readAsDataURL(file);
  
      // Once the file has been loaded, fire the processing
      reader.onloadend = function (e) {
        const preview = document.createElement('img');
  
        if (isValidFileType(file)) {
          preview.src = e.target.result;
        } else {
          preview.src = placeholderIcon;
        }
  
        // Apply styling
        preview.classList.add('preview-image');
        const previewContainer = document.getElementById('preview-container');
        previewContainer.appendChild(preview);
      };
    }
}
  
function isValidFileType(file) {
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
    return allowedTypes.includes(file.type);
}

dropArea.addEventListener('dragover', () => {
    dropArea.classList.add('drag-over');
});
  
dropArea.addEventListener('dragleave', () => {
    dropArea.classList.remove('drag-over');
});