import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.write("박스오피스 10위권 영화 데이터를 기반으로 장르 분포 및 관계를 시각화합니다.")

# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # genre 열 전처리 (첫 번째 장르만 extraction)
    if 'genre' in df.columns:
        df['genre'] = df['genre'].astype(str).apply(lambda x: x.split('|')[0] if '|' in x else x)
        
    return df

df = load_data()

# --- 첫 번째 그래프: 장르별 영화 편수 (도넛 차트) ---
st.subheader("1. 장르별 영화 편수 분포")

# 장르별 영화 편수 집계
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['장르', '영화 수']

# 플롯리 도넛 그래프 생성
fig_donut = px.pie(
    genre_counts,
    names='장르',
    values='영화 수',
    hole=0.4,
    title="장르별 영화 비율",
    hover_data=['영화 수']
)

# 마우스 호버 시 편수와 비율이 모두 표시되도록 설정
fig_donut.update_traces(
    textinfo='percent+label',
    hovertemplate="<b>장르:</b> %{label}<br><b>영화 수:</b> %{value}편<br><b>비율:</b> %{percent}"
)

st.plotly_chart(fig_donut, use_container_width=True)

# 그래프 해석 구역
st.markdown("---")
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("개봉한 주요 영화들 중 특정 장르(예: 드라마, 액션 등)가 차지하는 비중과 다빈도 개봉 장르를 한눈에 파악할 수 있습니다.")
st.markdown("---")
