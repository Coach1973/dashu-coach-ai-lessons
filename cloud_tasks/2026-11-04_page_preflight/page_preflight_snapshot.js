// 網頁交付前自檢（2026-11-04 教練：「不要每次都讓我抓到錯誤」——把教練這週親眼抓到的問題全部變成程式檢查）
// 用法：node scripts/page_preflight.js <網址>
// 電腦 1280／手機 390 各掃一次，檢查：
//  ① 字看不清（對比 <2.2＝🔴，2.2～3＝🟡偏淡；淡色浮水印、60px 以上裝飾字不算）：一般底色算對比；壓在漸層／背景圖／照片上的字，先把字藏起來截圖、取字下方像素算對比（11/03 rebreathe、10/29 榮樹下手冊）
//  ② 往下捲表頭不見（11/02 教練抓到；常見原因 body overflow-x:hidden 讓 sticky 失效）
//  ③ 手機左右捲動　④ 字小於 20px（教練 10/14 定）　⑤ 圖片壞掉或單張超過 1MB　⑥ 大樹作品頁常規連結（TAVA AI／榕樹下／人才軍火庫）
// 結束碼：有 🔴 就回 1。⑥只提醒、不算失敗（要不要加由教練決定，但要主動問）
const {chromium}=require(__dirname+'/node_modules/playwright-core');
const url=process.argv[2]; if(!url){console.log('用法：node page_preflight.js <網址>');process.exit(2);}
(async()=>{
 const b=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 let red=0; const say=(ok,msg)=>{if(!ok)red++;console.log((ok?'  ✅ ':'  🔴 ')+msg)};
 const bigImgs=new Map();
 for(const w of [1280,390]){
  const p=await b.newPage({viewport:{width:w,height:900}});
  p.on('response',async r=>{try{if(r.request().resourceType()==='image'){const len=+(r.headers()['content-length']||0);if(len>1048576)bigImgs.set(r.url(),len)}}catch(e){}});
  await p.goto(url,{waitUntil:'networkidle',timeout:60000}); await p.waitForTimeout(1200);
  await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=700){scrollTo(0,y);await new Promise(r=>setTimeout(r,120))}scrollTo(0,0)});
  await p.waitForTimeout(800);
  console.log(`\n【${w===1280?'電腦':'手機'} ${w}px】`);
  const info=await p.evaluate(()=>{
   const parse=c=>(c.match(/[\d.]+/g)||[0,0,0]).map(Number);
   const lum=([r,g,bb])=>{const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};return .2126*f(r)+.7152*f(g)+.0722*f(bb)};
   const cr=(a,b)=>{const x=lum(a),y=lum(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
   const solid=[],pix=[],pale=[];let small=0;const smallEx=[];let id=0;
   for(const e of document.querySelectorAll('body *')){
    const cs=getComputedStyle(e);
    if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity===0)continue;
    if(!e.offsetParent&&cs.position!=='fixed')continue;
    const txt=[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join('').trim();
    if(!txt)continue;
    const r=e.getBoundingClientRect(); if(r.width<2||r.height<2)continue;
    const fs=parseFloat(cs.fontSize); if(fs<19.5&&!/^(SCRIPT|STYLE|SUP|SUB)$/.test(e.tagName)){small++;if(smallEx.length<4)smallEx.push(txt.slice(0,12)+'('+fs+'px)')}
    let a=e,mode=null,bg=null;
    while(a){const s=getComputedStyle(a);
     if(s.backgroundImage&&s.backgroundImage!=='none'){mode='pix';break}
     const m=parse(s.backgroundColor);if(m.length===3||(m.length===4&&m[3]>0.5)){mode='solid';bg=m;break}
     a=a.parentElement}
    if(!mode){mode='solid';bg=[255,255,255]}
    const col=parse(cs.color);
    if((col.length===4&&col[3]<0.4)||fs>=60)continue; // 淡色浮水印、超大裝飾數字＝刻意設計，不算
    const tag=(e.className&&typeof e.className==='string'?'.'+e.className.split(' ')[0]:e.tagName)+'「'+txt.slice(0,14)+'」';
    if(mode==='solid'){const c=cr(col,bg);if(c<2.2)solid.push(tag+' 對比'+c.toFixed(2));else if(c<3)pale.push(tag)}
    else{e.dataset.pfId=++id;pix.push({id,tag,col,x:r.left+scrollX,y:r.top+scrollY,w:r.width,h:r.height})}
   }
   const head=[...document.querySelectorAll('header,nav,[class*=header],[class*=nav]')].find(h=>{const s=getComputedStyle(h),r=h.getBoundingClientRect();return r.top<5&&r.height>20&&r.height<260&&r.width>innerWidth*.6&&(s.position==='sticky'||s.position==='fixed')});
   const anyTop=[...document.querySelectorAll('header,nav')].some(h=>h.getBoundingClientRect().top<5&&h.getBoundingClientRect().height>20);
   const imgs=[...document.images].filter(i=>i.offsetParent&&i.getBoundingClientRect().width>8);
   const broken=imgs.filter(i=>i.complete&&i.naturalWidth===0).map(i=>(i.currentSrc||i.src).slice(-50));
   const bigData=imgs.filter(i=>(i.currentSrc||i.src).startsWith('data:')&&(i.currentSrc||i.src).length>1400000).length;
   const html=document.documentElement.innerHTML;
   return {solid,pale,pix,small,smallEx,hasHead:!!head,anyTop,broken,bigData,
     scrollW:document.documentElement.scrollWidth,vw:innerWidth,docH:document.body.scrollHeight,
     links:{tava:/tava-ai\.com/i.test(html),rong:/rongtree|榕樹下|榮樹下/.test(html),sky:/skyteam|人才軍火庫/.test(html)}};
  });
  let pixBad=[];
  if(info.pix.length){
   await p.addStyleTag({content:'[data-pf-id]{color:transparent!important;text-shadow:none!important;-webkit-text-stroke:0!important}'});
   await p.waitForTimeout(150);
   const shot=await p.screenshot({fullPage:true,type:'png'});
   pixBad=await p.evaluate(async({b64,items})=>{
    const img=new Image();img.src='data:image/png;base64,'+b64;await img.decode();
    const c=document.createElement('canvas');c.width=img.width;c.height=img.height;const g=c.getContext('2d');g.drawImage(img,0,0);
    const lum=([r,gg,bb])=>{const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};return .2126*f(r)+.7152*f(gg)+.0722*f(bb)};
    const out=[];
    for(const it of items){
     const L=lum(it.col);const xs=[];
     for(let i=0;i<6;i++)for(let j=0;j<3;j++){const x=Math.round(it.x+it.w*(i+.5)/6),y=Math.round(it.y+it.h*(j+.5)/3);
      if(x>=c.width||y>=c.height)continue;const d=g.getImageData(x,y,1,1).data;const l=lum([d[0],d[1],d[2]]);xs.push((Math.max(L,l)+.05)/(Math.min(L,l)+.05))}
     if(!xs.length)continue; xs.sort((a,b)=>a-b);
     const worst=xs[Math.floor(xs.length*.25)];
     if(worst<2.2)out.push(it.tag+' 對比'+worst.toFixed(2)+'（壓在圖／漸層上）');
    }
    return out;
   },{b64:shot.toString('base64'),items:info.pix});
   await p.evaluate(()=>document.querySelectorAll('[data-pf-id]').forEach(e=>delete e.dataset.pfId));
  }
  const bad=[...info.solid,...pixBad];
  say(!bad.length,`字看得清楚：${bad.length?bad.length+' 處看不清':'全部 OK'}`); bad.slice(0,40).forEach(x=>console.log('      '+x));
  if(info.pale.length)console.log('  🟡 偏淡但看得到（對比 2.2～3）'+info.pale.length+' 處，例：'+info.pale.slice(0,3).join('、'));
  if(info.hasHead){
   const still=await p.evaluate(async()=>{scrollTo(0,Math.min(1800,document.body.scrollHeight/2));await new Promise(r=>setTimeout(r,300));
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
