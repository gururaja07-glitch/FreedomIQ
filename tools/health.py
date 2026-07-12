def health_score(df):

    score = 100

    top_weight = df["Weight %"].max()

    if top_weight > 40:
        score -= 20

    elif top_weight > 30:
        score -= 10

    sectors = df["Sector"].nunique()

    if sectors < 5:
        score -= 20

    print()
    print("=" * 40)
    print("PORTFOLIO HEALTH")
    print("=" * 40)

    print(f"Health Score : {score}/100")
    print(f"Number of Sectors : {sectors}")
    print(f"Largest Holding   : {top_weight:.2f}%")

    if score >= 90:
        print("Rating : EXCELLENT ⭐⭐⭐⭐⭐")
    elif score >= 75:
        print("Rating : GOOD ⭐⭐⭐⭐")
    elif score >= 60:
        print("Rating : AVERAGE ⭐⭐⭐")
    else:
        print("Rating : NEEDS IMPROVEMENT ⭐⭐")

    print("=" * 40)