import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

# 제목
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

# 데이터 불러오기 함수
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # .str.split()을 사용하여 첫 번째 장르만 추출 (PyArrow 데이터 타입 문제 해결)
    df['genre'] = df['genre'].astype(str).str.split('|').str[0]
    
    return df
df = load_data()

# ---------------------------------------------------------
# 첫 번째 그래프: 장르별 영화 편수 (도넛 그래프)
# ---------------------------------------------------------
st.subheader("1. 장르별 영화 편수 분포")

# 장르별 편수 집계
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['장르', '편수']

# Plotly 도넛 그래프 생성
fig1 = px.pie(
    genre_counts, 
    names='장르', 
    values='편수', 
    hole=0.4,
    title="장르별 영화 편수"
)

# 마우스 호버 시 편수와 비율이 보이도록 설정
fig1.update_traces(
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}"
)

# 그래프 출력
st.plotly_chart(fig1, use_container_width=True)

# 그래프 설명 구역
st.info("**이 그래프로 알 수 있는 것:** 개봉한 박스오피스 상위 영화 중 어떤 장르가 가장 큰 비중을 차지하는지 한눈에 파악할 수 있습니다.")
