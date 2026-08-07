---
name: bni-official-brand-colors
description: BNI官方品牌標準色號(2020年6月版Brand Standards Manual)，bni-chapters系統及任何BNI相關網頁往後一律使用
metadata: 
  node_type: memory
  type: reference
  originSessionId: 25e0b432-4aad-4393-8880-950d3cea007c
  modified: 2026-08-07T22:23:46.158Z
---

# BNI官方品牌色（2020-06 Brand Standards Manual 第6頁，教練2026-08-08指定）

| 色名 | Hex | RGB | CMYK | Pantone |
|------|-----|-----|------|---------|
| **BNI Red**（主色） | `#CF2030` | 207,32,48 | 12,100,90,3 | 186 |
| Sterling Grey（次色） | `#C8C8C8` | 200,200,200 | 20,15,15,0 | Cool Grey 3 |
| True White | `#FFFFFF` | 255,255,255 | 0,0,0,0 | — |
| **Power Black** | `#000000` | 0,0,0 | 0,0,0,100 | Process Black |
| Granite Grey | `#64666A` | 100,102,106 | 60,50,45,20 | Cool Grey 10 |
| Sterling Light Grey | `#F2F2F2` | 244,244,244 | 3,3,3,0 | Cool Grey 3/20%不透明 |

來源PDF：`https://www2.bni.com/rs/166-SUM-744/images/BNI%20Brand%20Standards%20Manual.pdf`

## Why
2026-08-08教練檢視真誠分會頁面，質疑hero區塊的黑色（`#2A2829`，自訂暖調深炭黑）是不是BNI標準色——查證後確認不是，`bni-chapters`系統原本的`--red:#A22026`跟`--ink:#2A2829`兩色都不是官方色號，是先前建置時自訂的。教練裁示「全部套用，並且之後一定要用官方指定色系」。

## How to apply
1. `bni-chapters`(`github_repos/bni-chapters`)已改用官方色（commit `958eea2`）：`--red:#CF2030`、`--ink:#000000`，色彩變數集中在共用模板`templates/base.html`的`:root`，改一處9分會同步生效（改完記得`launchctl kickstart -k gui/$(id -u)/com.coach.bni-chapters-webapp`重啟，Flask非debug模式模板不會自動reload）
2. 往後任何BNI相關網頁（含未來新分會、BNI Connect相關頁面）配色，一律先對照這張表，不用自訂色號或憑印象猜
3. 若需要hover/深色變體，從官方色計算（例：`--red-dark:#9B1F27`是`#CF2030`調暗約25%），不是另外發明一個新顏色
4. `--sub`/`--line`/`--gold`等非品牌色（次要文字、邊框、裝飾金色）本次沒動，教練指令範圍是「黑+紅」這兩個核心品牌色

Related: [[project_bni_chapters_public_launch_2026-08-03]]
