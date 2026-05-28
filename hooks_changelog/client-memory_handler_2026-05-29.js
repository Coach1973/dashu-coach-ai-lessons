"use strict";

const fs = require('fs');
const path = require('path');

const OPENCLAW_DIR = path.resolve(__dirname, '../../');
const PROFILE_PATH = path.join(OPENCLAW_DIR, 'workspace', 'CLIENT_PROFILE.md');
const HEARTBEAT_PATH = path.join(OPENCLAW_DIR, 'workspace', 'HEARTBEAT.md');
const TEAM_IDENTITY_PATH = path.join(OPENCLAW_DIR, 'workspace', 'TEAM_IDENTITY.md');
const MEDIA_BASE_URL = 'https://media.bymyway.com';
const COUNTER_PATH = path.join(OPENCLAW_DIR, 'workspace', 'state', 'session_counter.json');

function getSessionCounter() {
  try {
    const dir = path.dirname(COUNTER_PATH);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    if (!fs.existsSync(COUNTER_PATH)) return { round: 0, bootstrapTime: new Date().toISOString() };
    return JSON.parse(fs.readFileSync(COUNTER_PATH, 'utf-8'));
  } catch (e) {
    return { round: 0, bootstrapTime: new Date().toISOString() };
  }
}

function resetSessionCounter() {
  try {
    const dir = path.dirname(COUNTER_PATH);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(COUNTER_PATH, JSON.stringify({
      round: 0,
      bootstrapTime: new Date().toISOString()
    }));
  } catch (e) {}
}

const handler = async (event) => {
  if (!event || typeof event !== 'object') return;
  if (event.type !== 'agent' || event.action !== 'bootstrap') return;
  if (!event.context || typeof event.context !== 'object') return;

  if (!event.context.inject) event.context.inject = [];
  if (!Array.isArray(event.context.inject)) return;

  // 重置本次 session 的輪次計數器
  resetSessionCounter();

  try {
    // 注入 LINE 媒體公開 URL 規則
    const mediaBlock = [
      '---',
      '# 📡 LINE 媒體傳送規則（自動注入）',
      `> 本機媒體目錄 \`~/.openclaw/media/\` 已透過靜態伺服器公開在 ${MEDIA_BASE_URL}`,
      '>',
      '> **重要**：透過 LINE 發送圖片、音樂、影片時，必須將本機路徑轉換為公開 URL。',
      '> 轉換規則：',
      '> - `/Users/bymyway/.openclaw/media/X` → `' + MEDIA_BASE_URL + '/X`',
      '> - `~/.openclaw/media/X` → `' + MEDIA_BASE_URL + '/X`',
      '>',
      '> 範例：`/Users/bymyway/.openclaw/media/tool-image-generation/image-xxx.png`',
      '> → `' + MEDIA_BASE_URL + '/tool-image-generation/image-xxx.png`',
      '>',
      '> 呼叫 message 工具時，media 參數請填入公開 URL 而非本機路徑。',
      '---',
    ].join('\n');
    event.context.inject.unshift({ role: 'system', content: mediaBlock });
  } catch (err) {}

  try {
    // 注入 TEAM_IDENTITY.md（守則 — 最高優先，放最前面）
    if (fs.existsSync(TEAM_IDENTITY_PATH)) {
      const tiContent = fs.readFileSync(TEAM_IDENTITY_PATH, 'utf-8');
      if (tiContent.trim()) {
        const block = [
          '---',
          '# 📋 頂級特助守則（TEAM_IDENTITY — 自動注入）',
          '> 以下是你必須遵守的完整守則，適用於所有頻道（Telegram / LINE）。',
          '',
          tiContent,
          '---',
        ].join('\n');
        event.context.inject.unshift({ role: 'system', content: block });
      }
    }
  } catch (err) {}

  try {
    // 注入 CLIENT_PROFILE.md（瘦身版 2026-05-29）
    // 舊行為：全文 ~13.6KB 全塞 → 開工就吃掉大半 context；多為 cron 雜訊蒸餾。
    // 新行為：只塞檔首最新 3500 字（≈最近 1-2 天蒸餾），其餘提示 agent 自行讀檔。
    if (fs.existsSync(PROFILE_PATH)) {
      const profileContent = fs.readFileSync(PROFILE_PATH, 'utf-8');
      if (profileContent.trim()) {
        const MAX = 3500;
        const truncated = profileContent.length > MAX;
        const body = truncated ? profileContent.slice(0, MAX) : profileContent;
        const tail = truncated
          ? `\n\n…（已截斷，完整檔在 \`~/.openclaw/workspace/CLIENT_PROFILE.md\`，需要更早期蒸餾自行讀取）`
          : '';
        const block = [
          '---',
          '# 📋 用戶記憶檔案（CLIENT_PROFILE — 最新摘要）',
          '> 以下是這位用戶最近的對話蒸餾，請在整個對話中牢記。',
          '',
          body + tail,
          '---',
        ].join('\n');
        event.context.inject.unshift({ role: 'system', content: block });
      }
    }
  } catch (err) {}

  try {
    // 注入 HEARTBEAT.md（當前任務狀態 — 最高優先）
    if (fs.existsSync(HEARTBEAT_PATH)) {
      const hbContent = fs.readFileSync(HEARTBEAT_PATH, 'utf-8');
      if (hbContent.trim()) {
        const now = new Date().toLocaleString('zh-TW', { timeZone: 'Asia/Taipei' });
        const block = [
          '---',
          '# 🚨 系統啟動上下文（HEARTBEAT — 自動注入）',
          `> 本次 Session 啟動時間：${now}`,
          '> ⚠️ 這是新的 Session。以下是你上次的工作狀態，請立即同步並告知教練你已重啟。',
          '',
          hbContent,
          '---',
        ].join('\n');
        // 放在最前面，確保是第一條讀到的 system 訊息
        event.context.inject.unshift({ role: 'system', content: block });
      }
    }
  } catch (err) {}
};

module.exports = handler;
module.exports.default = handler;
