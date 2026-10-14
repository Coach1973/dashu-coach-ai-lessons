/* 大樹作品通用漢堡選單（2026-10-14，教練：「這幾個站是不是要做漢堡按鈕」）
 *
 * 問題：各站頂部選單在窄螢幕（手機、平板、小筆電）會整個 display:none，手機上的人沒辦法跳段落。
 * 做法：螢幕窄於 data-bp 時，頂部列出現「☰ 選單」按鈕；點開是一整片大字清單，連結直接從頂部選單複製，
 *       所以頂部選單改了，這裡自動跟著變，不用維護兩份。字一律 20px 以上（教練 10/14 規定）。
 *
 * 用法（一行，放在 </body> 前；顏色各站自己帶）：
 *   <script src="/static/nav-burger.js?v=1" defer
 *     data-links=".nav ul a"            ← 要複製進選單的連結
 *     data-host=".nav .wrap"            ← 按鈕放進哪一個容器
 *     data-before=".nav .wrap > .btn"   ← 放在哪個元素前面（選填，沒有就放最後）
 *     data-bp="1180"                    ← 跟該站「頂部選單消失」的寬度一樣
 *     data-btn-bg="#fff" data-btn-fg="#0a1f3d" data-btn-ring="rgba(0,0,0,.15)"
 *     data-panel-bg="#fff" data-panel-fg="#0a1f3d" data-accent="#1c56b8" data-line="rgba(0,0,0,.1)"
 *     data-cta=".nav .wrap > .btn"     ← 頂部主要按鈕（選填）：一律複製到選單最下面當大按鈕
 *     data-cta-bp="560" data-cta-fg="#fff"></script>  ← 螢幕窄於 cta-bp 時頂部主要按鈕收起來（手機放不下三樣）
 * 改了這支檔案要把各站的 ?v= 加一（/static 有 4 小時快取）。
 * 已接：rongtree、runforfuture、social-club、social-good。
 */
(function () {
  var s = document.currentScript;
  if (!s) return;
  var d = s.dataset, bp = parseInt(d.bp, 10) || 1080;
  var host = document.querySelector(d.host || '.nav .wrap');
  var src = [].slice.call(document.querySelectorAll(d.links || '.nav ul a'));
  if (!host || !src.length) return;

  var c = {
    btnBg: d.btnBg || '#ffffff', btnFg: d.btnFg || '#1d2a22', btnRing: d.btnRing || 'rgba(0,0,0,.15)',
    panelBg: d.panelBg || '#ffffff', panelFg: d.panelFg || '#1d2a22', accent: d.accent || '#d9a441', line: d.line || 'rgba(0,0,0,.1)'
  };
  var st = document.createElement('style');
  st.textContent =
    '.bnb-btn{display:none;align-items:center;gap:9px;min-height:46px;padding:0 16px;border:0;border-radius:999px;cursor:pointer;flex:none;' +
      'font-family:inherit;font-size:20px;font-weight:700;line-height:1;letter-spacing:.06em;background:' + c.btnBg + ';color:' + c.btnFg + ';box-shadow:inset 0 0 0 2px ' + c.btnRing + '}' +
    '@media (max-width:' + bp + 'px){.bnb-btn{display:inline-flex}}' +
    '.bnb-ic{display:inline-flex;flex-direction:column;justify-content:center;gap:5px;width:22px;height:22px}' +
    '.bnb-ic i{display:block;height:3px;border-radius:2px;background:currentColor;transition:transform .2s,opacity .2s}' +
    '.bnb-btn[aria-expanded="true"] .bnb-ic i:nth-child(1){transform:translateY(8px) rotate(45deg)}' +
    '.bnb-btn[aria-expanded="true"] .bnb-ic i:nth-child(2){opacity:0}' +
    '.bnb-btn[aria-expanded="true"] .bnb-ic i:nth-child(3){transform:translateY(-8px) rotate(-45deg)}' +
    '.bnb-panel{position:fixed;left:0;right:0;z-index:1000;overflow:auto;background:' + c.panelBg + ';color:' + c.panelFg + ';box-shadow:0 18px 34px rgba(0,0,0,.22);padding:6px 0 18px}' +
    '.bnb-panel[hidden]{display:none}' +
    '.bnb-panel ul{list-style:none;margin:0 auto;padding:0 clamp(16px,4vw,40px);max-width:980px}' +
    '.bnb-panel a{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:16px 4px;font-size:22px;font-weight:700;line-height:1.4;text-decoration:none;color:inherit;border-bottom:1px solid ' + c.line + '}' +
    '.bnb-panel a::after{content:"\\203A";font-size:26px;color:' + c.accent + '}' +
    '.bnb-panel a:hover,.bnb-panel a:focus-visible{color:' + c.accent + '}' +
    '.bnb-panel a.bnb-cta-link{justify-content:center;margin-top:16px;border:0;border-radius:999px;background:' + c.accent + ';color:' + (d.ctaFg || '#ffffff') + '}' +
    '.bnb-panel a.bnb-cta-link::after{content:none}' +
    '.bnb-panel a.bnb-cta-link:hover,.bnb-panel a.bnb-cta-link:focus-visible{color:' + (d.ctaFg || '#ffffff') + ';filter:brightness(1.08)}' +
    (d.ctaBp ? '@media (max-width:' + parseInt(d.ctaBp, 10) + 'px){.bnb-cta-off{display:none!important}}' : '') +
    '@media (max-width:360px){.bnb-tx{display:none}.bnb-btn{padding:0 12px}}';
  document.head.appendChild(st);

  var btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'bnb-btn';
  btn.setAttribute('aria-expanded', 'false');
  btn.setAttribute('aria-controls', 'bnb-panel');
  btn.setAttribute('aria-label', '開啟選單');
  btn.innerHTML = '<span class="bnb-ic" aria-hidden="true"><i></i><i></i><i></i></span><span class="bnb-tx">選單</span>';
  var before = d.before && document.querySelector(d.before);
  // 放在 CTA 前：靠右並跟 CTA 隔 10px；放最後：跟前一個元素隔 10px
  if (before && before.parentNode === host) { host.insertBefore(btn, before); btn.style.margin = '0 10px 0 auto'; }
  else { host.appendChild(btn); btn.style.marginLeft = '10px'; }

  var panel = document.createElement('nav');
  panel.id = 'bnb-panel';
  panel.className = 'bnb-panel';
  panel.setAttribute('aria-label', '頁面選單');
  panel.hidden = true;
  var ul = document.createElement('ul');
  src.forEach(function (a) {
    var li = document.createElement('li'), n = document.createElement('a');
    n.href = a.getAttribute('href');
    n.textContent = a.textContent.trim();
    if (a.target) { n.target = a.target; n.rel = a.rel || 'noopener'; }
    li.appendChild(n);
    ul.appendChild(li);
  });
  var cta = d.cta && document.querySelector(d.cta);
  if (cta) {
    var cli = document.createElement('li'), ca = document.createElement('a');
    ca.href = cta.getAttribute('href'); ca.className = 'bnb-cta-link';
    ca.textContent = cta.textContent.replace(/[→↗›]/g, '').trim();
    if (cta.target) { ca.target = cta.target; ca.rel = cta.rel || 'noopener'; }
    cli.appendChild(ca); ul.appendChild(cli);
    if (d.ctaBp) cta.classList.add('bnb-cta-off');
    cta.style.whiteSpace = 'nowrap'; cta.style.flexShrink = '0';   // 多了選單鈕後，主要按鈕不准被擠成兩行
  }
  panel.appendChild(ul);
  document.body.appendChild(panel);

  function bar() { return (host.closest('header, nav') || host).getBoundingClientRect().bottom; }
  function open() {
    var top = Math.max(0, bar());
    panel.style.top = top + 'px';
    panel.style.maxHeight = (window.innerHeight - top) + 'px';
    panel.hidden = false;
    btn.setAttribute('aria-expanded', 'true');
    btn.setAttribute('aria-label', '關閉選單');
  }
  function close() {
    if (panel.hidden) return;
    panel.hidden = true;
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-label', '開啟選單');
  }
  btn.addEventListener('click', function (e) { e.stopPropagation(); panel.hidden ? open() : close(); });
  panel.addEventListener('click', function (e) { if (e.target.closest('a')) close(); });
  document.addEventListener('click', function (e) { if (!panel.contains(e.target)) close(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { close(); btn.focus(); } });
  window.addEventListener('resize', function () { if (window.innerWidth > bp) close(); });
})();
