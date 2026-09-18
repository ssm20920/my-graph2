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

genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

fig1 = px.pie(
    genre_counts,
    values="count",
    names="genre",
    hole=0.4,
    title="장르별 영화 편수 비율",
)
fig1.update_traces(
    textinfo="percent+label",
    hovertemplate="<b>장르: %{label}</b><br>편수: %{value}편<br>비율: %{percent}",
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.write(
    "박스오피스 상위권에 진입한 영화 중 특정 장르가 차지하는 비중과 주요 장르의 편수 분포를 확인할 수 있습니다."
)

st.markdown("<br><br>", unsafe_allow_html=True)

# -------------------------------------------------------------------
# [두 번째 그래프] 장르별/영화별 총 관객 수 (트리맵)
# -------------------------------------------------------------------
st.header("2. 장르 및 영화별 총 관객 수")

fig2 = px.treemap(
    df,
    path=[px.Constant("전체 영화"), "genre", "movieNm"],
    values="total_audi",
    title="장르 및 영화별 총 관객 수 분포",
)
fig2.update_traces(
    hovertemplate="<b>영화명: %{label}</b><br>총 관객 수: %{value:,.0f}명"
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.write(
    "장르별 전체 흥행 규모뿐만 아니라, 각 장르 내에서 어떤 영화가 전체 관객 수의 얼마만큼을 차지하는지 한눈에 비교할 수 있습니다."
)

st.markdown("<br><br>", unsafe_allow_html=True)

# -------------------------------------------------------------------
# [세 번째 그래프] 총 관객 수 분포 (히스토그램)
# -------------------------------------------------------------------
st.header("3. 총 관객 수 분포")

fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    title="영화별 총 관객 수 빈도 분포",
    labels={"total_audi": "총 관객 수"},
)
fig3.update_traces(
    hovertemplate="<b>관객 수 구간: %{x}</b><br>영화 수: %{y}편"
)

st.plotly_chart(fig3, use_container_width=True)

# 최다 관객 영화 데이터 추출
top_movie = df.loc[df["total_audi"].idxmax()]
top_movie_name = top_movie["movieNm"]
top_movie_audi = top_movie["total_audi"]

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.markdown(
    f"""
- 대부분의 영화가 **하위 관객 수 구간(약 100만~300만 명 대)**에 밀집해 있는 오른쪽으로 긴 꼬리를 가진 양의 왜도(Positive Skewness) 분포를 보입니다.
- 데이터에서 가장 관객 수가 많은 최상위 흥행 영화는 **'{top_movie_name}'** (총 {top_movie_audi:,.0f}명)입니다.
"""
)

st.markdown("<br><br>", unsafe_allow_html=True)

# -------------------------------------------------------------------
# [네 번째 그래프] 개봉일 스크린 수 vs 총 관객 수 (산점도)
# -------------------------------------------------------------------
st.header("4. 개봉일 스크린 수와 총 관객 수의 관계")

fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린 수 대 총 관객 수 산점도",
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "genre": "장르",
    },
)
fig4.update_traces(
    hovertemplate="<b>영화명: %{hovertext}</b><br>개봉일 스크린 수: %{x:,}개<br>총 관객 수: %{y:,.0f}명"
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.write(
    "개봉일 스크린 수가 많을수록 대체로 높은 총 관객 수를 기록하는 양의 상관관계를 보여주며, 동일한 스크린 수 대비 관객 동원력이 뛰어난 흥행 우수작(상단 이상치) 및 장르별 분포 경향을 파악할 수 있습니다."
)

st.markdown("<br><br>", unsafe_allow_html=True)

# -------------------------------------------------------------------
# [다섯 번째 그래프] 주요 장르별 총 관객 수 분포 (박스플롯)
# -------------------------------------------------------------------
st.header("5. 주요 장르별 총 관객 수 분포 (영화 10편 이상 장르)")

# 영화 수 10편 이상인 장르만 필터링
genre_counts_series = df["genre"].value_counts()
top_genres = genre_counts_series[genre_counts_series >= 10].index
df_filtered = df[df["genre"].isin(top_genres)]

# 박스플롯 생성
fig5 = px.box(
    df_filtered,
    x="genre",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="주요 장르별 총 관객 수 상자 그림 (Boxplot)",
    labels={"genre": "장르", "total_audi": "총 관객 수"},
    points="outliers",  # 이상치 점만 표시
)

# hover 툴팁 서식 지정 (이상치 점에 마우스 오버 시 영화명과 총 관객 수 표시)
fig5.update_traces(
    hovertemplate="<b>영화명: %{hovertext}</b><br>총 관객 수: %{y:,.0f}명"
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.write(
    "영화 편수가 10편 이상인 주요 장르별 관객 수의 중간값과 범위를 비교할 수 있으며, 박스 밖으로 튀어나온 이상치(Outlier) 점을 통해 각 장르 내 독보적인 메가 히트 흥행작을 확인할 수 있습니다."
)
