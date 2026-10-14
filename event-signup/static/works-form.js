/* 大樹作品通用表單模組（2026-10-14，教練：「送出資料不用每次交代，使用者送出我就一定收到」）
 *
 * 用法（任何掛在 event.bymyway.com 的作品頁都一樣，兩行）：
 *   <form data-works-form="<網站 slug>" data-success="謝謝，我們會盡快聯絡您">
 *     <input name="name"> <input name="phone"> <input name="email">  ← 姓名必填；電話或 Email 擇一
 *     <select name="item">…</select> <textarea name="message"></textarea>   ← 選填
 *     其他任何有 name 的欄位（公司、類型…）會自動併進留言，不會漏
 *   </form>
 *   <script src="/static/works-form.js" defer></script>
 *
 * 送到 POST /api/works/contact → 存 works_contact_leads → 通知「活動報名即時通知」群（app.py api_works_contact）。
 * 範例：github_repos/social-good、flower-site。不要再手寫 fetch，也不要做「展示版不送出」的表單。
 */
(function () {
  var KNOWN = { name: 1, phone: 1, email: 1, item: 1, message: 1, website: 1 };

  function msgBox(f) {
    var m = f.querySelector('[data-works-msg]');
    if (!m) {
      m = document.createElement('p');
      m.setAttribute('data-works-msg', '');
      m.setAttribute('role', 'status');
      m.style.cssText = 'margin:.6em 0 0;font-size:.95em;color:#b42318';
      f.appendChild(m);
    }
    return m;
  }

  function labelOf(el) {
    if (el.id) {
      var l = document.querySelector('label[for="' + el.id + '"]');
      if (l) return l.textContent.replace(/[*＊]/g, '').trim();
    }
    var p = el.closest('label') || (el.parentElement && el.parentElement.querySelector('label'));
    return (p ? p.textContent.replace(/[*＊]/g, '').trim() : '') || el.name;
  }

  function wire(f) {
    var site = f.getAttribute('data-works-form');
    if (!site || f.__worksWired) return;
    f.__worksWired = true;
    f.removeAttribute('onsubmit');
    f.onsubmit = null;
    if (!f.querySelector('[name=website]')) {               // 防機器人隱藏欄位
      var hp = document.createElement('input');
      hp.name = 'website'; hp.tabIndex = -1; hp.autocomplete = 'off';
      hp.setAttribute('aria-hidden', 'true');
      hp.style.cssText = 'position:absolute;left:-9999px;width:1px;height:1px;opacity:0';
      f.appendChild(hp);
    }
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      e.stopImmediatePropagation();
      var m = msgBox(f), btn = f.querySelector('[type=submit],button:not([type])');
      m.textContent = '';
      var v = function (n) { var el = f.querySelector('[name="' + n + '"]'); return el ? (el.value || '').trim() : ''; };
      var d = { site: site, name: v('name'), phone: v('phone'), email: v('email'), item: v('item'),
                message: v('message'), website: v('website') };
      if (!d.email && /@/.test(d.phone)) { d.email = d.phone; d.phone = ''; }   // 「電話或 Email」共用一格時
      var extra = [];
      Array.prototype.forEach.call(f.elements, function (el) {
        if (!el.name || KNOWN[el.name] || /^(submit|button|hidden|password|file)$/.test(el.type)) return;
        if ((el.type === 'checkbox' || el.type === 'radio') && !el.checked) return;
        var val = (el.value || '').trim();
        if (val) extra.push(labelOf(el) + '：' + val);
      });
      if (extra.length) d.message = extra.join('\n') + (d.message ? '\n' + d.message : '');
      if (!d.name) { m.textContent = '請填寫姓名'; return; }
      if (d.phone.replace(/\D/g, '').length < 8 && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(d.email)) {
        m.textContent = '請留下正確的電話或 Email，我們才聯絡得到您'; return;
      }
      if (!f.checkValidity()) { f.reportValidity(); return; }
      var label = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = '送出中…'; }
      fetch('/api/works/contact', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(d) })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (j) {
          if (j.ok) {
            var ok = f.getAttribute('data-success') || '資料已送出，謝謝您！我們收到了，會盡快與您聯絡。';
            var box = document.createElement('div');
            box.setAttribute('role', 'status');
            box.style.cssText = 'padding:1.2em;border-radius:12px;background:rgba(16,185,129,.1);text-align:center;font-weight:600';
            box.textContent = ok;
            f.replaceWith(box);
            f.dispatchEvent(new CustomEvent('works:sent', { bubbles: true }));
          } else {
            if (btn) { btn.disabled = false; btn.textContent = label; }
            m.textContent = j.error || '送出失敗，請稍後再試一次';
          }
        })
        .catch(function () {
          if (btn) { btn.disabled = false; btn.textContent = label; }
          m.textContent = '網路不穩，資料還在，請再按一次送出';
        });
    }, true);
  }

  function init() { Array.prototype.forEach.call(document.querySelectorAll('form[data-works-form]'), wire); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
