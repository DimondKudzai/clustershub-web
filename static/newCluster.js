const input = document.getElementById('tag-input');
const tagList = document.getElementById('tag-list');
const suggestionsBox = document.getElementById('suggestions');

const selectedTags = [];

document.getElementById('skills-input').value = JSON.stringify(selectedTags);

input.addEventListener('input', () => {
  const value = input.value.toLowerCase();
  suggestionsBox.innerHTML = '';

  if (!value) {
    suggestionsBox.style.display = 'none';
    return;
  }

  const filtered = availableTags.filter(tag =>
    tag.toLowerCase().includes(value) && !selectedTags.includes(tag)
  );

  if (filtered.length === 0) {
    const li = document.createElement('li');
    li.textContent = `Add "${input.value}"`;
    li.onclick = () => addTag(input.value);
    suggestionsBox.appendChild(li);
  } else {
    filtered.forEach(tag => {
      const li = document.createElement('li');
      li.textContent = tag;
      li.onclick = () => addTag(tag);
      suggestionsBox.appendChild(li);
    });
  }
suggestionsBox.style.display = 'block'; // <-- show the box
});

input.addEventListener('keydown', function (e) {
  if (e.key === 'Enter' && input.value.trim() !== '') {
    e.preventDefault();
    addTag(input.value.trim());
  }
});

function addTag(text) {
    if (selectedTags.length >= 10) {
        alert('You can add up to 10 skills only');
        return;
    }
    if (selectedTags.includes(text)) return;
    selectedTags.push(text);
    const tagItem = document.createElement('li');
    tagItem.textContent = text;
    const removeBtn = document.createElement('span');
    removeBtn.textContent = '×';
    removeBtn.onclick = () => {
        tagItem.remove();
        selectedTags.splice(selectedTags.indexOf(text), 1);
        document.getElementById('skills-input').value = JSON.stringify(selectedTags);
    };
    tagItem.appendChild(removeBtn);
    tagList.appendChild(tagItem);
    input.value = '';
    suggestionsBox.innerHTML = '';
    suggestionsBox.style.display = 'none';
    document.getElementById('skills-input').value = JSON.stringify(selectedTags);
}