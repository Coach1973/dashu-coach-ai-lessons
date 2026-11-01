// 改完網頁後掃一遍：全頁文字對底色對比 < 3 的元素 + 左右捲動（電腦 1280／手機 390）
// 用法：node scripts/page_contrast_scan.js <網址>   （2026-11-01 互動頁深色區塊白底白字連犯兩次後做）
const {chromium}=require(__dirname+'/node_modules/playwright-core');
const url=process.argv[2]; if(!url){console.log('用法：node page_contrast_scan.js <網址>');process.exit(1);}
(async()=>{
 const b=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 for(const w of [1280,390]){
  const p=await b.newPage({viewport:{width:w,height:900}});
  await p.goto(url,{waitUntil:'networkidle'}); await p.waitForTimeout(1500);
  const r=await p.evaluate(()=>{
   const lum=c=>{const m=c.match(/[\d.]+/g).map(Number);const [r,g,b]=m.slice(0,3).map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)});return .2126*r+.7152*g+.0722*b};
   const bg=e=>{while(e){const c=getComputedStyle(e).backgroundColor;const m=c.match(/[\d.]+/g);if(m&&(m.length<4||+m[3]>0.5))return c;e=e.parentElement}return 'rgb(255,255,255)'};
   const cr=(a,b)=>{const x=lum(a),y=lum(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
   const bad=[];
   for(const e of document.querySelectorAll('body *')){
    if(!e.offsetParent&&getComputedStyle(e).position!=='fixed')continue;
    if(![...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))continue;
    const cs=getComputedStyle(e),c=cr(cs.color,bg(e));
    if(c<3)bad.push((e.className||e.tagName)+' | '+e.textContent.trim().slice(0,16)+' | '+cs.color+' on '+bg(e)+' | '+c.toFixed(2));
   }
   return {bad,scrollW:document.documentElement.scrollWidth,vw:innerWidth};
  });
  console.log(w,'左右捲動:',r.scrollW>r.vw?'有 '+r.scrollW:'無','低對比',r.bad.length,'個'); r.bad.slice(0,20).forEach(x=>console.log('  ',x));
  await p.close();
 }
 console.log('提醒：圖片還沒載入的大圖區塊、疊在圖上的字可能誤報；互動狀態（選中／送出後）要另外手動點過再掃。');
 await b.close();
})();
