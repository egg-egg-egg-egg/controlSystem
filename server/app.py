import streamlit as st
from server.network import ServerNetwork
import cv2

def main():
    st.title("教室控制中心")
    
    # 初始化网络模块
    server = ServerNetwork()
    server.start_listening(handle_message)
    
    # 设备列表
    devices = st.sidebar.multiselect("选择设备", list(server.clients.keys()))
    
    # 实时画面展示
    if 'current_frame' in st.session_state:
        st.image(st.session_state.current_frame, 
                use_column_width=True,
                channels="BGR")

def handle_message(ip, data):
    if data['type'] == 'SCREENSHOT':
        frame = cv2.imdecode(np.frombuffer(data['frame'], np.uint8), 
                            cv2.IMREAD_COLOR)
        st.session_state.current_frame = frame