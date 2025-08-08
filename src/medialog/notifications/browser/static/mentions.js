//For use with 'mention', if user types @username in TinyMCE or other field

function fetchMentions(pattern) {
    const portalUrl = document.body.getAttribute('data-portal-url') || '';
    const mentionsUrl = portalUrl + '/@mentions_view';
    return fetch(mentionsUrl, {
        headers: { 'Accept': 'application/json' }
    })
        .then(res => res.json())
        .then(users => users
            .filter(u => u.key.toLowerCase().includes(pattern.toLowerCase()))
            .map(u => ({
                value: '@' + u.value,
                text: u.key
            }))
        );
}


function attachMentionsAutocomplete(textarea) {
    const dropdown = document.createElement('div');
    dropdown.className = 'mentions-dropdown';
    dropdown.style.position = 'absolute';
    dropdown.style.background = 'white';
    dropdown.style.border = '1px solid #ccc';
    dropdown.style.zIndex = 1000;
    dropdown.style.display = 'none';
    textarea.parentNode.style.position = 'relative'; // Required!
    textarea.parentNode.appendChild(dropdown);
  
    textarea.addEventListener('input', async () => {
      const pos = textarea.selectionStart;
      const text = textarea.value.slice(0, pos);
      const match = /@(\w+)$/.exec(text);
  
      if (!match) {
        dropdown.style.display = 'none';
        return;
      }
  
      const pattern = match[1];
      const mentions = await fetchMentions(pattern);
      if (!mentions.length) {
        dropdown.style.display = 'none';
        return;
      }
  
      const coords = getCaretCoordinatesRelativeToTextarea(textarea, pos);
  
      dropdown.innerHTML = '';
      mentions.forEach(item => {
        const div = document.createElement('div');
        div.textContent = item.text;
        div.style.padding = '4px 8px';
        div.style.cursor = 'pointer';
        div.addEventListener('mousedown', (e) => {
          e.preventDefault(); // keep focus
          const before = textarea.value.slice(0, pos - pattern.length - 1);
          const after = textarea.value.slice(pos);
          textarea.value = before + item.value + ' ' + after;
  
          const newPos = before.length + item.value.length + 1;
          textarea.setSelectionRange(newPos, newPos);
          textarea.focus();
          dropdown.style.display = 'none';
        });
        dropdown.appendChild(div);
      });
  
      dropdown.style.left = `${coords.left}px`;
      dropdown.style.top = `${coords.top + 15}px`; // add some offset
      dropdown.style.display = 'block';
    });
  
    document.addEventListener('click', (e) => {
      if (!dropdown.contains(e.target) && e.target !== textarea) {
        dropdown.style.display = 'none';
      }
    });
  }
  

$(document).ready(function () {
    $('#form-widgets-comment-text').click(function () {
        attachMentionsAutocomplete(this);    
    });
});


function getCaretCoordinatesRelativeToTextarea(textarea, position) {
    const div = document.createElement('div');
    const style = window.getComputedStyle(textarea);
  
    // Copy the necessary styles
    const props = [
      'borderWidth', 'fontFamily', 'fontSize', 'fontStyle', 'fontWeight', 'letterSpacing',
      'lineHeight', 'padding', 'textAlign', 'textTransform', 'whiteSpace', 'wordSpacing',
      'width', 'height'
    ];
    props.forEach(prop => {
      div.style[prop] = style[prop];
    });
  
    div.style.position = 'absolute';
    div.style.visibility = 'hidden';
    div.style.whiteSpace = 'pre-wrap';
    div.style.wordWrap = 'break-word';
    div.style.overflow = 'auto';
  
    // Add the content with a marker span
    const before = textarea.value.substring(0, position);
    const after = textarea.value.substring(position);
    div.textContent = before;
  
    const span = document.createElement('span');
    span.textContent = after.length ? after[0] : '.';
    div.appendChild(span);
  
    // Ensure matching width
    div.style.width = textarea.offsetWidth + 'px';
    div.style.height = textarea.offsetHeight + 'px';
  
    textarea.parentNode.appendChild(div);
    const rect = span.getBoundingClientRect();
    const parentRect = textarea.getBoundingClientRect();
    const top = rect.top - parentRect.top;
    const left = rect.left - parentRect.left;
    textarea.parentNode.removeChild(div);
  
    return { top, left };
  }