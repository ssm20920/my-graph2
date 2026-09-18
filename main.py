import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")

# 데이터 불러오기
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    # 장르(genre)가 세로막대 기호(|)로 분리되어 있는 경우 첫 번째 장르만 추출
    df['genre'] = df['genre'].astype(str).str.split('|').str[0]
    return df

df = load_data()

st.divider()

# 1. 장르별 영화 편수 (도넛 그래프)
st.subheader("1. 장르별 영화 편수")

# 장르별 편수 집계
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['장르', '편수']

# Plotly 도넛 그래프 생성
fig_donut = px.pie(
    genre_counts,
    names='장르',
    values='편수',
    hole=0.4,
    title="장르별 영화 분포"
)

# 마우스오버 시 편수와 비율이 함께 표시되도록 설정
fig_donut.update_traces(
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}"
)

# 그래프 출력
st.plotly_chart(fig_donut, use_container_width=True)

# 시각화 해석 및 구역 분리
st.info("💡 **이 그래프로 알 수 있는 것:** 특정 장르에 박스오피스 상위권 영화가 얼마나 집중되어 있는지 비중을 한눈에 확인할 수 있습니다.")

st.divider()
