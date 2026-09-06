import pandas as pd

df = pd.read_csv("index.csv")


def find_food(food_name):

    matches = df[
        df["name"].str.contains(
            food_name,
            case=False,
            na=False
        )
    ]

    if matches.empty:
        return []

    return matches["name"].tolist()


def get_nutrition(food_name, amount_grams, selected_food=None):

    matches = df[
        df["name"].str.contains(
            food_name,
            case=False,
            na=False
        )
    ]

    if matches.empty:
        return None

    if selected_food:
        selected = matches[
            matches["name"] == selected_food
        ]

        if not selected.empty:
            food = selected.iloc[0]
        else:
            food = matches.iloc[0]
    else:
        food = matches.iloc[0]

    multiplier = amount_grams / 100

    standard = {
        "calories": food["enerc"] / 4.184,
        "protein": food["protcnt"],
        "carbs": food["choavldf"],
        "fat": food["fatce"],
        "fiber": food["fibtg"]
    }

    actual = {
        "calories": standard["calories"] * multiplier,
        "protein": standard["protein"] * multiplier,
        "carbs": standard["carbs"] * multiplier,
        "fat": standard["fat"] * multiplier,
        "fiber": standard["fiber"] * multiplier
    }

    return {
        "name": food["name"],
        "standard": standard,
        "actual": actual
    }