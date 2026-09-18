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

st.info("**이 그래프로 알 수 있는 것:** 대부분의 영화는 200만 명 이하의 구간에 밀집되어 있으며, 대형 흥행을 거두는 영화는 극히 일부에 불과하다는 점을 한눈에 알 수 있습니다.")
