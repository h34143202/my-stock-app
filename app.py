import json
import os
import pandas as pd
import streamlit as st

# 1. 網頁頂級配置（滿版）
st.set_page_config(page_title="台股無腦量化交易聖盃", page_icon="⚡", layout="wide")

# 注入高端黑、量子綠、警示紅與量子金的頂級量化美學
st.markdown(
    """
    <style>
    .stApp { background-color: #0A0D14; color: #E4E7EB; }
    .stTextInput input { background-color: #161B22 !important; color: white !important; border: 1px solid #30363D !important; }
    .card-red { background-color: #221616; padding: 25px; border-radius: 12px; border: 1px solid #4E2424; border-left: 8px solid #FF4D4D; margin-bottom: 20px; }
    .card-yellow { background-color: #262114; padding: 25px; border-radius: 12px; border: 1px solid #4E3E1A; border-left: 8px solid #FFCC00; margin-bottom: 20px; }
    .card-green { background-color: #0E1F14; padding: 25px; border-radius: 12px; border: 1px solid #1B432A; border-left: 8px solid #00E676; margin-bottom: 20px; }
    .metric-box { background-color: #161B22; padding: 15px; border-radius: 10px; border: 1px solid #30363D; text-align: center; }
    .rank-box { background-color: #161B22; padding: 15px; border-radius: 10px; border: 1px solid #30363D; margin-bottom: 10px; }
    .rules-box { background-color: #11141A; padding: 15px; border-radius: 8px; border: 1px solid #1F242E; margin-bottom: 20px; }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("⚡ 台股全個股動態回測交易聖盃 (Premium V6)")
st.markdown(
    "##### ⚙️ 系統核心：上市櫃獨立動態回測 ｜ 隔夜高點套利勝率 ｜ 雙軌5MA防護與收盤前15分鐘硬停損機制"
)
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
    # 讀取數據安全檢查
    if os.path.exists("real_report.json"):
        with open("real_report.json", "r", encoding="utf-8") as f:
            report = json.load(f)
    else:
        # 內建防呆安全氣囊數據，確保檔案同步延遲時也能順暢開機
        report = {
            "date": "2026-10-05 (今日實戰初始日)",
            "market_risk": 1,
            "risk_desc": "最新指標安全，大盤環境穩定",
            "backtest_summary": {
                "tws_prev_stock": "等待明日開盤進場...",
                "tws_today_move": 0.00,
                "tws_total_trades": 0,
                "tws_win_rate": 0.00,
                "tws_stop_loss_count": 0,
                "tpex_prev_stock": "等待明日開盤進場...",
                "tpex_today_move": 0.00,
                "tpex_total_trades": 0,
                "tpex_win_rate": 0.00,
                "tpex_stop_loss_count": 0,
            },
            "tws_rank 5": [
                {
                    "股票": "2330 台積電",
                    "等級": 1,
                    "去噪判定": "🟢 終極聖盃股：布林首日突破 ＋ 投信鎖碼 ＋ 關鍵主力15日異常囤貨完勝！",
                    "平盤價": 950.0,
                }
            ],
            "tpex_rank 5": [
                {
                    "股票": "8069 元太",
                    "等級": 1,
                    "去噪判定": "🟢 終極聖盃股：布林首日突破 ＋ 投信鎖碼 ＋ 關鍵主力15日異常囤貨完勝！",
                    "平盤價": 240.0,
                }
            ],
        }

    # ==========================================
    # 🛡️ 操盤守則公告
    # ==========================================
    st.markdown(
        """
    <div class='rules-box'>
        <h5 style='color: #FFCC00; margin-top: 0;'>📝 隔夜高點套利與 13:15 尾盤洗盤停損守則</h5>
        <ul style='font-size: 13px; margin-bottom: 0; color: #B3B9C1;'>
            <li><b>進場紀律：</b> 前一天盤後選出標的，隔天早上 <b>08:30</b> 準時進場無腦掛單 <b>平盤價 +3% 內</b> 買入。</li>
            <li><b>出場停利：</b> 買到成交後一路抱過夜，於<b>再隔天的盤中最高點（高點）</b>由系統嘗試波段套利賣出。</li>
            <li><b>洗盤免疫停損：</b> 盤中震盪一律無視！只有到了<b>收盤前 15 分鐘（13:15 之後）</b>，若股價<b>依然死死跌破「買入價格 -4%」</b>，系統才執行紀律砍倉，拒絕被假跌破惡意洗出場！</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ==========================================
    # 🏆 核心看板：戰績統計
    # ==========================================
    st.markdown("### 📈 昨日第一名隔夜高點套利實測戰報 (天天自動對答案)")
    st.caption(f"📅 戰績統計截止日期：{report.get('date')}")

    backtest_data = report.get("backtest_summary", {})

    col_bt_tws, col_bt_tpex = st.columns(2)

    with col_bt_tws:
        st.markdown(
            f"<div class='metric-box' style='border-top: 4px solid #FFD700;'><span style='color: #FFD700; font-weight: bold;'>🏢 上市第一名隔夜回測結果</span><br><span style='font-size: 14px; color: #8B949E;'>昨日標的：{backtest_data.get('tws_prev_stock', '無')}</span><br><span style='font-size: 28px; font-weight: bold; color: #00E676;'>+{backtest_data.get('tws_today_move', 0.0)*100:.2f} %</span><div style='margin-top: 10px; display: flex; justify-content: space-around; font-size: 13px;'><span>📊 總測試天數: <b>{backtest_data.get('tws_total_trades', 0)} 天</b></span><span>🎯 高點套利勝率: <b style='color: #FFD700;'>{backtest_data.get('tws_win_rate', 0.0):.2f} %</b></span><span>🚨 尾盤確破停損: <b style='color: #FF4D4D;'>{backtest_data.get('tws_stop_loss_count', 0)} 次</b></span></div></div>",
            unsafe_allow_html=True,
        )

    with col_bt_tpex:
        st.markdown(
            f"<div class='metric-box' style='border-top: 4px solid #00E676;'><span style='color: #00E676; font-weight: bold;'>🏪 上櫃第一名隔夜回測結果</span><br><span style='font-size: 14px; color: #8B949E;'>昨日標的：{backtest_data.get('tpex_prev_stock', '無')}</span><br><span style='font-size: 28px; font-weight: bold; color: #00E676;'>+{backtest_data.get('tpex_today_move', 0.0)*100:.2f} %</span><div style='margin-top: 10px; display: flex; justify-content: space-around; font-size: 13px;'><span>📊 總測試天數: <b>{backtest_data.get('tpex_total_trades', 0)} 天</b></span><span>🎯 高點套利勝率: <b style='color: #00E676;'>{backtest_data.get('tpex_win_rate', 0.0):.2f} %</b></span><span>🚨 尾盤確破停損: <b style='color: #FF4D4D;'>{backtest_data.get('tpex_stop_loss_count', 0)} 次</b></span></div></div>",
            unsafe_allow_html=True,
        )

    st.write("---")

    # 大盤風險狀態
    st.markdown("### 📊 明日大盤風控與交易評級")
    risk_score = report.get("market_risk", 1)
    risk_desc = report.get("risk_desc", "")

    if risk_score >= 4:
        st.markdown(
            f"<div class='card-red'><h2 style='color: #FF4D4D; margin: 0 0 10px 0;'>🛡️ 全局環境風險等級： {risk_score} / 5 (高隱含風險)</h2><p style='font-size: 15px; margin: 0;'>⚠️ 警訊監控：{risk_desc}</p><p style='font-size: 16px; font-weight: bold; margin-top: 10px; color: #FF4D4D;'>【大師防護機制】系統已判定今日大漲為虛胖噪訊！自動啟動防護降級，剔除所有單純跟漲個股，嚴防誘多大跌！</p></div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div class='card-green'><h2 style='color: #00E676; margin: 0 0 10px 0;'>🛡️ 全局環境風險等級： {risk_score} / 5 (極低風險)</h2><p style='font-size: 15px; margin: 0;'>最新指標：{risk_desc}。滿足無腦買進資格！</p></div>",
            unsafe_allow_html=True,
        )

    st.write("---")

    # 明日首要作戰指令
    st.markdown("### 🎯 明日無腦作戰核心指令")
    tws_ranking = report.get("tws_rank 5", [])
    tpex_ranking = report.get("tpex_rank 5", [])

    top_tws = (
        tws_ranking
        if tws_ranking
        else {"股票": "無符合標的", "平盤價": 0.0, "等級": 5}
    )
    top_stock_tpex = (
        tpex_ranking
        if tpex_ranking
        else {"股票": "無符合標的", "平盤價": 0.0, "等級": 5}
    )

    col_tws_card, col_tpex_card = st.columns(2)
    with col_tws_card:
        if top_tws.get("平盤價", 0.0) > 0 and top_tws.get("等級", 5) <= 2:
            max_buy_tws = top_tws["平盤價"] * 1.03
            st.success(
                f"🏢 **【上市最優】** 明日買進標的： **{top_tws['股票']}** (等級：{top_tws['等級']})"
            )
            st.markdown(
                f"⏱️ **買進限制：** 08:30 掛單，不追超過 **{max_buy_tws:.1f} 元** (+3%內買入) ｜ 🛑 **尾盤硬停損：** 13:15 之後若依然跌破 **-4%** 執行砍倉！"
            )
        else:
            st.error("🏢 **【上市最優】** 今日無符合大師去噪條件之上市個股，紀律空手觀望！")

    with col_tpex_card:
        if (
            top_stock_tpex.get("平盤價", 0.0) > 0
            and top_stock_tpex.get("等級", 5) <= 2
        ):
            max_buy_pex = top_stock_tpex["平盤價"] * 1.03
            st.success(
                f"🏪 **【上櫃最優】** 明日買進標的： **{top_stock_tpex['股票']}** (等級：{top_stock_tpex['等級']})"
            )
            st.markdown(
                f"⏱️ **買進限制：** 08:30 掛單，不追超過 **{max_buy_pex:.1f} 元** (+3%內買入) ｜ 🛑 **尾盤硬停損：** 13:15 之後若依然跌破 **-4%** 執行砍倉！"
            )
        else:
            st.error("🏪 **【上櫃最優】** 今日無符合大師去噪條件之上櫃個股，紀律空手觀望！")

    st.write("---")

    # 展示上市與上櫃前五名 (【已修復】改用純單行代碼渲染，徹底終結括號漏字漏洞)
    col_tws_list, col_tpex_list = st.columns(2)

    with col_tws_list:
        st.markdown("### 🏢 上市股票最適合買入前五名")
        for idx, stock in enumerate(tws_ranking):
            border = "border-left: 5px solid #FFD700;" if stock.get("等級", 5) <= 2 and stock.get("平盤價", 0.0) > 0 else "border-left: 5px solid #30363D;"
            color = "color: #FFD700;" if stock.get("等級", 5) <= 2 and stock.get("平盤價", 0.0) > 0 else "color: #FFFFFF;"
            st.markdown(f"<div class='rank-box' style='{border}'><div style='display: flex; justify-content: space-between;'><span style='font-size: 15px; font-weight: bold; {color}'>🥇 第 {idx+1} 名： {stock.get('股票', '無')} (平盤: {stock.get('平盤價', 0.0)}元)</span><span style='background-color: #21262D; padding: 2px 8px; border-radius: 5px; font-size: 11px; color: #FFCC00;'>等級: {stock.get('等級', 5)}</span></div><div style='margin-top: 6px; font-size: 12px; color: #8B949E;'>{stock.get('去噪判定', '無')}</div></div>", unsafe_allow_html=True)

    with col_tpex_list:
        st.markdown("### 🏪 上櫃股票最適合買入前五名")
        for idx, stock in enumerate(tpex_ranking):
            border = "border-left: 5px solid #00E676;" if stock.get("等級", 5) <= 2 and stock.get("平盤價", 0.0) > 0 else "border-left: 5px solid #30363D;"
            color = "color: #00E676;" if stock.get("等級", 5) <= 2 and stock.get("平盤價", 0.0) > 0 else "color: #FFFFFF;"
