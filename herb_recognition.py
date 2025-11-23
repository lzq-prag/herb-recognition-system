import streamlit as st
import requests
import base64
import json

# -------------------------- 添加浅色背景与基础美化 --------------------------
def add_light_background():
    st.markdown("""
    <style>
        /* 浅色主题背景（柔和米色+淡绿，自然不刺眼） */
        .stApp {
            background-color: #faf6ed; /* 浅米色底色 */
        }
        
        /* 标题颜色优化（淡绿色系，贴合中草药主题） */
        h1 {
            color: #2d6a4f !important;
            margin-bottom: 10px !important;
        }
        
        h2 {
            color: #40916c !important;
            margin-top: 20px !important;
            margin-bottom: 15px !important;
        }
        
        /* 按钮美化（淡绿色，hover反馈） */
        .stButton > button {
            background-color: #74c69d;
            color: white;
            border-radius: 8px;
            border: none;
            transition: all 0.2s ease;
        }
        
        .stButton > button:hover {
            background-color: #52b788;
            transform: translateY(-1px);
        }
        
        /* 文本颜色优化（深色更易读） */
        .stWrite {
            color: #334155;
            font-size: 15px;
        }
        
        /* 上传组件提示文字 */
        .upload-hint {
            color: #64748b;
            font-size: 14px;
            margin-top: 8px;
        }
    </style>
    """, unsafe_allow_html=True)

# -------------------------- 配置AI接口信息 --------------------------
API_KEY = "BH8y25lbrmxePGVGY2WCVcRP" 
SECRET_KEY = "BvHGiG5Zu7uucpFpT6xaQ5bOdu64tCpE" 
TOKEN_URL = "https://aip.baidubce.com/oauth/2.0/token"  # 获取访问令牌的URL
DETECT_URL = "https://aip.baidubce.com/rest/2.0/image-classify/v1/plant"  # 植物识别接口

# -------------------------- 工具函数 --------------------------
@st.cache_data(ttl=3600)  # 缓存Token，1小时有效（避免重复获取）
def get_access_token():
    """获取百度AI接口的访问令牌"""
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY
    }
    response = requests.get(TOKEN_URL, params=params)
    result = response.json()
    if "access_token" in result:
        return result["access_token"]
    else:
        st.error(f"获取Token失败：{result}")
        return None

def image_to_base64(image_file):
    """将上传的图片文件转为Base64编码（AI接口要求的格式）"""
    return base64.b64encode(image_file.read()).decode("utf-8")

def call_plant_ai_api(image_base64, access_token):
    """调用百度AI植物识别接口，获取中草药信息"""
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "image": image_base64,
        "top_num": 3,  # 返回Top3识别结果（提高准确率）
        "baike_num": 1  # 要求返回百科信息（保留有效字段）
    }
    url = f"{DETECT_URL}?access_token={access_token}"
    response = requests.post(url, headers=headers, data=data)
    return response.json()

# -------------------------- 前端界面与逻辑 --------------------------
def main():
    # 加载浅色背景样式
    add_light_background()
    
    # 页面标题（带中草药图标，左对齐）
    st.title("🌿 中草药识别系统")
    st.subheader("上传图片，快速识别中草药名称及相关信息", divider="green")  # 加绿色分隔线更协调
    
    # 1. 前端图片上传组件（左对齐，优化提示文字）
    uploaded_file = st.file_uploader(
        "选择一张中草药图片（建议清晰拍摄叶片/全株）", 
        type=["jpg", "jpeg", "png"],
        help="支持JPG、JPEG、PNG格式，图片越清晰识别越准确"
    )
    st.markdown('<p class="upload-hint">💡 提示：尽量拍摄无遮挡、光线充足的中草药图片</p>', unsafe_allow_html=True)
    
    if uploaded_file:
        # 显示上传的图片（左对齐，添加圆角边框）
        st.image(uploaded_file, caption="上传的图片", use_column_width=False, width=400)  # 不占满列宽，左对齐显示
        
        # 2. 点击识别按钮触发后端逻辑（左对齐显示按钮）
        if st.button("开始识别", type="primary"):
            with st.spinner("🔍 识别中... 请稍候"):
                # 3. 步骤1：获取AI接口Token
                access_token = get_access_token()
                if not access_token:
                    return
                
                # 4. 步骤2：图片转Base64
                image_base64 = image_to_base64(uploaded_file)
                
                # 5. 步骤3：调用AI接口
                ai_result = call_plant_ai_api(image_base64, access_token)
                
                # 6. 步骤4：解析并展示结果（全部左对齐）
                if "result" in ai_result and len(ai_result["result"]) > 0:
                    # 取置信度最高的结果
                    top_result = ai_result["result"][0]
                    st.success(f"✅ 识别成功！最可能的中草药：{top_result['name']}", icon="✅")
                    
                    # 显示核心信息（名称+置信度，左对齐）
                    st.subheader("📊 核心识别结果")
                    st.write(f"**名称**：{top_result['name']}")
                    st.write(f"**识别置信度**：{round(top_result['score'] * 100, 2)}%")
                    
                    # 只展示百度接口实际返回的有效百科信息（无数据则不显示，左对齐）
                    if "baike_info" in top_result and top_result["baike_info"]:
                        baike = top_result["baike_info"]
                        st.subheader("📝 百度百科相关信息")
                        
                        # 有哪个字段就显示哪个，没有就跳过
                        if baike.get("property"):  # 性味归经（有数据才显示）
                            st.write(f"**性味归经**：{baike['property']}")
                        if baike.get("function"):  # 功效主治（有数据才显示）
                            st.write(f"**功效主治**：{baike['function']}")
                        if baike.get("growth_env"):  # 生长环境（有数据才显示）
                            st.write(f"**生长环境**：{baike['growth_env']}")
                        if baike.get("morphology"):  # 形态特征（有数据才显示）
                            st.write(f"**形态特征**：{baike['morphology']}")
                        if baike.get("baike_url"):  # 百科链接（有数据才显示）
                            st.markdown(f"[🔗 查看完整百度百科]({baike['baike_url']})", unsafe_allow_html=True)
                    
                    # 显示其他候选结果（可选，左对齐）
                    if len(ai_result["result"]) > 1:
                        st.subheader("🔍 其他可能的识别结果")
                        for i, res in enumerate(ai_result["result"][1:], 2):
                            st.write(f"{i}. {res['name']}（置信度：{round(res['score'] * 100, 2)}%）")
                else:
                    st.error(f"❌ 识别失败！原因：{ai_result.get('error_msg', '未返回有效结果')}", icon="❌")

if __name__ == "__main__":
    main()