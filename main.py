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
