# =========================================================
# 6. 개봉일 스크린수 vs 총 관객 수 버블 그래프 (점 크기: 첫 주 관객)
# =========================================================
st.subheader("6. 개봉일 스크린수 vs 총 관객 수 버블 그래프 (점 크기: 첫 주 관객)")

fig_bubble = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    size='first_week_audi', # 네 번째 산점도에 첫 주 관객(first_week_audi)을 점 크기로 매핑
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
