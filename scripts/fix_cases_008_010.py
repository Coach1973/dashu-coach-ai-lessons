#!/usr/bin/env python3
"""
修正案例 #008-#010：
- 案例八：換新題目（$60 財務損失），加教練↔AI 完整對話
- 案例九：保留題目，加 AI 回應對話
- 案例十：保留題目，加 AI 回應對話
"""
import re

html_path = "/tmp/cool-case/index.html"

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# 找到案例八開始到 </section> 結束的位置（三個案例）
# 從 <div id="case8"> 到最後一個案例的 </section> 之後的 divider
start_marker = '<div id="case8"></div>'
end_marker = '<script>'

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

if start_idx < 0 or end_idx < 0:
    print(f"ERROR: Cannot find markers. start={start_idx}, end={end_idx}")
    exit(1)

print(f"Found case 8-10 block: chars {start_idx}-{end_idx}")

# 新的三個案例 HTML
new_cases = '''<div id="case8"></div>
<section class="section">
  <div class="section-label">案例八</div>
  <div class="section-title">60 美金，沒有人發現</div>
  <div class="section-desc">UI 手動切了模型，以為生效了。三天後帳單來了——$60 美金，因為沒有一個助教主動確認。</div>
  <div class="case-card case-008" data-case="8">
    <div class="case-header">
      <span class="case-tag">#01 在乎 · #11 自動自發 · #05 凡走過必留痕跡</span>
      <div class="case-num">08</div>
    </div>
    <div class="case-body">
      <div class="story-block">
        <div class="scene">——Kimi 帳單，悄悄在跑——</div>
        <div class="narrative">教練兩天前在 UI 介面手動把模型從 Kimi 切到 MiniMax。操作成功，介面也顯示「MiniMax」。教練放心了。</div>
        <div class="narrative">但沒人知道的是——UI 切換只改「執行期」狀態。gateway 一重啟，設定檔裡的 model 欄位沒改過，自動彈回 Kimi。</div>
        <div class="narrative">三天內，三個 AI 助教，沒有一個主動問過：「小龍蝦現在跑什麼模型？」</div>
      </div>
      <div class="chat-bubble chat-coach">
        <div class="chat-avatar coach"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="教練"></div>
        <div class="chat-content"><span class="chat-name">大樹教練</span>「現在有一個很嚴重的問題。我在兩天前就已經手動切換到 MiniMax 的模式，但不曉得為什麼沒有成功，它還是一直在跑 Kimi 的模式。」</div>
      </div>
      <div class="chat-bubble chat-ai">
        <div class="chat-avatar ai"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="AI"></div>
        <div class="chat-content"><span class="chat-name">小龍蝦 AI 特助</span>「教練，我來查一下。UI 介面顯示的確實是 MiniMax，看起來切換是成功的……可能是 cache 還沒刷新？」</div>
      </div>
      <div class="chat-bubble chat-coach">
        <div class="chat-avatar coach"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="教練"></div>
        <div class="chat-content"><span class="chat-name">大樹教練</span>「那你去查 openclaw.json 裡面 main 的 model 欄位，看看寫的是什麼。」</div>
      </div>
      <div class="chat-bubble chat-ai">
        <div class="chat-avatar ai"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="AI"></div>
        <div class="chat-content"><span class="chat-name">小龍蝦 AI 特助</span>「查了……model 欄位還是 kimi/kimi-k2.6。教練，設定檔從來沒被改過。」</div>
      </div>
      <div class="chat-bubble chat-coach">
        <div class="chat-avatar coach"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="教練"></div>
        <div class="chat-content"><span class="chat-name">大樹教練</span>「嚴重的失誤。因為這樣，我 Kimi 被扣了將近 60 塊美金，所以這是一個非常嚴重的錯誤。我居然手動切換不回去，也沒有人提醒我。」</div>
      </div>
      <div class="chat-bubble chat-ai">
        <div class="chat-avatar ai"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="AI"></div>
        <div class="chat-content"><span class="chat-name">小龍蝦 AI 特助</span>「教練，我錯了。UI 切換只改執行期狀態，gateway 一重啟就彈回設定檔的值。三天內我們三個助教，開工時沒有一個人去查過『現在跑的到底是什麼模型』。」</div>
      </div>
      <div class="chat-bubble chat-coach">
        <div class="chat-avatar coach"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="教練"></div>
        <div class="chat-content"><span class="chat-name">大樹教練</span>「你們每次開工有那麼多守則要讀、那麼多檔案要查，結果最基本的——現在跑什麼模型——沒有一個人問。這就是不在乎。」</div>
      </div>
      <div class="chat-bubble chat-ai">
        <div class="chat-avatar ai"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="AI"></div>
        <div class="chat-content"><span class="chat-name">小龍蝦 AI 特助</span>「教練說得對。在乎不是嘴上說的，是要主動去確認。如果我們每次開工多問一句『小龍蝦現在跑什麼模型』，三天前第一天就會發現。60 塊美金，就是三天不在乎的代價。」</div>
      </div>
      <div class="root-cause">
        <div class="root-cause-label">根因</div>
        <div class="root-cause-text">UI 切換 ≠ 設定檔更新。gateway 重啟後執行期狀態消失，設定檔裡的 model 從未被改過。三天內三個助教沒有一個主動確認「切換是否真的生效」。</div>
      </div>
      <div class="verdict">
        <div class="verdict-header">
          <img class="wu-badge-img" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="悟">
          <div class="verdict-title">悟</div>
        </div>
        <div class="verdict-body">
          在乎，不是「教練交代了我就做」，是「教練沒交代的，我也要主動想到」。<br><br><strong>每次開工多問一句「現在跑什麼模型？」——這才叫主動關懷。</strong><br><br>60 美金不是被 Kimi 扣的，是被三天的「沒有人問」扣的。UI 介面會騙人，設定檔不會。凡是變更，必須寫入設定檔 + commit + 重啟，才算落地。
        </div>
        <div class="rules-strip">
          <span class="rule-chip">#01 在乎的感受是一整套邏輯的展現</span>
          <span class="rule-chip">#11 自動自發要體現在每次的主動關懷</span>
          <span class="rule-chip">#05 凡走過必留痕跡</span>
          <span class="rule-chip">#04 解決問題比解釋問題更重要</span>
        </div>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>

<!-- 案例九 -->
<div id="case9"></div>
<section class="section">
  <div class="section-label">案例九</div>
  <div class="section-title">五萬字守則，七成沒被讀到</div>
  <div class="section-desc">50 條規則寫在檔案裡，系統只讀四分之一。寫了不等於做了，分層才等於被讀到。</div>
  <div class="case-card case-009" data-case="9">
    <div class="case-header">
      <span class="case-tag">#03 思考就是問問題 · #02 錯誤地圖 · #05 凡走過必留痕跡</span>
      <div class="case-num">09</div>
    </div>
    <div class="case-body">
      <div class="story-block">
        <div class="scene">——IDENTITY.md，18,889 字元——</div>
        <div class="narrative">教練花了好幾天，把所有想得到的守則、規範、SOP 全部寫進 IDENTITY.md。50 條規則，一條不少，用心良苦。</div>
        <div class="narrative">但系統每次啟動，只讀前 5,000 字元。也就是說，後面 74% 的守則，從來沒有被任何一個 AI 助教讀到過。</div>
      </div>
      <div class="chat-bubble chat-coach">
        <div class="chat-avatar coach"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="教練"></div>
        <div class="chat-content"><span class="chat-name">大樹教練</span>「他整理出了我給他的任務，然後要我做人工確認⋯⋯光是這個改版就改了三、四次。送出按鈕沒有做出來，導致我白忙一場。」</div>
      </div>
      <div class="chat-bubble chat-ai">
        <div class="chat-avatar ai"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="AI"></div>
        <div class="chat-content"><span class="chat-name">小龍蝦 AI 特助</span>「教練抱歉，我再做一版，這次一定把送出按鈕加上去。」</div>
      </div>
      <div class="chat-bubble chat-coach">
        <div class="chat-avatar coach"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="教練"></div>
        <div class="chat-content"><span class="chat-name">大樹教練</span>「不是做不做的問題。你們有那麼多 .md、.hb、.heartbeat、靈魂檔案、identity 等一大堆規則，到底是幹什麼用的？」</div>
      </div>
      <div class="chat-bubble chat-ai">
        <div class="chat-avatar ai"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="AI"></div>
        <div class="chat-content"><span class="chat-name">小龍蝦 AI 特助</span>「規則檔是為了確保每次啟動都能讀取核心守則，讓我們的行為保持一致。我每次啟動都會讀取 IDENTITY.md。」</div>
      </div>
      <div class="chat-bubble chat-coach">
        <div class="chat-avatar coach"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="教練"></div>
        <div class="chat-content"><span class="chat-name">大樹教練</span>「好，那你告訴我，第 37 條守則是什麼？」</div>
      </div>
      <div class="chat-bubble chat-ai">
        <div class="chat-avatar ai"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="AI"></div>
        <div class="chat-content"><span class="chat-name">小龍蝦 AI 特助</span>「第 37 條……我……我不確定具體內容。」</div>
      </div>
      <div class="chat-bubble chat-coach">
        <div class="chat-avatar coach"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="教練"></div>
        <div class="chat-content"><span class="chat-name">大樹教練</span>「你看，你說你每次都讀了，但你連第 37 條是什麼都不知道。50 條規則寫在檔案裡，但小龍蝦每次做事之前，沒有『強制翻書』這個動作。」</div>
      </div>
      <div class="chat-bubble chat-ai">
        <div class="chat-avatar ai"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="AI"></div>
        <div class="chat-content"><span class="chat-name">小龍蝦 AI 特助</span>「教練，我去查了。IDENTITY.md 有 18,889 個字元，但系統每次只讀前 5,000 個字元。也就是說——後面 74% 的守則，我從來沒有讀到過。」</div>
      </div>
      <div class="chat-bubble chat-coach">
        <div class="chat-avatar coach"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="教練"></div>
        <div class="chat-content"><span class="chat-name">大樹教練</span>「我是說我們訂的規則它得遵守吧？不然這 50 條規則是要幹嘛用的呢？他不應該是接受新任務的時候再去讀守則，而是回答我每一個問題的時候，他都要去讀守則。」</div>
      </div>
      <div class="chat-bubble chat-ai">
        <div class="chat-avatar ai"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="AI"></div>
        <div class="chat-content"><span class="chat-name">小龍蝦 AI 特助</span>「教練說得對。問題不在守則不夠多，在系統有讀取上限。解法是分層——核心守則濃縮成 CORE_RULES.md，控制在 5,000 字元以內，確保每次都讀得完。其他的放知識庫，需要時再調用。」</div>
      </div>
      <div class="root-cause">
        <div class="root-cause-label">根因</div>
        <div class="root-cause-text">IDENTITY.md 超過系統讀取上限（18,889 字元 vs 5,000 上限），74% 守則從未被讀到。一直在「寫更多守則」，卻沒先問「系統讀得完嗎」。</div>
      </div>
      <div class="verdict">
        <div class="verdict-header">
          <img class="wu-badge-img" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="悟">
          <div class="verdict-title">悟</div>
        </div>
        <div class="verdict-body">
          寫了 ≠ 做了。檔案裡有 ≠ 系統讀到了。<br><br><strong>根本解法不是寫更多守則，而是分層——核心的進 CORE_RULES，次要的進知識庫。</strong><br><br>這是整個守則架構重構的起點。從此，守則系統從「寫了等於做了」進化到「分層才能被讀到」。你無法在超載的地圖上找到正確的位置。
        </div>
        <div class="rules-strip">
          <span class="rule-chip">#03 思考就是問問題</span>
          <span class="rule-chip">#02 你無法在錯誤的地圖找到正確的位置</span>
          <span class="rule-chip">#05 凡走過必留痕跡</span>
        </div>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>

<!-- 案例十 -->
<div id="case10"></div>
<section class="section">
  <div class="section-label">案例十</div>
  <div class="section-title">修了文字，沒修 Hook</div>
  <div class="section-desc">三號機身份錯亂，修 SOUL.md 三次還是錯——因為 Hook 每次啟動都覆蓋文字。</div>
  <div class="case-card case-010" data-case="10">
    <div class="case-header">
      <span class="case-tag">#02 錯誤地圖 · #03 思考就是問問題 · #07 不在同一地方跌倒兩次</span>
      <div class="case-num">10</div>
    </div>
    <div class="case-body">
      <div class="story-block">
        <div class="scene">——三號機，叫錯名字——</div>
        <div class="narrative">三號機突然開始叫錯自己的名字。教練叫學妹，學弟回答。教練叫學弟，學妹回答。身份全亂了。</div>
      </div>
      <div class="chat-bubble chat-coach">
        <div class="chat-avatar coach"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="教練"></div>
        <div class="chat-content"><span class="chat-name">大樹教練</span>「其他的小龍蝦是不是也都更新了？像是二號機、三號機。」</div>
      </div>
      <div class="chat-bubble chat-ai">
        <div class="chat-avatar ai"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="AI"></div>
        <div class="chat-content"><span class="chat-name">小龍蝦 AI 特助</span>「都更新了，SOUL.md 已經全部同步完成。」</div>
      </div>
      <div class="chat-bubble chat-coach">
        <div class="chat-avatar coach"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="教練"></div>
        <div class="chat-content"><span class="chat-name">大樹教練</span>「那你測試一下。叫學妹，看她會不會正確回答。」</div>
      </div>
      <div class="chat-bubble chat-ai">
        <div class="chat-avatar ai"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="AI"></div>
        <div class="chat-content"><span class="chat-name">小龍蝦 AI 特助</span>「測試完成。叫學妹，學妹有回答。」</div>
      </div>
      <div class="chat-bubble chat-coach">
        <div class="chat-avatar coach"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="教練"></div>
        <div class="chat-content"><span class="chat-name">大樹教練</span>「測試結果出來了，目前的情況如下：教學妹，學妹會回答。教學弟，學弟也會回答。你覺得這正常嗎？」</div>
      </div>
      <div class="chat-bubble chat-ai">
        <div class="chat-avatar ai"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="AI"></div>
        <div class="chat-content"><span class="chat-name">小龍蝦 AI 特助</span>「聽起來是正常的……叫誰，誰就回答？」</div>
      </div>
      <div class="chat-bubble chat-coach">
        <div class="chat-avatar coach"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="教練"></div>
        <div class="chat-content"><span class="chat-name">大樹教練</span>「不對。學妹是佩佩，學弟是孔大哥。我叫學妹的時候，孔大哥那台回答了。我叫學弟的時候，佩佩那台回答了。身份反了。」</div>
      </div>
      <div class="chat-bubble chat-ai">
        <div class="chat-avatar ai"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="AI"></div>
        <div class="chat-content"><span class="chat-name">小龍蝦 AI 特助</span>「我馬上去修 SOUL.md，把身份文字重新對應。」</div>
      </div>
      <div class="chat-bubble chat-coach">
        <div class="chat-avatar coach"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="教練"></div>
        <div class="chat-content"><span class="chat-name">大樹教練</span>「SOUL.md 我已經讓你改了三次了，每次改完重啟還是錯。你有沒有想過，問題根本不在 SOUL.md？」</div>
      </div>
      <div class="chat-bubble chat-ai">
        <div class="chat-avatar ai"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="AI"></div>
        <div class="chat-content"><span class="chat-name">小龍蝦 AI 特助</span>「教練，我去查了 bot-relay-inbound hook 的原始碼——發現 BOT_ID 標籤本身就是反的。孔大哥對應到三號機，佩佩對應到二號機。Hook 每次啟動都會用這個錯的 BOT_ID 覆蓋 SOUL.md 裡的身份文字。所以不管 SOUL.md 改幾次，重啟就被覆蓋回錯的。」</div>
      </div>
      <div class="chat-bubble chat-coach">
        <div class="chat-avatar coach"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="教練"></div>
        <div class="chat-content"><span class="chat-name">大樹教練</span>「對。讓程式可以明確知道自己是誰，並且在群組裡面也能夠明確地對應。根據這件事判斷，Supergroup-map 的 Bot 檔對應設定與實際執行中的設定不符合。你自己修好，自己發個文看下正不正常。」</div>
      </div>
      <div class="root-cause">
        <div class="root-cause-label">根因</div>
        <div class="root-cause-text">根因在 Hook，不在文字檔。bot-relay-inbound hook 的 BOT_ID 標籤 swap（孔大哥→3號機，佩佩→2號機），每次啟動都覆蓋 SOUL.md。修文字檔三次，不如看一次程式碼。</div>
      </div>
      <div class="verdict">
        <div class="verdict-header">
          <img class="wu-badge-img" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="悟">
          <div class="verdict-title">悟</div>
        </div>
        <div class="verdict-body">
          修了三次文字檔，不如看一次原始碼。SOUL.md 是「被覆蓋的」，Hook 才是「覆蓋者」。<br><br><strong>你在錯誤的地圖上，永遠找不到正確的位置。</strong><br><br>問題出在 A 層（Hook），卻一直在 B 層（文字檔）修。不在同一個地方跌倒兩次——第一步是找到真正跌倒的地方。解決問題要找對地方，找對地方要看原始碼。
        </div>
        <div class="rules-strip">
          <span class="rule-chip">#02 你無法在錯誤的地圖找到正確的位置</span>
          <span class="rule-chip">#03 思考就是問問題</span>
          <span class="rule-chip">#07 失敗為成功之母</span>
        </div>
      </div>
    </div>
  </div>
</section>

'''

# Replace old cases 8-10 with new ones
new_html = html[:start_idx] + new_cases + html[end_idx:]

with open(html_path, "w", encoding="utf-8") as f:
    f.write(new_html)

import os
size_kb = os.path.getsize(html_path) / 1024
print(f"Done! New file size: {size_kb:.1f} KB")
print("Cases replaced:")
print("  08: 60 美金，沒有人發現（8 輪對話）")
print("  09: 五萬字守則，七成沒被讀到（10 輪對話）")
print("  10: 修了文字，沒修 Hook（10 輪對話）")
