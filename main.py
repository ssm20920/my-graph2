import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide"
)

# 제목
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")


# 데이터 불러오기 및 전처리 함수
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # 장르 전처리: '|' 구분 기호가 있는 경우 첫 번째 장르만 추출
    df["genre"] = df["genre"].fillna("기타").astype(str)
    df["genre"] = df["genre"].apply(lambda x: x.split("|")[0].strip())

    return df


# 데이터 로드
df = load_data()

# -------------------------------------------------------------------
# [첫 번째 그래프] 장르별 영화 편수 (도넛 차트)
# -------------------------------------------------------------------
st.header("1. 장르별 영화 분포")

# 장르별 편수 집계
genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

# Plotly 도넛 차트 생성
fig = px.pie(
    genre_counts,
    values="count",
    names="genre",
    hole=0.4,
    title="장르별 영화 편수 비율",
)

# 마우스오버 시 편수와 비율이 보이도록 설정
fig.update_traces(
    textinfo="percent+label", hovertemplate="<b>장르: %{label}</b><br>편수: %{value}편<br>비율: %{percent}"
)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)

# 구분선 및 이 그래프로 알 수 있는 것 구역
st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("박스오피스 상위권에 진입한 영화 중 특정 장르가 차지하는 비중과 주요 장르의 편수 분포를 확인할 수 있습니다.")
