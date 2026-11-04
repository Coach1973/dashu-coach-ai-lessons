// 網頁交付前自檢（2026-11-04 教練：「不要每次都讓我抓到錯誤」——把教練這週親眼抓到的問題全部變成程式檢查）
// 用法：node scripts/page_preflight.js <網址>
// 電腦 1280／手機 390 各掃一次，檢查：
//  ① 字看不清（對比 <2.2＝🔴，2.2～3＝🟡偏淡；淡色浮水印、60px 以上裝飾字不算）：一般底色算對比；壓在漸層／背景圖／照片上的字，先把字藏起來截圖、取字下方像素算對比（11/03 rebreathe、10/29 榮樹下手冊）
//  ② 往下捲表頭不見（11/02 教練抓到；常見原因 body overflow-x:hidden 讓 sticky 失效）
//  ③ 手機左右捲動　④ 字小於 20px（教練 10/14 定）　⑤ 圖片壞掉或單張超過 1MB　⑥ 大樹作品頁常規連結（TAVA AI／榕樹下／人才軍火庫）
// 結束碼：有 🔴 就回 1。⑥只提醒、不算失敗（要不要加由教練決定，但要主動問）
const fs=require('fs');
// 套件與瀏覽器「有就用、沒有就換」：Mac 用本資料夾的 playwright-core＋Google Chrome；雲端／其他電腦用全域 playwright 內建 chromium
const {chromium}=(()=>{for(const m of [__dirname+'/node_modules/playwright-core',__dirname+'/node_modules/playwright','playwright','playwright-core']){try{return require(m)}catch(e){}}throw new Error('找不到 playwright，請先安裝')})();
const CHROME=['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',process.env.PREFLIGHT_CHROME].filter(Boolean).find(x=>fs.existsSync(x));
const url=process.argv[2]; if(!url){console.log('用法：node page_preflight.js <網址>');process.exit(2);}
(async()=>{
 const b=await chromium.launch(CHROME?{executablePath:CHROME,headless:true}:{headless:true});
 let red=0; const say=(ok,msg)=>{if(!ok)red++;console.log((ok?'  ✅ ':'  🔴 ')+msg)};
 const bigImgs=new Map();
 for(const w of [1280,390]){
  const p=await b.newPage({viewport:{width:w,height:900}});
  p.on('response',async r=>{try{if(r.request().resourceType()==='image'){const len=+(r.headers()['content-length']||0);if(len>1048576)bigImgs.set(r.url(),len)}}catch(e){}});
  await p.goto(url,{waitUntil:'networkidle',timeout:60000}); await p.waitForTimeout(1200);
  await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=700){scrollTo({top:y,behavior:'instant'});await new Promise(r=>setTimeout(r,120))}scrollTo({top:0,behavior:'instant'})});
  await p.waitForTimeout(800);
  console.log(`\n【${w===1280?'電腦':'手機'} ${w}px】`);
  const info=await p.evaluate(()=>{
   const parse=c=>(c.match(/[\d.]+/g)||[0,0,0]).map(Number);
   const lum=([r,g,bb])=>{const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};return .2126*f(r)+.7152*f(g)+.0722*f(bb)};
   const cr=(a,b)=>{const x=lum(a),y=lum(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
   const items=[];let small=0;const smallEx=[];let id=0;
   for(const e of document.querySelectorAll('body *')){
    const cs=getComputedStyle(e);
    if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity===0)continue;
    if(!e.offsetParent&&cs.position!=='fixed')continue;
    if(e.closest('[aria-hidden="true"]'))continue; // 標成裝飾的（例如章節大編號）
    const tnodes=[...e.childNodes].filter(n=>n.nodeType===3&&n.textContent.trim());
    const txt=tnodes.map(n=>n.textContent).join('').trim();
    if(!txt)continue;
    const r=e.getBoundingClientRect(); if(r.width<2||r.height<2)continue;
    const fs=parseFloat(cs.fontSize); if(fs<19.5&&!/^(SCRIPT|STYLE|SUP|SUB)$/.test(e.tagName)){small++;if(smallEx.length<4)smallEx.push(txt.slice(0,12)+'('+fs+'px)')}
    const col=parse(cs.color);
    if(col.length===4&&col[3]<0.4)continue;            // 淡色浮水印、鏤空字＝刻意設計
    if(fs>=60&&/^[\d\s\W]{1,4}$/.test(txt))continue;     // 超大純數字編號＝裝飾；超大「標題」照樣要檢查
    // 字實際的不透明度＝字色透明度 × 所有上層 opacity
    let op=col.length===4?col[3]:1;for(let a=e;a;a=a.parentElement)op*=+getComputedStyle(a).opacity;
    const tag=(e.className&&typeof e.className==='string'&&e.className.trim()?'.'+e.className.trim().split(/\s+/)[0]:e.tagName)+'「'+txt.slice(0,14)+'」';
    e.dataset.pfId=++id;items.push({id,tag,col:col.slice(0,3),op,cy:r.top+scrollY+r.height/2});
   }
   const head=[...document.querySelectorAll('header,nav,[class*=header],[class*=nav]')].find(h=>{const s=getComputedStyle(h),r=h.getBoundingClientRect();return r.top<5&&r.height>20&&r.height<260&&r.width>innerWidth*.6&&(s.position==='sticky'||s.position==='fixed')});
   const anyTop=[...document.querySelectorAll('header,nav')].some(h=>h.getBoundingClientRect().top<5&&h.getBoundingClientRect().height>20);
   const imgs=[...document.images].filter(i=>i.offsetParent&&i.getBoundingClientRect().width>8);
   const broken=imgs.filter(i=>i.complete&&i.naturalWidth===0).map(i=>(i.currentSrc||i.src).slice(-50));
   const bigData=imgs.filter(i=>(i.currentSrc||i.src).startsWith('data:')&&(i.currentSrc||i.src).length>1400000).length;
   const html=document.documentElement.innerHTML;
   return {items,small,smallEx,hasHead:!!head,anyTop,broken,bigData,
     scrollW:document.documentElement.scrollWidth,vw:innerWidth,docH:document.body.scrollHeight,
     links:{tava:/tava-ai\.com/i.test(html),rong:/rongtree|榕樹下|榮樹下/.test(html),sky:/skyteam|人才軍火庫/.test(html)}};
  });
  // 字看不看得清（2026-11-04 雲端重寫，原本修前修後都報 50 多處、分不出好壞）：
  // 像真人一樣一段一段往下捲，每段字在「捲到畫面中間」那一刻量（捲動才升起的太陽、淡入動畫都算得到）。
  // 每個位置拍兩張：①正常 ②把字藏起來。兩張不同、而且是「往這個字自己的顏色變」的像素＝真的看得到的字；
  // 字底下真正的顏色＝第②張同一點。卡片背面、被蓋住的字兩張一樣→自動跳過；暗幕、漸層、::before、半透明底都算得到。
  let bad=[],pale=[];
  if(info.items.length){
   const H=900,step=Math.round(H*.75); // 一次捲 3/4 畫面：每段字量的時候都在畫面中間一半以內
   const maxY=Math.max(0,info.docH-H);
   const plan=new Map();
   for(const it of info.items){const c=it.cy-H/2;const y=Math.min(maxY,Math.max(0,Math.round(c/step)*step));if(!plan.has(y))plan.set(y,[]);plan.get(y).push(it.id)}
   const tagOf=new Map(info.items.map(it=>[it.id,it]));
   await p.addStyleTag({content:'html.pf-hide [data-pf-id]{color:transparent!important;-webkit-text-fill-color:transparent!important;text-shadow:none!important;-webkit-text-stroke:0!important;text-decoration-color:transparent!important;transition:none!important}'});
   for(const y of [...plan.keys()].sort((a,b)=>a-b)){
    await p.evaluate(y=>scrollTo({top:y,behavior:'instant'}),y); await p.waitForTimeout(250); // 淡入動畫在前面整頁捲過時已跑完；這裡只等捲動帶動的畫面（例如太陽升起）
    await p.evaluate(()=>document.getAnimations().forEach(a=>{try{a.pause()}catch(e){}}));
    const ids=plan.get(y);
    const rects=await p.evaluate(ids=>ids.map(id=>{const e=document.querySelector('[data-pf-id="'+id+'"]');if(!e)return [];
      const out=[];for(const n of e.childNodes){if(n.nodeType!==3||!n.textContent.trim())continue;const rg=document.createRange();rg.selectNodeContents(n);
       for(const q of rg.getClientRects())if(q.width>1&&q.height>1&&q.bottom>0&&q.top<innerHeight)out.push([q.left,q.top,q.width,q.height])}return out}),ids);
    const shotA=await p.screenshot({type:'png',caret:'hide'});
    await p.evaluate(()=>document.documentElement.classList.add('pf-hide'));await p.waitForTimeout(80);
    const shotB=await p.screenshot({type:'png',caret:'hide'});
    await p.evaluate(()=>{document.documentElement.classList.remove('pf-hide');document.getAnimations().forEach(a=>{try{a.play()}catch(e){}})});
    const items=ids.map((id,k)=>({tag:tagOf.get(id).tag,col:tagOf.get(id).col,op:tagOf.get(id).op,rects:rects[k]}));
    const res=await p.evaluate(async({a64,b64,items})=>{
     const load=async b=>{const im=new Image();im.src='data:image/png;base64,'+b;await im.decode();const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d',{willReadFrequently:true});g.drawImage(im,0,0);return g};
     const A=await load(a64),B=await load(b64);const W=A.canvas.width,Hh=A.canvas.height;
     const lin=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};
     const lum=(r,g,b)=>.2126*lin(r)+.7152*lin(g)+.0722*lin(b);
     const dist=(a,b,c,x,y,z)=>Math.abs(a-x)+Math.abs(b-y)+Math.abs(c-z);
     const bad=[],pale=[];
     for(const it of items){
      const cr=[];
      for(const [x0,y0,w,h] of it.rects){
       const x=Math.max(0,Math.floor(x0)),y=Math.max(0,Math.floor(y0)),ww=Math.min(W-x,Math.ceil(w)),hh=Math.min(Hh-y,Math.ceil(h));
       if(ww<1||hh<1)continue;
       const da=A.getImageData(x,y,ww,hh).data,db=B.getImageData(x,y,ww,hh).data;
       for(let i=0;i<da.length;i+=4){
        const br=db[i],bg=db[i+1],bb=db[i+2];
        if(dist(da[i],da[i+1],da[i+2],br,bg,bb)<48)continue;                 // 兩張一樣＝不是字
        const tr=it.col[0]*it.op+br*(1-it.op),tg=it.col[1]*it.op+bg*(1-it.op),tb=it.col[2]*it.op+bb*(1-it.op);
        if(dist(da[i],da[i+1],da[i+2],tr,tg,tb)>=dist(br,bg,bb,tr,tg,tb))continue; // 不是往「這個字的顏色」變＝是疊在同一塊的別的字
        const L1=lum(tr,tg,tb),L2=lum(br,bg,bb);cr.push((Math.max(L1,L2)+.05)/(Math.min(L1,L2)+.05));
       }
      }
      if(cr.length<12)continue; // 畫面上幾乎沒畫出來（卡片背面、被蓋住）＝訪客看不到，不算
      cr.sort((a,b)=>a-b);
      const v=cr[Math.floor(cr.length*.25)]; // 取較差的四分之一：字有一段壓在亮處也抓得到
      if(v<2.2)bad.push(it.tag+' 對比'+v.toFixed(2));else if(v<3)pale.push(it.tag);
     }
     return {bad,pale};
    },{a64:shotA.toString('base64'),b64:shotB.toString('base64'),items});
    bad.push(...res.bad);pale.push(...res.pale);
   }
   await p.evaluate(()=>{scrollTo({top:0,behavior:'instant'});document.querySelectorAll('[data-pf-id]').forEach(e=>delete e.dataset.pfId)});
  }
  say(!bad.length,`字看得清楚：${bad.length?bad.length+' 處看不清':'全部 OK'}`); bad.slice(0,40).forEach(x=>console.log('      '+x));
  if(pale.length)console.log('  🟡 偏淡但看得到（對比 2.2～3）'+pale.length+' 處，例：'+pale.slice(0,3).join('、'));
  if(info.hasHead){
   const still=await p.evaluate(async()=>{scrollTo({top:Math.min(1800,document.body.scrollHeight/2),behavior:'instant'});await new Promise(r=>setTimeout(r,300));
     const el=[...document.querySelectorAll('header,nav,[class*=header],[class*=nav]')].find(x=>{const s=getComputedStyle(x);return s.position==='sticky'||s.position==='fixed'});
     if(!el)return false;const r=el.getBoundingClientRect();return r.top>-2&&r.top<10&&r.height>10});
   say(still,`往下捲表頭還在：${still?'OK':'表頭不見了（查 body/html 有沒有 overflow-x:hidden、父層 overflow）'}`);
  }else if(info.anyTop&&info.docH>2500){
   say(false,'表頭沒有固定：頁面很長、最上面有選單，但往下捲就看不到（加 position:sticky; top:0）');
  }
  say(info.scrollW<=info.vw+1,`左右捲動：${info.scrollW>info.vw+1?'有，頁面寬 '+info.scrollW+'px > 畫面 '+info.vw+'px':'無'}`);
  say(info.small===0,`字 20px 以上：${info.small?info.small+' 處太小，例：'+info.smallEx.join('、'):'OK'}`);
  say(!info.broken.length,`圖片都有出來：${info.broken.length?info.broken.length+' 張壞掉：'+info.broken.slice(0,3).join('、'):'OK'}`);
  if(w===390){
   const L=info.links,miss=[!L.tava&&'TAVA AI',!L.rong&&'榕樹下',!L.sky&&'人才軍火庫'].filter(Boolean);
   if(/event\.bymyway\.com\/curated|coach1973\.github\.io|tava-ai\.com/.test(url)&&miss.length)console.log('  🟡 頁尾常規連結缺：'+miss.join('、')+' → 回報時主動問教練要不要加（教練 11/02）');
   if(info.bigData)console.log('  🟡 有 '+info.bigData+' 張內嵌大圖超過 1MB，可以壓縮');
  }
  await p.close();
 }
 if(bigImgs.size){red++;console.log('\n  🔴 單張圖片超過 1MB：');[...bigImgs].slice(0,5).forEach(([u,l])=>console.log('      '+(l/1048576).toFixed(1)+'MB '+u.slice(-60)))}
 console.log(red?`\n結果：🔴 ${red} 項要修，修完再跑一次，全過才交付`:'\n結果：✅ 全部通過，可以交付');
 console.log('（程式看不到的：人臉／主角有沒有被框切到、整體好不好看——交付前仍要截一張被改的那一塊親眼看）');
 await b.close(); process.exit(red?1:0);
})().catch(e=>{console.log('❌ 自檢跑不起來：'+e.message);process.exit(2)});
