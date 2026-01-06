(function(){
  const toggle = document.querySelector('.menu-toggle');
  const menu = document.querySelector('.menu');
  const toast = document.getElementById('toast');
  const bell = document.getElementById('notif-bell');
  const badge = document.getElementById('notif-badge');
  const dropdown = document.getElementById('notif-dropdown');
  const list = document.getElementById('notif-list');
  const markAllBtn = document.getElementById('notif-mark-all');

  if (toggle && menu){
    toggle.addEventListener('click', () => {
      const open = menu.style.display === 'flex';
      menu.style.display = open ? 'none' : 'flex';
      toggle.setAttribute('aria-expanded', (!open).toString());
    });
  }

  window.showToast = function(message, timeout=2800){
    if (!toast) return;
    toast.textContent = message;
    toast.hidden = false;
    toast.style.opacity = '1';
    setTimeout(()=> {
      toast.style.opacity = '0';
      setTimeout(()=> toast.hidden = true, 300);
    }, timeout);
  };

  // --- Notifications dropdown logic ---
  if (bell && dropdown){
    bell.addEventListener('click', (e) => {
      // Toggle dropdown; keep link to full page with Ctrl/Meta
      if (!e.ctrlKey && !e.metaKey) {
        e.preventDefault();
        const hidden = dropdown.hasAttribute('hidden');
        dropdown.toggleAttribute('hidden');
        bell.setAttribute('aria-expanded', (!hidden).toString());
        if (hidden) fetchAndRenderNotifications();
      }
    });

    document.addEventListener('click', (e) => {
      if (!dropdown || dropdown.hasAttribute('hidden')) return;
      if (!dropdown.contains(e.target) && !bell.contains(e.target)){
        dropdown.setAttribute('hidden', '');
        bell.setAttribute('aria-expanded', 'false');
      }
    });
  }

  if (markAllBtn){
    markAllBtn.addEventListener('click', async () => {
      await postJSON('/notifications/api/mark-all-read/');
      await refreshUnreadBadge();
      fetchAndRenderNotifications();
      window.showToast && window.showToast('All notifications marked as read');
    });
  }

  async function fetchAndRenderNotifications(){
    const data = await getJSON('/notifications/api/list/');
    if (!data) return;
    renderNotifications(data.notifications);
    updateBadge(data.unread_count);
  }

  function renderNotifications(items){
    if (!list) return;
    list.innerHTML = '';
    if (!items.length){
      const empty = document.createElement('li');
      empty.className = 'notif-item';
      empty.textContent = 'No notifications';
      list.appendChild(empty);
      return;
    }
    items.forEach((n) => {
      const li = document.createElement('li');
      li.className = 'notif-item' + (n.is_read ? '' : ' unread');
      const a = document.createElement('a');
      a.href = n.url || '#';
      a.textContent = n.message;
      a.addEventListener('click', async (e) => {
        if (!n.url){ e.preventDefault(); return; }
        // Mark read optimistically
        await postJSON(`/notifications/api/mark-read/${n.id}/`);
        li.classList.remove('unread');
        refreshUnreadBadge();
      });
      const time = document.createElement('time');
      time.dateTime = n.created_at;
      time.textContent = formatRelativeTime(n.created_at);
      li.appendChild(a);
      li.appendChild(time);
      list.appendChild(li);
    });
  }

  function updateBadge(count){
    if (!badge) return;
    if (count && count > 0){
      badge.textContent = count;
      badge.removeAttribute('hidden');
    } else {
      badge.textContent = '';
      badge.setAttribute('hidden', '');
    }
  }

  async function refreshUnreadBadge(){
    const data = await getJSON('/notifications/api/unread-count/');
    if (data) updateBadge(data.unread_count);
  }

  function formatRelativeTime(iso){
    try {
      const d = new Date(iso);
      const diff = (Date.now() - d.getTime()) / 1000; // seconds
      if (diff < 60) return 'just now';
      if (diff < 3600) return `${Math.floor(diff/60)}m ago`;
      if (diff < 86400) return `${Math.floor(diff/3600)}h ago`;
      return `${Math.floor(diff/86400)}d ago`;
    } catch { return ''; }
  }

  async function getJSON(url){
    try {
      const res = await fetch(url, { credentials: 'same-origin' });
      if (!res.ok) return null;
      return await res.json();
    } catch { return null; }
  }

  async function postJSON(url){
    try {
      const res = await fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'X-CSRFToken': getCSRFToken() },
      });
      if (!res.ok) return null;
      return await res.json();
    } catch { return null; }
  }

  function getCSRFToken(){
    const name = 'csrftoken=';
    const cookies = document.cookie ? document.cookie.split(';') : [];
    for (let c of cookies){
      c = c.trim();
      if (c.startsWith(name)) return c.substring(name.length);
    }
    return '';
  }

  // Poll unread count every 30s
  setInterval(refreshUnreadBadge, 30000);
})();
