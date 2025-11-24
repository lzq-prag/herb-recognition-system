# 中草药识别系统（Herb Recognition System）

**作者**：骆泽权
**学号**：102300423


## 项目简介
本项目是一个基于 Python + Streamlit + 百度 AI 图像识别 API 开发的中草药智能识别工具，支持通过上传图片快速识别常见中草药种类，输出识别结果、置信度及相关百科信息，无需复杂配置，开箱即用。

适合学生、中医药爱好者、相关从业者快速查询中草药信息，也可作为深度学习与 API 集成的实践案例参考。


## 核心功能
- **图片上传识别**：支持上传 JPG、PNG 格式的中草药图片（叶片、植株等清晰部位均可），自动调用百度 AI 植物识别接口分析；
- **精准识别结果**：返回中草药名称、识别置信度（可信度评分），确保识别结果的参考价值；
- **百科信息展示**：关联中草药的基础百科介绍（如性味、功效、用法等），辅助用户深入了解；
- **跨平台使用**：
  - 云端版：无需安装，通过浏览器直接访问（[在线使用链接](https://herb-recognition-system-jnmyuzsjebtfnqoa884atm.streamlit.app/)）；
  - 本地版：支持打包为 Windows 可执行文件（.exe），双击运行，无需配置 Python 环境。


## 技术栈
- 前端框架：Streamlit（快速构建交互式 Web 界面）
- 核心依赖：requests（API 请求）、Pillow（图片处理）
- 识别接口：百度 AI 开放平台 - 植物识别 API
- 部署平台：Streamlit Community Cloud
- 打包工具：PyInstaller（本地 .exe 生成）


## 使用方法
### 方式 1：在线使用
点击在线链接：[https://herb-recognition-system-jnmyuzsjebtfnqoa884atm.streamlit.app/](https://herb-recognition-system-jnmyuzsjebtfnqoa884atm.streamlit.app/)
- 点击「浏览文件」，上传清晰的中草药图片（建议单株、无过多遮挡）；
- 等待 1-2 秒，系统自动显示识别结果及相关信息。


### 方式 2：本地运行（需 Python 环境）
1. 克隆本仓库（复制以下命令到终端/命令行执行）：
   ```bash
   git clone https://github.com/lzq-prag/herb-recognition-system.git
   cd herb-recognition-system
2. 安装项目依赖：
  ```bash
pip install -r requirements.txt

3. 启动本地应用:
  ```bash
streamlit run herb_recognition.py

