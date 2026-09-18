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
    
    # 결측치 및 중복 제거
    df = df.dropna(subset=['genre', 'movieNm', 'movieCd', 'total_audi', 'first_scrn', 'first_week_audi', 'nation', 'days_in_top10']).copy()
    df = df.drop_duplicates(subset=['movieCd']).copy()
    
    # 장르 전처리 (첫 번째 장르만 사용)
    df['genre'] = df['genre'].astype(str).str.split('|').str[0]
    
    # 트리맵용 고유 식별 레이블
    df['movie_label'] = df['movieNm'] + " (" + df['movieCd'].astype(str) + ")"
    
    return df

# 데이터 불러오기
df = load_data()

# ---------------------------------------------------------
# 1. 10위권에 든 영화의 장르 구성은 어떠한가? (도넛 차트)
# ---------------------------------------------------------
st.subheader("1. 10위권에 든 영화의 장르 구성은 어떠한가?")

genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['장르', '편수']

top_genres = genre_counts.iloc[:5]
other_count = genre_counts.iloc[5:]['편수'].sum()
if other_count > 0:
    other_row = pd.DataFrame([{'장르': '기타', '편수': other_count}])
    genre_counts_clean = pd.concat([top_genres, other_row], ignore_index=True)
else:
    genre_counts_clean = top_genres

fig1 = px.pie(
    genre_counts_clean, 
    names='장르', 
    values='편수', 
    hole=0.4,
    title="10위권 진입 영화의 장르별 구성 비율"
)
fig1.update_traces(
    textposition='inside',
    textinfo='percent+label',
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}"
)

st.plotly_chart(fig1, use_container_width=True)
st.info("**이 그래프로 알 수 있는 것:** 특정 상위 장르들이 10위권 진입 영화 시장의 과반수 이상을 차지하고 있음을 알 수 있습니다.")

st.markdown("---")

# ---------------------------------------------------------
# 2. 각 장르 안에서 어떤 영화가 가장 큰 관객을 동원했을까? (트리맵)
# ---------------------------------------------------------
st.subheader("2. 각 장르 안에서 어떤 영화가 가장 큰 관객을 동원했을까?")

fig2 = px.treemap(
    df,
    path=['genre', 'movie_label'],
    values='total_audi',
    color='genre',
    custom_data=['movieNm'],
    title="장르 및 개별 영화별 총 관객 수"
)

fig2.update_traces(
    hovertemplate="<b>%{customdata[0]}</b><br>총 관객 수: %{value:,}명"
)

st.plotly_chart(fig2, use_container_width=True)
st.info("**이 그래프로 알 수 있는 것:** 각 장르 영역 안에서 가장 큰 사각형을 차지하고 있는 영화를 확인하여, 해당 장르의 흥행을 주도한 대표 영화가 무엇인지 바로 비교할 수 있습니다.")
