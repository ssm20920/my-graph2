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
    df = df.dropna(subset=['genre', 'movieNm', 'movieCd', 'total_audi', 'first_scrn']).copy()
    df = df.drop_duplicates(subset=['movieCd']).copy()
    
    # 장르 전처리 (첫 번째 장르만 사용)
    df['genre'] = df['genre'].astype(str).str.split('|').str[0]
    
    # 트리맵용 고유 식별 레이블
    df['movie_label'] = df['movieNm'] + " (" + df['movieCd'].astype(str) + ")"
    
    return df

df = load_data()

# ---------------------------------------------------------
# 1. 장르별 영화 편수 (도넛 그래프)
# ---------------------------------------------------------
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
# 2. 장르 및 영화별 총 관객 수 (트리맵)
# ---------------------------------------------------------
st.subheader("2. 장르별 영화 관객 수 분포 (트리맵)")

fig2 = px.treemap(
    df,
    path=['genre', 'movie_label'],
    values='total_audi',
    color='genre',
    custom_data=['movieNm'],
    title="장르 및 영화별 총 관객 수"
)

fig2.update_traces(
    hovertemplate="<b>%{customdata[0]}</b><br>총 관객 수: %{value:,}명"
)

st.plotly_chart(fig2, use_container_width=True)
st.info("**이 그래프로 알 수 있는 것:** 각 장르가 전체 관객 수에서 차지하는 비중과, 장르 내에서 흥행을 주도한 개별 영화의 스케일을 동시에 확인할 수 있습니다.")

st.markdown("---")

# ---------------------------------------------------------
# 3. 총 관객 수 분포 (히스토그램)
# ---------------------------------------------------------
st.subheader("3. 총 관객 수 분포")

fig3 = px.histogram(
    df,
    x='total_audi',
    nbins=30,
    title="영화별 총 관객 수 분포",
    labels={'total_audi': '총 관객 수 (명)'}
)
fig3.update_layout(yaxis_title="영화 수 (편)")
fig3.update_traces(
    hovertemplate="관객 수 구간: %{x}<br>영화 수: %{y}편"
)

st.plotly_chart(fig3, use_container_width=True)

top_movie = df.loc[df['total_audi'].idxmax()]
max_title = top_movie['movieNm']
max_audi = top_movie['total_audi']

st.markdown(f"""
* **관객 수 밀집 구간:** 대부분의 영화는 관객 수 **200만 명 이하**의 하위 구간에 모여 있으며, 관객 수가 커질수록 영화 수가 급격히 줄어드는 오른쪽 꼬리가 긴(Right-skewed) 분포를 보입니다.
* **최다 관객 동원 영화:** **{max_title}** ({max_audi:,}명)
""")

st.info("**이 그래프로 알 수 있는 것:** 흥행 영화 시장은 일부 소수의 대대적 흥행작과 다수의 중소 규모 관객 동원작으로 극명하게 양극화되어 있음을 알 수 있습니다.")

st.markdown("---")

# ---------------------------------------------------------
# 4. 개봉일 스크린수와 총 관객수의 관계 (산점도)
# ---------------------------------------------------------
st.subheader("4. 개봉일 스크린수 vs 총 관객수")

fig4 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    title="개봉일 스크린수와 총 관객수의 관계",
    labels={
        'first_scrn': '개봉일 스크린수 (개)',
        'total_audi': '총 관객수 (명)',
        'genre': '장르'
    }
)

fig4.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명"
)

st.plotly_chart(fig4, use_container_width=True)
st.info("**이 그래프로 알 수 있는 것:** 개봉일 스크린수가 많을수록 총 관객수가 대체로 증가하는 양의 상관관계를 보이나, 스크린수가 적음에도 높은 관객수를 기록한 흥행 이변작도 확인할 수 있습니다.")

st.markdown("---")

# ---------------------------------------------------------
# 5. 주요 장르별 총 관객 수 분포 (박스플롯)
# ---------------------------------------------------------
st.subheader("5. 주요 장르별 총 관객 수 분포")

# 영화 수가 10편 이상인 장르만 필터링
genre_counts_series = df['genre'].value_counts()
major_genres = genre_counts_series[genre_counts_series >= 10].index
df_major_genres = df[df['genre'].isin(major_genres)]

fig5 = px.box(
    df_major_genres,
    x='genre',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    title="주요 장르별 총 관객 수 분포 (10편 이상 장르 대상)",
    labels={
        'genre': '장르',
        'total_audi': '총 관객 수 (명)'
    },
    points='outliers'  # 이상치(outliers)만 점으로 표시
)

fig5.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객 수: %{y:,}명"
)

st.plotly_chart(fig5, use_container_width=True)
st.info("**이 그래프로 알 수 있는 것:** 주요 장르별 관객 수의 중간값과 분포 범위를 비교할 수 있으며, 상자 밖의 점(이상치)을 통해 해당 장르에서 대형 흥행을 거둔 이변작들을 확인할 수 있습니다.")
