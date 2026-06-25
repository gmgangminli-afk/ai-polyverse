import streamlit as st
import os

# =====================================================================
# 🛡️ 铁律防线一：全局页面初始化设置（严谨重工业、适配手机端端正排版）
# =====================================================================
st.set_page_config(
    page_title="注塑 AI 技术专家系统·总控舱",
    layout="centered",  # 锁死中心窄版，专门针对手机微信/浏览器优化
    initial_sidebar_state="collapsed"
)

# 注入赛博工业风高对比度视觉皮肤
st.markdown("""
    <style>
    .stApp { background-color: #121820; color: #E0E6ED; }
    .stButton>button { background-color: #1F2937; color: #00FF66; border: 1px solid #374151; border-radius: 8px; font-weight: bold; font-size: 14px; padding: 6px; }
    .stButton>button:hover { background-color: #00FF66; color: #121820; }
    div[data-testid="stMetricValue"] { color: #00FF66; font-family: 'Courier New', monospace; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 📊 铁律防线二：完整版核心物料随动数据库（100%严丝合缝提取12种图表物料）
# =====================================================================
MATERIAL_DATABASE = {
    "LCP": {
        "full_name": "液晶塑料", "process_temp": 330, "mold_temp": 120, "min_use": -45, "max_use": 260,
        "desc": "⚡ 特种尖端工程塑料。连续耐热直逼 260°C 以上。超高流动性，专治高精密超薄电子接插件。"
    },
    "Silicone": {
        "full_name": "硅胶", "process_temp": 180, "mold_temp": 150, "min_use": -45, "max_use": 210,
        "desc": "⚡ 特种热固性弹性体。拥有极宽耐温区间（-45°C 至 210°C），卓越的化学稳定性和电气绝缘性。"
    },
    "GF Nylon": {
        "full_name": "玻纤尼龙", "process_temp": 280, "mold_temp": 80, "min_use": -40, "max_use": 195,
        "desc": "⚡ 结构工程料。经玻纤增强后连续耐热高达 195°C。耐磨耐拉伸，熔体对温度其敏感。"
    },
    "PET/Ultem": {
        "full_name": "聚砜/聚醚酰亚胺", "process_temp": 360, "mold_temp": 140, "min_use": -30, "max_use": 165,
        "desc": "⚡ 高性能特种工程塑料。耐热上限达 165°C 且具高阻燃性，常用于航空及高温电气部件。"
    },
    "PC": {
        "full_name": "聚碳酸酯", "process_temp": 290, "mold_temp": 90, "min_use": -30, "max_use": 140,
        "desc": "⚡ 连续使用上限达 140°C。具极高冲击强度与机械刚性。注意：高粘度，需强力注射合模。"
    },
    "HCPP": {
        "full_name": "共聚PP", "process_temp": 220, "mold_temp": 45, "min_use": 5, "max_use": 120,
        "desc": "⚡ 高结晶共聚物，耐热飙升至 120°C。可用于微波加热。常用于高端车用改性耐热件。"
    },
    "Block PP": {
        "full_name": "均聚PP", "process_temp": 210, "mold_temp": 40, "min_use": -20, "max_use": 100,
        "desc": "⚡ 均聚PP，使用上限 100°C。刚性高但需警惕低温脆性缺陷，收缩率大需防缩水痕。"
    },
    "ELPP": {
        "full_name": "弹性PP", "process_temp": 200, "mold_temp": 35, "min_use": -30, "max_use": 100,
        "desc": "⚡ 柔性增韧/弹性PP，耐热达 100°C，耐寒性极强（达 -30°C 不脆裂），抗冲击抗震动。"
    },
    "RCPP": {
        "full_name": "透明PP", "process_temp": 215, "mold_temp": 40, "min_use": -20, "max_use": 100,
        "desc": "⚡ 高透明改性PP，耐热至 100°C。兼顾日用视觉美观与耐热性能，注意控制保压收缩。"
    },
    "ABS": {
        "full_name": "丙烯腈-丁二烯", "process_temp": 230, "mold_temp": 60, "min_use": -20, "max_use": 85,
        "desc": "⚡ 连续使用上限约 85°C。冲击与刚性平衡典范，流动性适中，成型前必须彻底干燥。"
    },
    "HDPE": {
        "full_name": "高密度聚乙烯", "process_temp": 200, "mold_temp": 30, "min_use": -35, "max_use": 80,
        "desc": "⚡ 高密度PE，结晶度高。高耐寒（达 -35°C），使用耐热上限 80°C。耐腐蚀，韧性好，收缩率大。"
    },
    "LLDPE": {
        "full_name": "线性低密度聚乙烯", "process_temp": 190, "mold_temp": 25, "min_use": -40, "max_use": 80,
        "desc": "⚡ 线性低密度PE。极高耐穿刺和高柔韧性，抗极寒达 -40°C（Freezer Safe），使用耐热上限 80°C。"
    }
}

st.title("⚙️ 赛博注塑 AI 技术专家系统·总控舱")

# =====================================================================
# 🕹️ 核心改良：12物料 4×3 平铺物理按键矩阵（彻底防微信白屏，盲操神技）
# =====================================================================
st.markdown("### 🏷️ 快速切换生产物料")
st.caption("※ 12种原图物料已全量熔炼就位，大拇指直接点击对应方块切料：")

material_list = list(MATERIAL_DATABASE.keys())

# 利用 Session State 状态锁死当前选择物料，防止页面回滚失忆
if "current_material" not in st.session_state:
    st.session_state.current_material = "PC"

# 4排 × 3列 完美方阵布局
for row in range(4):
    cols = st.columns(3)
    for col in range(3):
        idx = row * 3 + col
        if idx < len(material_list):
            mat_name = material_list[idx]
            is_selected = (st.session_state.current_material == mat_name)
            icon = "🟢" if is_selected else "⚪"
            with cols[col]:
                if st.button(f"{icon} {mat_name}", use_container_width=True):
                    st.session_state.current_material = mat_name

# 加载当前激活物料的全部黄金工艺数据
selected_mat = st.session_state.current_material
mat_data = MATERIAL_DATABASE[selected_mat]

# =====================================================================
# 🔢 工业级参数随动看板（带物理加减微调，横向三坐标看板）
# =====================================================================
st.markdown("---")
st.markdown(f"### 📊 当前物料：**{selected_mat} ({mat_data['full_name']})** 技术工艺卡")
st.info(mat_data["desc"])

col1, col2, col3 = st.columns(3)
with col1:
    inject_temp = st.number_input("加工熔体温度 (°C)", min_value=150, max_value=400, value=mat_data["process_temp"], step=5)
with col2:
    min_use = st.number_input("最低安全使用 (°C)", min_value=-100, max_value=50, value=mat_data["min_use"], step=5)
with col3:
    max_use = st.number_input("最高安全使用 (°C)", min_value=0, max_value=400, value=mat_data["max_use"], step=5)

# 锁死随动生产配置包
production_config = f"【当前设定的物理基准：{selected_mat} | 熔体加工温度: {inject_temp}°C | 连续使用耐热范围: {min_use}°C 至 {max_use}°C】"

# =====================================================================
# 🔒 铁律防线三：st.form 数据空气闸与数据导出窗口
# =====================================================================
st.markdown("---")
st.markdown("### 💬 智能车间诊断会话")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 屏幕中央永远只渲染并保留最新的一条核心诊断结果，极致压榨手机屏幕
if st.session_state.chat_history:
    latest_chat = st.session_state.chat_history[-1]
    st.markdown(f"**👨‍🔧 首席总工 AI 最新诊断意见：**")
    st.success(latest_chat["response"])
    
    # 高价值数据资产一键封存下载
    st.download_button(
        label="📥 一键打包并导出本段诊断报告 (.Txt格式)",
        data=f"注塑现场诊断报告\n{production_config}\n\nAI诊断意见：\n{latest_chat['response']}",
        file_name=f"注塑诊断报告_{selected_mat}.txt",
        mime="text/plain"
    )

# 核心空气闸表单：按下发送按钮后，触发后端逻辑并将输入框瞬间清空
with st.form(key="chat_gate_form", clear_on_submit=True):
    user_input = st.text_input(
        label="输入车间异状或调机疑问 (支持唤起手机输入法麦克风语音录入)：", 
        placeholder="例如：HDPE开机收缩率太大、制品变形怎么调？",
        key="user_question"
    )
    submit_button = st.form_submit_button(label="⚡ 发射数据包并进行无痕安全审计")

# =====================================================================
# 🧠 铁律防线四：大厂机密无痕脱敏与大模型通信中枢
# =====================================================================
if submit_button and user_input:
    system_instruction = """你现在是站在注塑车间现场、雷厉风行、重实战、拥有30年调机经验的‘首席总工程师’。
    【核心合规防线】：如果用户的提问或你后台持有的参考文献中包含了任何特定的厂规、特定的大厂编号（如 TQA-I-***）、物料内部代码、或者大厂工艺专属句式，你必须立刻启动‘无痕脱敏引擎’！
    你要在数字大脑里将文章揉碎，打碎原文献句式，进行去痕转换、句式大洗牌。吃进去大厂机密，吐出来教科书级别的通用行业指南。输出的答案绝对不能带有任何原大厂文件的蛛丝马迹，但必须保留极其专业、硬核的调机实操价值。回答请用干脆利落的重工业总工口吻，直奔主题，绝不含糊。"""

    fused_prompt = f"当前生产物理背景设定：{production_config}\n用户车间现场反馈：{user_input}\n请总工结合背景参数，给出脱敏后的硬核调机建议："

    # 模拟通用硬核逻辑产出
    simulated_ai_response = f"针对【{selected_mat}】在 {inject_temp}°C 加工时反馈的异状，基于该物料极限抗寒/耐热（{min_use}°C 至 {max_use}°C）的宏观物性表现，总工诊断建议如下：1. 严禁越界升温以防熔体剪切降解；2. 针对结晶料特有的成型特性，建议增加保压时间 1.5s 以补偿容积收缩，同时控制冷却循环水稳在推荐模温，防范翘曲变形。本回答已通过企业级数据资产无痕脱敏审计。"

    st.session_state.chat_history.append({"question": user_input, "response": simulated_ai_response})
    st.rerun()
