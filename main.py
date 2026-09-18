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
    
    # genre 열 안전한 전처리 (첫 번째 장르만 추출)
    if 'genre' in df.columns:
        df['genre'] = df['genre'].astype(str).str.split('|').str[0]
        
    return df

# 전역 데이터 변수 정의
df = load_data()


# =========================================================
# 1. 장르별 영화 편수 (도넛 차트)
# =========================================================
st.subheader("1. 장르별 영화 편수 분포")

genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['장르', '영화 수']

fig_donut = px.pie(
    genre_counts,
    names='장르',
    values='영화 수',
    hole=0.4,
    title="장르별 영화 비율",
    hover_data=['영화 수']
)

fig_donut.update_traces(
    textinfo='percent+label',
    hovertemplate="<b>장르:</b> %{label}<br><b>영화 수:</b> %{value}편<br><b>비율:</b> %{percent}"
)

st.plotly_chart(fig_donut, use_container_width=True)

st.markdown("---")
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("개봉한 주요 영화들 중 특정 장르가 차지하는 비중과 다빈도 개봉 장르를 한눈에 파악할 수 있습니다.")
st.markdown("---")


# =========================================================
# 2. 장르별 영화 및 총 관객 수 (트리맵)
# =========================================================
st.subheader("2. 장르 및 영화별 총 관객 수 트리맵")

fig_treemap = px.treemap(
    df,
    path=[px.Constant("전체 장르"), 'genre', 'movieNm'],
    values='total_audi',
    color='genre',
    title="장르 내 영화별 총 관객 수 분포",
    custom_data=['movieNm', 'total_audi', 'genre']
)

fig_treemap.update_traces(
    hovertemplate="<b>영화명:</b> %{customdata[0]}<br><b>장르:</b> %{customdata[2]}<br><b>총 관객 수:</b> %{customdata[1]:,}명<extra></extra>"
)

fig_treemap.update_layout(margin=dict(t=50, l=10, r=10, b=10))

st.plotly_chart(fig_treemap, use_container_width=True)

st.markdown("---")
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("장르 전체의 총 관객 규모뿐만 아니라, 해당 장르 내에서 어떤 영화가 관객 수를 주도했는지 개별 영화의 기여도를 사각형 크기로 직관적으로 비교할 수 있습니다.")
st.markdown("---")


# =========================================================
# 3. 총 관객 수 분포 (히스토그램)
# =========================================================
st.subheader("3. 총 관객 수 히스토그램")

max_movie_row = df.loc[df['total_audi'].idxmax()]
max_movie_name = max_movie_row['movieNm']
max_movie_audi = max_movie_row['total_audi']

fig_hist = px.histogram(
    df,
    x='total_audi',
    nbins=20,
    title="영화별 총 관객 수 분포 구간",
    labels={'total_audi': '총 관객 수'},
    color_discrete_sequence=['#636EFA']
)

fig_hist.update_layout(
    xaxis_title="총 관객 수 (명)",
    yaxis_title="영화 수 (편)",
    bargap=0.08
)

fig_hist.update_traces(
    hovertemplate="<b>관객 수 구간:</b> %{x}<br><b>영화 수:</b> %{y}편<extra></extra>"
)

st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("---")
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info(
    f"대부분의 영화가 하위 관객 수 구간(0~200만 명 대)에 몰려 있는 쏠림 현상을 보이며, "
    f"가장 관객이 많은 최고의 흥행 영화는 **'{max_movie_name}'**(총 {max_movie_audi:,}명)입니다."
)
st.markdown("---")


# =========================================================
# 4. 개봉일 스크린수와 총 관객 수의 관계 (산점도)
# =========================================================
st.subheader("4. 개봉일 스크린수 vs 총 관객 수 관계")

fig_scatter = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='genre',
    title="개봉일 스크린수에 따른 총 관객 수 분포",
    labels={
        'first_scrn': '개봉일 스크린수',
        'total_audi': '총 관객 수',
        'genre': '장르'
    },
    hover_name='movieNm',
    custom_data=['movieNm', 'genre']
)

fig_scatter.update_traces(
    hovertemplate="<b>영화명:</b> %{customdata[0]}<br>" +
                  "<b>장르:</b> %{customdata[1]}<br>" +
                  "<b>개봉일 스크린수:</b> %{x:,}개<br>" +
                  "<b>총 관객 수:</b> %{y:,}명<extra></extra>"
)

fig_scatter.update_layout(
    xaxis_title="개봉일 스크린수 (개)",
    yaxis_title="총 관객 수 (명)"
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("개봉일 스크린수가 많을수록 대체로 총 관객 수도 증가하는 양의 상관관계를 보이지만, 스크린수가 적음에도 높은 관객 수를 기록한 흥행작(입소문 영화)이나 반대의 사례도 함께 확인할 수 있습니다.")
st.markdown("---")


# =========================================================
# 5. 영화 10편 이상 장르의 총 관객 수 상자 그림 (박스플롯)
# =========================================================
st.subheader("5. 주요 장르별 총 관객 수 박스플롯")

genre_counts_series = df['genre'].value_counts()
top_genres = genre_counts_series[genre_counts_series >= 10].index
df_filtered = df[df['genre'].isin(top_genres)]

fig_box = px.box(
    df_filtered,
    x='genre',
    y='total_audi',
    color='genre',
    title="영화 10편 이상 주요 장르의 총 관객 수 분포 (이상치 포함)",
    labels={'genre': '장르', 'total_audi': '총 관객 수'},
    hover_name='movieNm',
    points='outliers',
    custom_data=['movieNm']
)

fig_box.update_traces(
    hovertemplate="<b>영화명:</b> %{customdata[0]}<br>" +
                  "<b>장르:</b> %{x}<br>" +
                  "<b>총 관객 수:</b> %{y:,}명<extra></extra>"
)

fig_box.update_layout(
    xaxis_title="장르",
    yaxis_title="총 관객 수 (명)",
    showlegend=False
)

st.plotly_chart(fig_box, use_container_width=True)

st.markdown("---")
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("주요 장르별 관객 수의 중간값과 편차를 비교할 수 있으며, 박스 바깥으로 튀어나온 점(이상치)에 마우스를 올려 각 장르의 대흥행 성공작이 어떤 영화인지 한눈에 식별할 수 있습니다.")
st.markdown("---")


# =========================================================
# 6. 개봉일 스크린수 vs 총 관객 수 버블 그래프 (점 크기: 첫 주 관객)
# =========================================================
st.subheader("6. 개봉일 스크린수 vs 총 관객 수 버블 그래프 (점 크기: 첫 주 관객)")

fig_bubble = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    size='first_week_audi',
    color='genre',
    title="개봉일 스크린수, 총 관객 수 및 첫 주 관객 수(버블 크기) 관계",
    labels={
        'first_scrn': '개봉일 스크린수',
        'total_audi': '총 관객 수',
        'first_week_audi': '첫 주 관객 수',
        'genre': '장르'
    },
    hover_name='movieNm',
    size_max=40,
    custom_data=['movieNm', 'genre', 'first_week_audi']
)

fig_bubble.update_traces(
    hovertemplate="<b>영화명:</b> %{customdata[0]}<br>" +
                  "<b>장르:</b> %{customdata[1]}<br>" +
                  "<b>개봉일 스크린수:</b> %{x:,}개<br>" +
                  "<b>첫 주 관객 수:</b> %{customdata[2]:,}명<br>" +
                  "<b>총 관객 수:</b> %{y:,}명<extra></extra>"
)

fig_bubble.update_layout(
    xaxis_title="개봉일 스크린수 (개)",
    yaxis_title="총 관객 수 (명)"
)

st.plotly_chart(fig_bubble, use_container_width=True)

st.markdown("---")
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("개봉일 스크린수와 총 관객 수의 관계뿐만 아니라, 점의 크기를 통해 개봉 초반(첫 주 관객)의 흥행 규모가 최종 흥행 관객 수에 미치는 영향력을 시각적으로 동시에 비교해 볼 수 있습니다.")
st.markdown("---")
