css = """
.loader-container {
  display: flex; /* Use flex to align items horizontally */
  align-items: center; /* Center items vertically within the container */
  white-space: nowrap; /* Prevent line breaks within the container */
}

.loader {
  border: 8px solid #f3f3f3; /* Light grey */
  border-top: 8px solid #3498db; /* Blue */
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Style the progress bar */
progress {
  appearance: none; /* Remove default styling */
  height: 20px; /* Set the height of the progress bar */
  border-radius: 5px; /* Round the corners of the progress bar */
  background-color: #f3f3f3; /* Light grey background */
  width: 100%;
}

/* Style the progress bar container */
.progress-container {
  margin-left: 20px;
  margin-right: 20px;
  flex-grow: 1; /* Allow the progress container to take up remaining space */
}

/* Set the color of the progress bar fill */
progress::-webkit-progress-value {
  background-color: #3498db; /* Blue color for the fill */
}

progress::-moz-progress-bar {
  background-color: #3498db; /* Blue color for the fill in Firefox */
}

/* Style the text on the progress bar */
progress::after {
  content: attr(value '%'); /* Display the progress value followed by '%' */
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white; /* Set text color */
  font-size: 14px; /* Set font size */
}

/* Style other texts */
.loader-container > span {
  margin-left: 5px; /* Add spacing between the progress bar and the text */
}

.progress-bar > .generating {
  display: none !important;
}

.progress-bar{
  height: 30px !important;
}

.hint-container > .generating {
  display: none !important;
}

.hint-container{
  height: 150px !important;
}

.json-container{
  height: 600px;
  overflow: auto !important;
  }

.type_row{
  height: 96px !important;
}
.type_small_row{
  height: 40px !important;
}

.type_row_half{
  height: 32px !important;
}

.scroll-hide{
  resize: none !important;
}

.refresh_button{
  border: none !important;
  background: none !important;
  font-size: none !important;
  box-shadow: none !important;
}

.advanced_check_row{
  width: 250px !important;
}

.min_check{
  min-width: min(1px, 100%) !important;
}

.resizable_area {
  resize: vertical;
  overflow: auto !important;
}

.aspect_ratios label {
    width: 140px !important;
}

.aspect_ratios label span {
    white-space: nowrap !important;
}

.aspect_ratios label input {
    margin-left: -5px !important;
}

.element1 {
  opacity: 0.01;
}

div.block.tokenCounter {
  width: auto;
  position: absolute;
  right: 0.4em;
  bottom: 0.4em;
  padding: 0 0.5em;
  opacity: 0.5;
  background-color: var(--neutral-900);
  border-radius: var(--radius-md);
}

div.block.tokenCounter div.wrap.center.full {
  display: none !important;
}

div.prose.tokenCounter {
  min-height: auto;
}

#inpaint_sketch { overflow: overlay !important; resize: auto; background: var(--panel-background-fill); z-index: 5; }

"""
progress_html = """
<div class="loader-container">
  <div class="loader"></div>
  <div class="progress-container">
    <progress value="*number*" max="100"></progress>
  </div>
  <span>*text*</span>
</div>
"""
scripts = """
function generate_shortcut(){
  document.addEventListener('keydown', (e) => {
    let handle = 'none';
    if (e.key !== undefined) {
      if ((e.key === 'Enter' && e.ctrlKey)) handle = 'run';
    } else if (e.keyCode !== undefined) {
      if ((e.keyCode === 13 && e.ctrlKey)) handle = 'run';
    }
    if (e.key !== undefined) {
      if ((e.key === 'Shift' && e.ctrlKey)) handle = 'hurtme';
    } else if (e.keyCode !== undefined) {
      if ((e.keyCode === 16 && e.ctrlKey)) handle = 'hurtme';
    }
    if (handle == 'run') {
      const button = document.getElementById('generate');
      if (button) button.click();
      e.preventDefault();
    }
    if (handle == 'hurtme') {
      const ctrl = document.getElementById('hurtme').getElementsByTagName('INPUT')[0];
      if (ctrl) ctrl.click();
      e.preventDefault();
    }
  });
}
"""

from shared import state


def make_progress_html(number, text):
    if number == -1:
        number = state["last_progress"]
    else:
        state["last_progress"] = number
    return progress_html.replace("*number*", str(number)).replace("*text*", text)
