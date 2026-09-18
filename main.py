import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # 장르 전처리
    df['genre'] = df['genre'].astype(str).str.split('|').str[0]
    
    # 영화명과 코드를 조합하여 계층 중복(ValueError) 방지용 고유 레이블 생성
    df['movie_label'] = df['movieNm'] + " (" + df['movieCd'].astype(str) + ")"
    
    return df

df = load_data()

# 1. 도넛 그래프 (생략 - 기존 동일)
st.subheader("1. 장르별 영화 편수 분포")
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['장르', '편수']

fig1 = px.pie(
    genre_counts, 
    names='장르', 
    values='편수', 
    hole=0.4,
    title="장르별 영화 편수"
)
fig1.update_traces(
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}"
)
st.plotly_chart(fig1, use_container_width=True)
st.info("**이 그래프로 알 수 있는 것:** 개봉한 박스오피스 상위 영화 중 어떤 장르가 가장 큰 비중을 차지하는지 한눈에 파악할 수 있습니다.")

st.markdown("---")

# ---------------------------------------------------------
# 2. 트리맵 그래프 (오류 수정 반영)
# ---------------------------------------------------------
st.subheader("2. 장르별 영화 관객 수 분포 (트리맵)")

fig2 = px.treemap(
    df,
    path=['genre', 'movie_label'],  # 고유 식별 레이블 사용
    values='total_audi',
    color='genre',
    custom_data=['movieNm'],        # 마우스 호버에 원래 영화명 전달
    title="장르 및 영화별 총 관객 수"
)

# 마우스 호버 시 순수 영화명과 관객 수만 표시
fig2.update_traces(
    hovertemplate="<b>%{customdata[0]}</b><br>총 관객 수: %{value:,}명"
)

st.plotly_chart(fig2, use_container_width=True)
st.info("**이 그래프로 알 수 있는 것:** 각 장르가 전체 관객 수에서 차지하는 비중과, 장르 내에서 흥행을 주도한 개별 영화의 스케일을 동시에 확인할 수 있습니다.")
