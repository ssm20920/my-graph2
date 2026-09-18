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
    
    # 결측치 제거 및 데이터 타입 정형화
    df = df.dropna(subset=['genre', 'movieNm', 'total_audi', 'first_scrn'])
    
    return df

df = load_data()

st.divider()

# ---------------------------------------------------------
# 1. 장르별 영화 편수 (도넛 그래프)
# ---------------------------------------------------------
st.subheader("1. 장르별 영화 편수")

genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['장르', '편수']

fig_donut = px.pie(
    genre_counts,
    names='장르',
    values='편수',
    hole=0.4,
    title="장르별 영화 분포"
)

fig_donut.update_traces(
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}"
)

st.plotly_chart(fig_donut, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 특정 장르에 박스오피스 상위권 영화가 얼마나 집중되어 있는지 비중을 한눈에 확인할 수 있습니다.")

st.divider()

# ---------------------------------------------------------
# 2. 장르 및 영화별 총 관객 수 (트리맵)
# ---------------------------------------------------------
st.subheader("2. 장르별 영화 총 관객 수 트리맵")

# 트리맵 오류 방지를 위한 데이터 전처리: 장르와 영화명 기준 관객수 합산
df_treemap = df.groupby(['genre', 'movieNm'], as_index=False)['total_audi'].sum()

# 트리맵 생성
fig_treemap = px.treemap(
    df_treemap,
    path=[px.Constant("전체"), 'genre', 'movieNm'],
    values='total_audi',
    color='genre',
    title="장르 및 영화별 총 관객 수 비중"
)

# 툴팁(마우스오버) 정보 설정
fig_treemap.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객 수: %{value:,}명"
)

st.plotly_chart(fig_treemap, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 장르 내에서 어떤 영화가 가장 많은 관객을 모았는지, 전체 시장에서 해당 영화의 관객 점유 규모를 한눈에 비교할 수 있습니다.")

st.divider()

# ---------------------------------------------------------
# 3. 총 관객 수 분포 (히스토그램)
# ---------------------------------------------------------
st.subheader("3. 총 관객 수 분포")

# 히스토그램 생성
fig_hist = px.histogram(
    df,
    x='total_audi',
    nbins=30,
    title="영화별 총 관객 수 분포",
    labels={'total_audi': '총 관객 수(명)'}
)

fig_hist.update_traces(
    hovertemplate="관객 수 구간: %{x}명<br>영화 수: %{y}편"
)

st.plotly_chart(fig_hist, use_container_width=True)

# 최다 관객 영화 찾기
top_movie = df.loc[df['total_audi'].idxmax()]
top_title = top_movie['movieNm']
top_audi = top_movie['total_audi']

st.info(
    f"💡 **이 그래프로 알 수 있는 것:** 대부분의 영화는 관객 수가 낮은 구간(약 100만 명 이하)에 집중되어 있는 오른쪽으로 긴 꼬리 분포를 보입니다. "
    f"가장 관객이 많은 영화는 **'{top_title}'**(총 관객 수 {top_audi:,}명)입니다."
)

st.divider()

# ---------------------------------------------------------
# 4. 개봉일 스크린수와 총 관객 수의 관계 (산점도)
# ---------------------------------------------------------
st.subheader("4. 개봉일 스크린수 vs 총 관객 수")

# 산점도 생성
fig_scatter = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    title="개봉일 스크린수와 총 관객 수의 상호관계",
    labels={
        'first_scrn': '개봉일 스크린수(개)',
        'total_audi': '총 관객 수(명)',
        'genre': '장르'
    }
)

# 툴팁 스타일 및 표시 정보 설정
fig_scatter.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객 수: %{y:,}명"
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 개봉일 스크린수가 많을수록 총 관객 수도 증가하는 양의 상관관계를 보이지만, 일부 영화는 적은 스크린수에도 불구하고 높은 총 관객 수를 기록하는 입소문 흥행 양상을 확인할 수 있습니다.")

st.divider()

# ---------------------------------------------------------
# 5. 주요 장르별 총 관객 수 분포 (상자 그림)
# ---------------------------------------------------------
st.subheader("5. 주요 장르별 총 관객 수 분포 (10편 이상 장르)")

# 영화가 10편 이상인 장르만 추출
genre_counts_series = df['genre'].value_counts()
major_genres = genre_counts_series[genre_counts_series >= 10].index
df_major = df[df['genre'].isin(major_genres)]

# 상자 그림 생성
fig_box = px.box(
    df_major,
    x='genre',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    points='outliers',  # 이상치 점 표시
    title="주요 장르별 총 관객 수 상자 그림",
    labels={
        'genre': '장르',
        'total_audi': '총 관객 수(명)'
    }
)

fig_box.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객 수: %{y:,}명"
)

st.plotly_chart(fig_box, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 영화 수가 10편 이상인 주요 장르 간 중간 관객 수 및 변동 범위의 차이를 볼 수 있으며, 상자 위쪽에 위치한 점(이상치)을 통해 장르별 대흥행작을 확인할 수 있습니다.")

st.divider()
