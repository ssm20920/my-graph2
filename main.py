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
    title="장르 및 영화별 총 관객 수"
)

fig2.update_traces(
    hovertemplate="<b>%{customdata[0]}</b><br>총 관객 수: %{value:,}명"
)

st.plotly_chart(fig2, use_container_width=True)
st.info("**이 그래프로 알 수 있는 것:** 각 장르 영역 안에서 가장 큰 사각형을 차지하고 있는 영화를 확인하여 대표 흥행작을 비교할 수 있습니다.")

st.markdown("---")

# ---------------------------------------------------------
# 3. 영화 대부분은 관객이 몇 명쯤인가? (히스토그램)
# ---------------------------------------------------------
st.subheader("3. 영화 대부분은 관객이 몇 명쯤인가?")

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
* **관객 수 밀집 구간:** 대부분의 영화는 관객 수 **200만 명 이하**의 하위 구간에 모여 있으며, 관객 수가 커질수록 영화 수가 급격히 줄어드는 오른쪽 꼬리가 긴 분포를 보입니다.
* **최다 관객 동원 영화:** **{max_title}** ({max_audi:,}명)
""")

st.info("**이 그래프로 알 수 있는 것:** 흥행 영화 시장은 일부 소수의 대대적 흥행작과 다수의 중소 규모 관객 동원작으로 극명하게 양극화되어 있음을 알 수 있습니다.")

st.markdown("---")

# ---------------------------------------------------------
# 4. 스크린을 많이 받은 영화가 관객도 많나? (산점도)
# ---------------------------------------------------------
st.subheader("4. 스크린을 많이 받은 영화가 관객도 많나?")

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
# 5. 장르별 관객 분포는 어떻게 다를까? (박스플롯)
# ---------------------------------------------------------
st.subheader("5. 장르별 관객 분포는 어떻게 다를까?")

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
    points='outliers'
)

fig5.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객 수: %{y:,}명"
)

st.plotly_chart(fig5, use_container_width=True)
st.info("**이 그래프로 알 수 있는 것:** 주요 장르별 관객 수의 중간값과 흥행 변동 폭을 비교할 수 있으며, 상자 밖의 점(이상치)을 통해 특정 장르에서 발생한 대형 흥행 이변작을 확인할 수 있습니다.")

st.markdown("---")

# ---------------------------------------------------------
# 6. 첫 주 관객까지 넣으면 무엇이 더 보이나? (버블 차트)
# ---------------------------------------------------------
st.subheader("6. 첫 주 관객까지 넣으면 무엇이 더 보이나?")

fig6 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    size='first_week_audi',
    color='genre',
    hover_name='movieNm',
    size_max=40,
    title="개봉일 스크린수, 총 관객수 및 첫 주 관객수의 관계",
    labels={
        'first_scrn': '개봉일 스크린수 (개)',
        'total_audi': '총 관객수 (명)',
        'first_week_audi': '개봉 첫 주 관객수 (명)',
        'genre': '장르'
    }
)

fig6.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명<br>첫 주 관객수: %{marker.size:,}명"
)

st.plotly_chart(fig6, use_container_width=True)
st.info("**이 그래프로 알 수 있는 것:** 버블의 크기(첫 주 관객수)를 통해 초반 몰아치기로 성공한 블록버스터와, 초반 화력은 약했으나 입소문으로 장기 흥행에 성공한 영화를 구분할 수 있습니다.")

st.markdown("---")

# ---------------------------------------------------------
# 7. 국가에서 장르로 내려가면 무엇이 보이나? (선버스트)
# ---------------------------------------------------------
st.subheader("7. 국가에서 장르로 내려가면 무엇이 보이나?")

fig7 = px.sunburst(
    df,
    path=['nation', 'genre'],
    title="제작 국가 및 장르별 영화 편수 계층 구조",
    color='nation'
)

fig7.update_traces(
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<br>비율: %{percentParent:.1%}"
)

st.plotly_chart(fig7, use_container_width=True)
st.info("**이 그래프로 알 수 있는 것:** 중심 원에서 주요 국가의 영화 공급 비중을 확인하고, 바깥쪽 장르 조각을 통해 국가별 주력/선호 장르 구조를 한눈에 파악할 수 있습니다.")

st.markdown("---")

# ---------------------------------------------------------
# 8. 10위권에 오래 머문 영화는 총 관객도 많은가 (산점도)
# ---------------------------------------------------------
st.subheader("8. 10위권에 오래 머문 영화는 총 관객도 많은가")

fig8 = px.scatter(
    df,
    x='days_in_top10',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    title="10위권에 오래 머문 영화는 총 관객도 많은가",
    labels={
        'days_in_top10': '10위권에 머문 날수 (일)',
        'total_audi': '총 관객수 (명)',
        'genre': '장르'
    }
)

fig8.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>10위권 체류 일수: %{x}일<br>총 관객수: %{y:,}명"
)

st.plotly_chart(fig8, use_container_width=True)
st.info("**이 그래프로 알 수 있는 것:** 박스오피스 Top 10에 머무른 기간이 길어질수록 총 관객수 역시 확연히 증가하는 강한 양의 상관관계를 확인할 수 있습니다.")
