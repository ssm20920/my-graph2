# main.py
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

# ---------------------------------------------------------
# 첫 번째 그래프: 장르별 영화 편수 (도넛 차트)
# ---------------------------------------------------------
st.subheader("1. 장르별 영화 편수 분포")

genre_counts = df['genre_first'].value_counts().reset_index()
genre_counts.columns = ['장르', '영화편수']

fig1 = px.pie(
    genre_counts, 
    values='영화편수', 
    names='장르', 
    hole=0.4,
    title='장르별 영화 편수 비율'
)

fig1.update_traces(
    textinfo='percent+label',
    hovertemplate='<b>장르</b>: %{label}<br><b>영화 편수</b>: %{value}편<br><b>비율</b>: %{percent}'
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("박스오피스 상위권에 진입한 영화 중 특정 장르가 차지하는 비중과 주요 인기 장르의 분포를 한눈에 확인할 수 있습니다.")

st.divider()

# ---------------------------------------------------------
# 두 번째 그래프: 장르-영화 트리맵 (총 관객 수 기준)
# ---------------------------------------------------------
st.subheader("2. 장르 및 영화별 총 관객 수 분포 (트리맵)")

fig2 = px.treemap(
    df,
    path=['genre_first', 'movieNm'],
    values='total_audi',
    title='장르 및 영화별 총 관객 수 (칸 크기: 총 관객 수)',
    color='genre_first',
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig2.update_traces(
    hovertemplate='<b>%{label}</b><br>총 관객 수: %{value:,.0f}명'
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("각 장르 내에서 어떤 영화가 흥행을 주도했는지 영역 크기를 통해 비교할 수 있으며, 전체 시장 관객 수 대비 개별 영화의 관객 점유율을 직관적으로 파악할 수 있습니다.")

st.divider()

# ---------------------------------------------------------
# 세 번째 그래프: 총 관객 수 분포 (히스토그램)
# ---------------------------------------------------------
st.subheader("3. 총 관객 수 분포 (히스토그램)")

fig3 = px.histogram(
    df,
    x='total_audi',
    nbins=25,
    title='총 관객 수 분포 히스토그램',
    labels={'total_audi': '총 관객 수'},
    color_discrete_sequence=['#636EFA']
)

fig3.update_layout(
    xaxis_title='총 관객 수 (명)',
    yaxis_title='영화 수 (편)',
    bargap=0.1
)

fig3.update_traces(
    hovertemplate='<b>관객 수 구간</b>: %{x}<br><b>영화 수</b>: %{y}편'
)

st.plotly_chart(fig3, use_container_width=True)

# 최다 관객 영화 정보 동적 계산
top_movie = df.loc[df['total_audi'].idxmax()]
top_movie_name = top_movie['movieNm']
top_movie_audi = top_movie['total_audi']

st.subheader("💡 이 그래프로 알 수 있는 것")
st.write(
    f"- **밀집 구간**: 대부분의 영화가 **200만~400만 명 이하**의 하위 관객 수 구간에 높게 집중되어 있습니다.\n"
    f"- **최다 관객 영화**: 데이터 내에서 가장 많은 관객을 동원한 영화는 **'{top_movie_name}'**(총 {top_movie_audi:,.0f}명)입니다."
)
