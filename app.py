import streamlit as st
import pandas as pd

# [화면 설정]
st.set_page_config(page_title="그린 키오스크 엔진", layout="wide")

# --- [배경 스타일 정의] ---
# 탄소 배출량에 따라 배경의 밝기나 색상을 조절하는 CSS입니다.
def set_background(pollution_level):
    # pollution_level: 0(맑음) ~ 100(탁함)
    darkness = pollution_level * 0.5  # 수치가 높을수록 어두워짐
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(to bottom, 
                rgba(135, 206, 235, {1 - (pollution_level/100)}) 0%, 
                rgba(105, 105, 105, {pollution_level/100}) 50%, 
                #8FBC8F 100%);
            background-size: cover;
        }}
        /* 아래쪽에 마을 느낌을 주기 위한 가상 요소 */
        .stApp::after {{
            content: "🏡🏘️🌳";
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 50px;
        }}
        </style>
        """, unsafe_allow_name=True)

# --- [조원들 함수 배치 구역] ---

# 1번 조원: 키오스크 사진에서 메뉴 추출
def extract_menu_from_kiosk(image):
    # 예: ['빅맥 세트', '치즈버거 세트', '불고기버거'] 리스트 반환
    return ["소고기 버거", "콩고기 버거", "콜라", "감자튀김"]

# 2번 조원: 탄소 배출량 계산 (두 메뉴 비교용)
def get_carbon_score(menu_name):
    # 품목별 탄소 배출량 데이터베이스 연결
    db = {"소고기 버거": 15.0, "콩고기 버거": 2.5, "콜라": 0.5, "감자튀김": 0.8}
    return db.get(menu_name, 1.0)

# --- [4번 프론트엔드 메인 화면] ---

def main():
    st.title("🍔 그린 키오스크: 메뉴 비교 엔진")
    
    # 기본은 맑은 배경 (0)
    pollution = 0
    
    # 1. 키오스크 사진 업로드
    uploaded_file = st.file_uploader("키오스크 화면을 촬영해 주세요", type=['jpg', 'png'])
    
    if uploaded_file:
        menu_list = extract_menu_from_kiosk(uploaded_file)
        st.info(f"📍 인식된 메뉴: {', '.join(menu_list)}")
        
        st.divider()
        st.subheader("⚖️ 어떤 메뉴가 지구에 더 좋을까요?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            option_a = st.selectbox("메뉴 A 선택", menu_list, index=0)
            score_a = get_carbon_score(option_a)
            st.metric(f"{option_a}의 탄소량", f"{score_a} kg")
            
        with col2:
            option_b = st.selectbox("메뉴 B 선택", menu_list, index=1)
            score_b = get_carbon_score(option_b)
            st.metric(f"{option_b}의 탄소량", f"{score_b} kg")

        # 비교 결과 도출
        saving = score_a - score_b
        
        if st.button("결과 확인 및 환경 변화 보기"):
            if saving > 0:
                st.success(f"✅ {option_b}를 선택하면 {option_a}보다 {abs(saving)}kg의 탄소를 줄일 수 있습니다!")
                pollution = 20  # 상대적으로 깨끗함
            else:
                st.warning(f"⚠️ {option_a}가 {option_b}보다 {abs(saving)}kg 더 친환경적입니다.")
                pollution = 70  # 배출량이 많으면 하늘이 탁해짐
                
            # 배경 업데이트
            set_background(pollution)
            
            # 리워드 포인트 (3번 조원 기능 연결)
            points = int(abs(saving) * 100) if saving > 0 else 0
            st.sidebar.metric("획득 예정 리워드", f"{points} P")

    else:
        set_background(0) # 사진 없으면 맑은 하늘

if __name__ == "__main__":
    main()
