// Additional functions for new_audiobook

const boxsetCheckbox = document.getElementById('id_boxset')
const boxsetInput = document.getElementById('id_boxset_name')

boxsetCheckbox.addEventListener('change', function() {
    if (this.checked) {
        boxsetInput.disabled = false
    } else {
        boxsetInput.value = ""
        boxsetInput.disabled = true
    }
})