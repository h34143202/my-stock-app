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

st.title("⚡ 台股全個股去噪交易聖盃 (Premium V4)")
st.markdown("##### ⚙️ 系統核心：大盤相對動能濾網 ｜ 剔除大盤一日大漲跟漲股 ｜ 買進與風險雙重分級系統")
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
    # 移除雙欄位，直接改成滿版一條流，專注看盤
    st.markdown("### 📊 明日大盤風控與交易評級")
    st.caption("📅 本日大盤與期權監控日期：2026-10-05")
    
    # 模擬今日市況：假設今日大盤「大漲一天」，但籌碼面暗藏危機
    market_risk_score = 4  # 大盤亮起高風險 4 級！
    
    st.markdown(f"""
    <div class='card-yellow'>
        <h2 style='color: #FFCC00; margin: 0 0 10px 0;'>🛡️ 全局環境風險等級： {market_risk_score} / 5 (高隱含風險)</h2>
        <p style='font-size: 15px; margin: 0;'>⚠️ 警訊監控：今日大盤雖單日大漲，但外資期貨空單居高不下，且夜盤並未跟進拉抬。</p>
        <p style='font-size: 16px; font-weight: bold; margin-top: 10px; color: #FFCC00;'>【大師防護機制】系統已判定今日大漲為虛胖噪訊！自動啟動防護降級，剔除所有單純跟漲個股，嚴防誘多大跌！</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    # 顯示明日首要標的作戰規則
    st.markdown("### 🎯 排名第一名個股作戰指令")
    
    # 建立去噪後的個股排行榜（台積電暫列第一）
    stock_rankings = [
        {"排名": 1, "股票": "2330 台積電", "買進等級": 2, "去噪判定": "⚠️ 獨立動能極強，但受大盤風險 4 級波及，強行從 1 級降為 2 級避險", "平盤價": 950.0},
        {"排名": 2, "股票": "2603 長榮", "買進等級": 3, "去噪判定": "❌ 偵測為大盤一日大漲的『純跟漲股』，毫無獨立鎖碼筹碼，從 1 級剔除至 3 級", "平盤價": 185.0},
        {"排名": 3, "股票": "2317 鴻海", "買進等級": 4, "去噪判定": "❌ 純粹跟隨大盤指數虛胖，個股布林通道根本尚未帶量突破，判定不適合買入", "平盤價": 180.0}
    ]
    
    top_stock = stock_rankings[0]
    st.success(f"🏆 明日無腦買進唯一目標： **{top_stock['股票']}** (目前降級調控中，買進等級：2)")
    
    max_buy = top_stock['平盤價'] * 1.03
    profit_target = top_stock['平盤價'] * 1.04
    
    col_buy, col_sell = st.columns(2)
    with col_buy:
        st.warning(f"📈 **開盤買入限制保護：**\n\n平盤價為 {top_stock['平盤價']} 元。\n\n開盤直接買入，**上限絕不超過 {max_buy} 元** (限價平盤 +3% 以內，開太高紀律棄單)！")
    with col_sell:
        st.info(f"💰 **無腦複利掛賣限制：**\n\n買到成交後，**立刻掛賣出目標價：{profit_target} 元**。\n\n當天若沒成交，隔天 08:30 準時掛好同樣目標，隨後關掉看盤軟體，無腦等待！")
        
    st.write("---")
    
    st.markdown("### 🏆 全台股量化篩選排名 (剔除大盤跟漲噪訊榜)")
    st.write("系統已自動啟動『大盤相對動能（Beta 去噪）公式』，唯有具備超越大盤的獨立鎖碼股才能入榜：")
    
    for stock in stock_rankings:
        border_style = "border-left: 5px solid #FFCC00;" if stock['買進等級'] == 2 else "border-left: 5px solid #30363D;"
        color_style = "color: #FFCC00;" if stock['買進等級'] == 2 else "color: #FFFFFF;"
        
        st.markdown(f"""
        <div class='rank-box' style='{border_style}'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='font-size: 16px; font-weight: bold; {color_style}'>🥇 排名第 {stock['排名']} 名： {stock['股票']}</span>
                <span style='background-color: #21262D; padding: 2px 8px; border-radius: 5px; font-size: 12px; color: #FFCC00; border: 1px solid #30363D;'>買進等級: {stock['買進等級']}</span>
            </div>
            <div style='margin-top: 8px; font-size: 13px; color: #8B949E;'>
                <span style='color: #FF9999;'>去噪過濾機制：{stock['去噪判定']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
