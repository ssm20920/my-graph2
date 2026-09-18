# ---------------------------------------------------------
# 8. 10위권 체류 기간 구간별 총 관객 수 분포 (상자 그림)
# ---------------------------------------------------------
QUESTION_8 = "10위권 체류 기간 구간별로 총 관객 수의 분포는 어떻게 다를까?"

st.subheader(f"8. {QUESTION_8}")

# 파이썬 조건문으로 체류 기간 구간 범주화 열 생성
def categorize_days(days):
    if days <= 10:
        return '1. 10일 이하'
    elif days <= 30:
        return '2. 11~30일'
    else:
        return '3. 31일 이상'

df['days_group'] = df['days_in_top10'].apply(categorize_days)

# 상자 그림 생성
fig_box_group = px.box(
    df,
    x='days_group',
    y='total_audi',
    color='days_group',
    hover_name='movieNm',
    points='outliers',
    title=QUESTION_8,
    labels={
        'days_group': '10위권 체류 기간 구간',
        'total_audi': '총 관객 수(명)'
    },
    category_orders={'days_group': ['1. 10일 이하', '2. 11~30일', '3. 31일 이상']}
)

fig_box_group.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객 수: %{y:,}명"
)

st.plotly_chart(fig_box_group, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 10위권 체류 기간이 길어질수록 중앙값(중위수)과 상위 관객 수의 범위가 크게 상승하며, 특히 31일 이상 장기 흥행한 구간에서 대형 흥행작들이 집중되는 경향을 명확히 비교할 수 있습니다.")

st.divider()
