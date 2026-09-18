
import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")

# 제목
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

# 데이터 불러오기 및 전처리 함수
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # 장르 전처리: 세로막대 기호(|)로 여러 개 적힌 영화는 첫 번째 장르만 추출
    df['genre_first'] = df['genre'].astype(str).apply(lambda x: x.split('|')[0] if x else x)
    
    return df

df = load_data()

st.subheader("1. 장르별 영화 편수 분포")

# 장르별 영화 편수 집계
genre_counts = df['genre_first'].value_counts().reset_index()
genre_counts.columns = ['장르', '영화편수']

# Plotly 도넛 그래프 생성
fig = px.pie(
    genre_counts, 
    values='영화편수', 
    names='장르', 
    hole=0.4,
    title='장르별 영화 편수 비율'
)

# 마우스 호버 시 편수와 비율 표기 설정
fig.update_traces(
    textinfo='percent+label',
    hovertemplate='<b>장르</b>: %{label}<br><b>영화 편수</b>: %{value}편<br><b>비율</b>: %{percent}'
)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)

st.divider()

# 그래프 하단 구역 및 설명 문구 자리
st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("박스오피스 상위권에 진입한 영화 중 특정 장르가 차지하는 비중과 주요 인기 장르의 분포를 한눈에 확인할 수 있습니다.")
