import streamlit as st
from server.network import ServerNetwork
import cv2
import numpy as np



def main():
    st.title("教室控制中心")
    
    if "serverNetwork" not in st.session_state:
        try:
            st.session_state.serverNetwork = server = ServerNetwork(8848)
            # 初始化网络模块
            server.start_listening(handle_message)
        except OSError as e:
            st.error(f"服务器启动失败: {e}. 请检查端口是否被占用或更换端口后重试。")
            return
    else:
        server = st.session_state.serverNetwork
    # 设备列表
    devices = st.sidebar.multiselect("选择设备", list(server.clients.keys()))
    
    # 实时画面展示
    if 'current_frame' in st.session_state:
        st.image(st.session_state.current_frame, 
                use_column_width=True,
                channels="BGR")

def handle_message(ip, data):
    if data['type'] == 'SCREENSHOT':
        try:
            frame = cv2.imdecode(np.frombuffer(data['data'], np.uint8), 
                                 cv2.IMREAD_COLOR)
            st.session_state.current_frame = frame
            st.write(f"Received screenshot from {ip}")
        except Exception as e:
            st.error(f"处理截图数据时出错: {e}")


if __name__ == "__main__":
    main()