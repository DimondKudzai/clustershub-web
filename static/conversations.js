const threadsContainer = document.getElementById('threads');
const newThreadForm = document.getElementById('new-thread-form');
const titleInput = document.getElementById('thread-title');
const bodyInput = document.getElementById('thread-body');

let threads = [];

newThreadForm.addEventListener('submit', function (e) {
  e.preventDefault();

  const title = titleInput.value.trim();
  const body = bodyInput.value.trim();

  if (!title || !body) return;

  const thread = {
    title,
    body,
    comments: [],
  };

  threads.push(thread);
  renderThreads();

  titleInput.value = '';
  bodyInput.value = '';
});

function renderThreads() {
  threadsContainer.innerHTML = '';

  threads.forEach((thread, index) => {
    const threadEl = document.createElement('div');
    threadEl.classList.add('thread');

    const commentsHtml = thread.comments.map(comment =>`<div class="comment">comment</div>`
    ).join(”);
    
    threadEl.innerHTML = `
    <h4 class="thread-title">{thread.title}</h4>
    <p>thread.body</p>
    <div class="comment-section">{commentsHtml}
    <input type="text" class="reply-input" placeholder="Reply..." data-index="${index}" />
    </div>
    `;
    
    const replyInput = threadEl.querySelector('.reply-input');
    replyInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && this.value.trim() !== '') {
    threads[index].comments.push(this.value.trim());
    renderThreads();
    }
    });
    
    threadsContainer.appendChild(threadEl);
    });
    }
