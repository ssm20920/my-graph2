import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# 한글 폰트 설정 (Mac: AppleGothic, Windows: Malgun Gothic)
plt.rc("font", family="Malgun Gothic")
plt.rc("axes", unicode_minus=False)  # 마이너스 기호 깨짐 방지

# 1. 예시 데이터 생성
data = {
    "영화명": [
        "영화 A",
        "영화 B",
        "영화 C",
        "영화 D",
        "영화 E",
        "영화 F",
        "영화 G",
    ],
    "관객수": [100, 350, 500, 750, 1000, 1200, 1300],  # 단위: 만 명
    "매출액": [9, 32, 48, 70, 95, 110, 125],  # 단위: 억원
}
df = pd.DataFrame(data)

# 2. 그래프 크기 설정
plt.figure(figsize=(10, 6))

# 3. Seaborn 산점도 및 추세선(회귀선) 그리기
sns.regplot(
    data=df,
    x="관객수",
    y="매출액",
    scatter_kws={"s": 80, "color": "#1f77b4", "alpha": 0.8},  # 점 크기 및 투명도
    line_kws={"color": "red", "linewidth": 1.5},  # 추세선 스타일
)

# 4. 데이터 포인트별 영화명 라벨링
for i in range(len(df)):
    plt.text(
        df["관객수"][i] + 20,
        df["매출액"][i],
        df["영화명"][i],
        fontsize=10,
        verticalalignment="center",
    )

# 5. 그래프 제목 및 축 라벨 설정
plt.title(
    "영화 관객 수와 매출액 간의 상관관계", fontsize=15, fontweight="bold", pad=15
)
plt.xlabel("총 관객 수 (만 명)", fontsize=12)
plt.ylabel("총 매출액 (억 원)", fontsize=12)

# 6. 그리드 및 그리기
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()

# 그래프 출력
plt.show()
