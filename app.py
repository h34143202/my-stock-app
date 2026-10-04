
import streamlit as st
import json
import os

# 1. 設定網頁標題與酷炫黑底外觀
st.set_page_config(page_title="大師無腦量化聖盃", page_icon="📊", layout="centered")

# 使用 CSS 強制注入科技感深色模式
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    .stTextInput input {
        background-color: #262730 !important;
        color: white !important;
    }
    .metric-box {
        background-color: #1A1C23;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #2D3139;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 我的無腦量化交易聖盃")
st.write("---")

# 2. 安全防護：設定密碼檢查
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.subheader("🔒 系統已加密，請輸入密碼解鎖")
    user_password = st.text_input("請輸入看盤密碼：", type="password")
    
    if st.button("確認登入"):
        if user_password == "8888":  # 大師的專屬密碼
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("❌ 密碼錯誤，拒絕存取！")
else:
    # 3. 密碼正確，讀取步驟 2 留下來的 json 小盒子
    if os.path.exists("result.json"):
        with open("result.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            
        st.sidebar.success("✅ 數據載入成功")
        st.sidebar.write(f"📅 數據更新日期：{data.get('date')}")
        
        # 4. 根據紅綠燈狀態，渲染出不同的震撼視覺效果
        status_text = data.get("status", "")
        
        if "🔴" in status_text:
            # 紅燈警戒狀態
            st.markdown(f"""
            <div class='metric-box' style='border-left: 8px solid #FF4B4B;'>
                <h2 style='color: #FF4B4B; margin-top:0;'>⚠️ 風險指標：紅燈警報</h2>
                <p style='font-size: 18px;'>{status_text}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.error("🚨 紀律高於一切！今日請嚴格執行空手，不進行任何買入操作。")
            
        else:
            # 綠燈安全狀態
            st.markdown(f"""
            <div class='metric-box' style='border-left: 8px solid #00E676;'>
                <h2 style='color: #00E676; margin-top:0;'>✅ 風險指標：綠燈安全</h2>
                <p style='font-size: 18px;'>{status_text}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 秀出明日操作標的
            st.markdown("### 🎯 明日無腦買進目標")
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="🏆 策略排名第一名個股", value=data.get("target"))
            with col2:
                st.metric(label="💰 買進價格限制", value=data.get("price_rule"))
                
            st.info("💡 紀律提示：開盤價直接買入，買到後立刻掛好設定好的波段目標價賣出。")
            
    else:
        st.warning("⚠️ 找不到數據小盒子 (result.json)，請先執行步驟 1 與步驟 2 的程式碼！")
