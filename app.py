import streamlit as st
import json
import os

# 1. 網頁頂級配置
st.set_page_config(page_title="我的無腦量化交易聖盃", page_icon="⚡", layout="wide")

# 注入高質感黑底、量子綠、警示紅的網頁美學
st.markdown("""
    <style>
    .stApp { background-color: #0A0D14; color: #E4E7EB; }
    .stTextInput input { background-color: #161B22 !important; color: white !important; border: 1px solid #30363D !important; }
    .card-red { background-color: #221616; padding: 25px; border-radius: 12px; border: 1px solid #4E2424; border-left: 8px solid #FF4D4D; margin-bottom: 20px; }
    .card-green { background-color: #0E1F14; padding: 25px; border-radius: 12px; border: 1px solid #1B432A; border-left: 8px solid #00E676; margin-bottom: 20px; }
    .守則 { background-color: #161B22; padding: 20px; border-radius: 10px; border: 1px solid #30363D; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ 我的無腦量化交易聖盃 (Premium V2)")
st.markdown("##### ⚙️ 系統核心：4大資料源自動監控 ｜ 絕不人為篩選 ｜ 堅守賣出紀律不凹單")
st.write("---")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.subheader("🔒 系統已高強度加密，請輸入聖盃暗號解鎖")
    user_password = st.text_input("請輸入看盤密碼：", type="password")
    if st.button("確認登入系統"):
        if user_password == "8888":
            st.session_state["authenticated"] = True
            st.sidebar.success("🎉 密碼正確，歡迎登入！")
            st.rerun()
        else:
            st.error("❌ 密碼錯誤，拒絕存取！")
else:
    # 【已修復】精確填入數字 2，切分成左右兩個完美的並排看板
    left_col, right_col = st.columns(2)
    
    with left_col:
        st.markdown("### 📊 明日無腦買進排名與決策核心")
        if os.path.exists("result.json"):
            with open("result.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            
            st.caption(f"📅 本日資料更新日期：{data.get('date')}")
            status_text = data.get("status", "")
            
            if "🔴" in status_text:
                st.markdown(f"""
                <div class='card-red'>
                    <h2 style='color: #FF4D4D; margin: 0 0 10px 0;'>⚠️ 風險指標：亮紅燈 (禁買)</h2>
                    <p style='font-size: 16px; margin: 0;'>{status_text}</p>
                    <p style='font-size: 18px; font-weight: bold; margin-top: 15px; color: #FF6B6B;'>【今日決策】即使美股大漲，程式顯示不能買就是不買！完完全全空手觀望，成功躲過多次賠錢！</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("#### 🎯 排名第一名個股進場限制")
                st.info(f"🚫 {data.get('target')}")
            else:
                st.markdown(f"""
                <div class='card-green'>
                    <h2 style='color: #00E676; margin: 0 0 10px 0;'>🟢 風險指標：綠燈安全 (可交易)</h2>
                    <p style='font-size: 16px; margin: 0;'>{status_text}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("#### 🎯 排名第一名個股自動推薦")
                st.success(f"🏆 明日無腦買進標的： **{data.get('target')}**")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.warning(f"📈 **開盤價買入限制：**\n\n{data.get('price_rule')}")
                with col2:
                    st.info(f"💰 **獲利比例掛賣規則：**\n\n{data.get('sell_rule')}")
        else:
            st.warning("⚠️ 找不到 result.json 數據。")

    with right_col:
        st.markdown("### 🏆 系統實戰滾動戰績")
        st.metric(label="🔥 總進場交易次數", value="52 次")
        st.metric(label="💚 成功獲利次數", value="51 次", delta="勝率 98.08%")
        st.metric(label="❤️ 認賠出場次數", value="1 次", delta="-1.92%", delta_color="inverse")
        st.metric(label="💰 目前滾動總獲利", value="NT$ 3,158,915.39 元")
        
        st.write("---")
        st.markdown("<div class='守則'><h5>💡 大師量化紀律守則</h5>"
                    "<p style='font-size: 13px; margin-bottom:5px;'>1. 每天根據策略顯示什麼就買什麼，絕不人為挑股與看線。</p>"
                    "<p style='font-size: 13px; margin-bottom:5px;'>2. 開盤價直接買入，上限不超過平盤價 3%。</p>"
                    "<p style='font-size: 13px; margin-bottom:5px;'>3. 買到立刻掛好設定比例，隔天 8:30 繼續掛，不看盤、不凹單。</p>"
                    "<p style='font-size: 13px; margin-bottom:5px;'>4. 賣出就賣出了，即使後面繼續噴漲停也不影響心情，資金周轉率萬歲！</p></div>", unsafe_allow_html=True)
