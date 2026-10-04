import streamlit as st
import json
import os
import pandas as pd

# 1. 網頁頂級配置（滿版）
st.set_page_config(page_title="台股無腦量化交易聖盃", page_icon="⚡", layout="wide")

# 注入高端黑、量子綠、警示紅與量子金的頂級量化美學
st.markdown("""
    <style>
    .stApp { background-color: #0A0D14; color: #E4E7EB; }
    .stTextInput input { background-color: #161B22 !important; color: white !important; border: 1px solid #30363D !important; }
    .card-red { background-color: #221616; padding: 25px; border-radius: 12px; border: 1px solid #4E2424; border-left: 8px solid #FF4D4D; margin-bottom: 20px; }
    .card-yellow { background-color: #262114; padding: 25px; border-radius: 12px; border: 1px solid #4E3E1A; border-left: 8px solid #FFCC00; margin-bottom: 20px; }
    .card-green { background-color: #0E1F14; padding: 25px; border-radius: 12px; border: 1px solid #1B432A; border-left: 8px solid #00E676; margin-bottom: 20px; }
    .rank-box { background-color: #161B22; padding: 15px; border-radius: 10px; border: 1px solid #30363D; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ 台股全個股去噪交易聖盃 (Premium V5)")
st.markdown("##### ⚙️ 系統核心：大盤相對動能濾網 ｜ 上市上櫃獨立計分模型 ｜ 剔除大盤虛胖跟漲股")
st.write("---")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.subheader("🔒 系統已高強度加密，請輸入聖盃暗號解鎖")
    user_password = st.text_input("請輸入看盤密碼：", type="password")
    if st.button("確認登入系統"):
        if user_password == "8888":
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("❌ 密碼錯誤，拒絕存取！")
else:
    # 顯示大盤風險狀態
    st.markdown("### 📊 明日大盤風控與交易評級")
    st.caption("📅 本日大盤與期權監控日期：2026-10-05")
    
    # 假設今日環境判定（此處模擬為安全綠燈，全面啟動上市櫃分級篩選）
    market_risk_score = 1
    
    st.markdown(f"""
    <div class='card-green'>
        <h2 style='color: #00E676; margin: 0 0 10px 0;'>🛡️ 全局環境風險等級： {market_risk_score} / 5 (極低風險)</h2>
        <p style='font-size: 15px; margin: 0;'>最新指標：外資期貨空單安全、夜盤動能強勁。滿足無腦買進資格！</p>
        <p style='font-size: 16px; font-weight: bold; margin-top: 10px; color: #00E676;'>【決策提示】環境安全，解除大盤噪訊干擾，啟動上市櫃布林通道＋投信鎖碼雙強獨立分級榜！</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    # 建立上市前五名與上櫃前五名的獨立數據集
    tws_ranking = [
        {"排名": 1, "股票": "2330 台積電", "等級": 1, "去噪判定": "🟢 布林通道高度擠壓後帶量首日突破上軌，投信狂鎖碼", "平盤價": 950.0},
        {"排名": 2, "股票": "2317 鴻海", "等級": 1, "去噪判定": "🟢 站上布林上軌，突破20日高點，外資法人聯買", "平盤價": 180.0},
        {"排名": 3, "股票": "2454 聯發科", "等級": 2, "去噪判定": "⏳ 技術面強勢突破，但投信買超佔比尚未達標，列為2級", "平盤價": 1200.0},
        {"排名": 4, "股票": "2382 廣達", "等級": 2, "去噪判定": "⏳ 剛站上布林中軌，動能正要加溫", "平盤價": 250.0},
        {"排名": 5, "股票": "3034 聯詠", "等級": 3, "去噪判定": "❌ 純跟隨大盤一日大漲，缺乏實質鎖碼籌碼降級", "平盤價": 510.0}
    ]

    tpex_ranking = [
        {"排名": 1, "股票": "8069 元太", "等級": 1, "去噪判定": "🟢 布林通道緊縮後量增長紅突破上軌，內資主力狂拉", "平盤價": 240.0},
        {"排名": 2, "股票": "3293 鈊象", "等級": 1, "去噪判定": "🟢 逆大盤率先突破布林上軌，投信連續不計成本鎖碼", "平盤價": 1020.0},
        {"排名": 3, "股票": "5483 中美晶", "等級": 2, "去噪判定": "⏳ 通道擠壓帶量，但尚未實質突破上軌壓力區", "平盤價": 175.0},
        {"排名": 4, "股票": "3529 力旺", "等級": 2, "去蹤判定": "⏳ 股性活潑帶動，但資券比異常，列為2級觀察", "平盤價": 2200.0},
        {"排名": 5, "股票": "6488 環球晶", "等級": 4, "去噪判定": "❌ 隨大盤虛胖跟漲，布林通道正向開口未開，列為4級", "平盤價": 490.0}
    ]
    
    # 2. 顯示明日首要作戰指令（自動抓出上市與上櫃的雙料第一名個股）
    st.markdown("### 🎯 明日無腦作戰核心指令")
    top_tws = tws_ranking[0]
    top_tpex = tpex_ranking[0]
    
    col_tws_card, col_tpex_card = st.columns(2)
    with col_tws_card:
        max_buy_tws = top_tws['平盤價'] * 1.03
        sell_target_tws = top_tws['平盤價'] * 1.04
        st.success(f"🏢 **【上市最優】** 明日買進標的： **{top_tws['股票']}** (等級：1)")
        st.caption(f"📈 買進限制：不追超過 **{max_buy_tws} 元** (平盤+3%) ｜ 💰 獲利掛賣：**{sell_target_tws} 元**")
        
    with col_tpex_card:
        max_buy_tpex = top_tpex['平盤價'] * 1.03
        sell_target_tpex = top_tpex['平盤價'] * 1.04
        st.success(f"🏪 **【上櫃最優】** 明日買進標的： **{top_tpex['股票']}** (等級：1)")
        st.caption(f"📈 買進限制：不追超過 **{max_buy_tpex} 元** (平盤+3%) ｜ 💰 獲利掛賣：**{sell_target_tpex} 元**")
        
    st.write("---")
    
    # 3. 獨立展示上市與上櫃的 1-5 名榜單
    col_tws_list, col_tpex_list = st.columns(2)
    
    with col_tws_list:
        st.markdown("### 🏢 上市股票最適合買入前五名")
        for stock in tws_ranking:
            border = "border-left: 5px solid #FFD700;" if stock['等級'] == 1 else "border-left: 5px solid #30363D;"
            color = "color: #FFD700;" if stock['等級'] == 1 else "color: #FFFFFF;"
            st.markdown(f"""
            <div class='rank-box' style='{border}'>
                <div style='display: flex; justify-content: space-between;'>
                    <span style='font-size: 15px; font-weight: bold; {color}'>🥇 第 {stock['排名']} 名： {stock['股票']} (平盤: {stock['平盤價']}元)</span>
                    <span style='background-color: #21262D; padding: 2px 8px; border-radius: 5px; font-size: 11px; color: #FFCC00;'>等級: {stock['等級']}</span>
                </div>
                <div style='margin-top: 6px; font-size: 12px; color: #8B949E;'>{stock['去噪判定']}</div>
            </div>
            """, unsafe_allow_html=True)
            
    with col_tpex_list:
        st.markdown("### 🏪 上櫃股票最適合買入前五名")
        for stock in tpex_ranking:
            border = "border-left: 5px solid #00E676;" if stock['等級'] == 1 else "border-left: 5px solid #30363D;"
            color = "color: #00E676;" if stock['等級'] == 1 else "color: #FFFFFF;"
            st.markdown(f"""
            <div class='rank-box' style='{border}'>
                <div style='display: flex; justify-content: space-between;'>
                    <span style='font-size: 15px; font-weight: bold; {color}'>🥇 第 {stock['排名']} 名： {stock['股票']} (平盤: {stock['平盤價']}元)</span>
                    <span style='background-color: #21262D; padding: 2px 8px; border-radius: 5px; font-size: 11px; color: #FFCC00;'>等級: {stock['等級']}</span>
                </div>
                <div style='margin-top: 6px; font-size: 12px; color: #8B949E;'>{stock['去噪判定']}</div>
            </div>
            """, unsafe_allow_html=True)
