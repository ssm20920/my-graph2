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

top_movie = df.loc[df['total_audi'].idxmax()]
top_movie_name = top_movie['movieNm']
top_movie_audi = top_movie['total_audi']

st.subheader("💡 이 그래프로 알 수 있는 것")
st.write(
    f"- **밀집 구간**: 대부분의 영화가 **200만~400만 명 이하**의 하위 관객 수 구간에 높게 집중되어 있습니다.\n"
    f"- **최다 관객 영화**: 데이터 내에서 가장 많은 관객을 동원한 영화는 **'{top_movie_name}'**(총 {top_movie_audi:,.0f}명)입니다."
)

st.divider()

# ---------------------------------------------------------
# 네 번째 그래프: 개봉일 스크린수 vs 총 관객 수 (산점도)
# ---------------------------------------------------------
st.subheader("4. 개봉일 스크린수와 총 관객 수의 관계 (산점도)")

fig4 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='genre_first',
    hover_name='movieNm',
    title='개봉일 스크린수(first_scrn) vs 총 관객 수(total_audi)',
    labels={
        'first_scrn': '개봉일 스크린수 (개)',
        'total_audi': '총 관객 수 (명)',
        'genre_first': '장르'
    }
)

fig4.update_traces(
    marker=dict(size=9, opacity=0.8),
    hovertemplate='<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,.0f}개<br>총 관객 수: %{y:,.0f}명'
)

fig4.update_layout(
    xaxis_title='개봉일 스크린수 (개)',
    yaxis_title='총 관객 수 (명)'
)

st.plotly_chart(fig4, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("개봉 첫날 확보한 스크린수가 많을수록 대체로 최종 총 관객 수도 높게 나타나는 양의 상관관계를 볼 수 있으며, 초기 스크린 수가 적더라도 흥행에 성공한 아웃라이어 영화들도 확인할 수 있습니다.")

st.divider()

# ---------------------------------------------------------
# 다섯 번째 그래프: 주요 장르별 총 관객 수 분포 (박스플롯)
# ---------------------------------------------------------
st.subheader("5. 주요 장르별 총 관객 수 분포 (박스플롯)")

genre_counts_series = df['genre_first'].value_counts()
major_genres = genre_counts_series[genre_counts_series >= 10].index
df_major_genres = df[df['genre_first'].isin(major_genres)]

fig5 = px.box(
    df_major_genres,
    x='genre_first',
    y='total_audi',
    color='genre_first',
    points='outliers',
    hover_data={'movieNm': True, 'total_audi': ':,', 'genre_first': False},
    title='영화 10편 이상 장르별 총 관객 수 분포 및 이상치',
    labels={
        'genre_first': '장르',
        'total_audi': '총 관객 수 (명)',
        'movieNm': '영화명'
    }
)

fig5.update_layout(
    showlegend=False,
    xaxis_title='장르 (10편 이상)',
    yaxis_title='총 관객 수 (명)'
)

st.plotly_chart(fig5, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("장르별 중간값(중앙값)과 관객 수 변동 폭을 비교할 수 있으며, 박스 위쪽으로 멀리 떨어진 아웃라이어(이상치) 점들을 통해 해당 장르 내에서 초대형 흥행을 기록한 대작 영화들을 식별할 수 있습니다.")

st.divider()

# ---------------------------------------------------------
# 여섯 번째 그래프: 스크린수 vs 총 관객 수 + 첫 주 관객 수 (버블 그래프)
# ---------------------------------------------------------
st.subheader("6. 스크린수, 총 관객 수 및 첫 주 관객 수의 관계 (버블 그래프)")

fig6 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    size='first_week_audi',
    color='genre_first',
    hover_name='movieNm',
    size_max=40,
    title='개봉일 스크린수 vs 총 관객 수 (원 크기: 개봉 첫 주 관객 수)',
    labels={
        'first_scrn': '개봉일 스크린수 (개)',
        'total_audi': '총 관객 수 (명)',
        'genre_first': '장르',
        'first_week_audi': '첫 주 관객 수 (명)'
    }
)

fig6.update_traces(
    hovertemplate='<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,.0f}개<br>총 관객 수: %{y:,.0f}명<br>첫 주 관객 수: %{marker.size:,.0f}명'
)

fig6.update_layout(
    xaxis_title='개봉일 스크린수 (개)',
    yaxis_title='총 관객 수 (명)'
)

st.plotly_chart(fig6, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("초기 스크린수와 최종 총 관객 수뿐만 아니라, **원 크기(첫 주 관객 수)**를 통해 개봉 초반의 폭발적인 흥행세가 최종 흥행 성공으로 이어졌는지(초반 몰아치기형 vs 입소문 역주행형)를 다차원적으로 비교 분석할 수 있습니다.")

st.divider()

# ---------------------------------------------------------
# 일곱 번째 그래프: 제작 국가 -> 장르 선버스트 (Sunburst)
# ---------------------------------------------------------
st.subheader("7. 제작 국가 및 장르별 영화 편수 구조 (선버스트)")

fig7 = px.sunburst(
    df,
    path=['nation', 'genre_first'],
    title='제작 국가 및 장르별 영화 편수 비율 (칸 크기: 영화 편수)',
    color='nation',
    color_discrete_sequence=px.colors.qualitative.Set3
)

fig7.update_traces(
    hovertemplate='<b>%{label}</b><br>영화 편수: %{value}편<br>상위 항목 대비 비율: %{percentParent:.1%}<br>전체 대비 비율: %{percentRoot:.1%}'
)

st.plotly_chart(fig7, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("주요 제작 국가(한국, 미국 등)별로 어떤 장르의 영화가 주로 제작·수입되었는지 계층적 비중을 원형 다이어그램 형태로 한눈에 파악할 수 있습니다.")
# ── 그래프 7. 국가에서 장르로 (선버스트) ──
st.header("7. 국가에서 장르로 (선버스트)")
df["대표국가"] = df["nation"].str.split("|").str[0]
counted = (df.groupby(["대표국가", "장르"], as_index=False)
             .agg(편수=("movieNm", "count")))
fig7 = px.sunburst(counted, path=["대표국가", "장르"], values="편수")
st.plotly_chart(fig7, width="stretch")
st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")
