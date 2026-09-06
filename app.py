import streamlit as st
from food_ai import identify_food
from nutrition import find_food, get_nutrition

st.title("🍎 AI Food Scanner")

st.write("Upload a picture of your food to identify it and calculate its nutrition.")

image = st.file_uploader(
    "Choose a food image",
    type=["jpg", "jpeg", "png"]
)

if image:

    st.image(
        image,
        caption="Uploaded food",
        width=400
    )

    if st.button("🔍 Identify Food"):

        with st.spinner("AI is identifying your food..."):

            with open("uploaded_food.jpg", "wb") as file:
                file.write(image.getbuffer())

            food = identify_food("uploaded_food.jpg")

        st.success(f"Detected food: {food}")

        st.session_state["food"] = food


if "food" in st.session_state:

    food = st.session_state["food"]

    matches = find_food(food)

    if len(matches) > 1:

        st.subheader("🍽️ Select the food variety")

        selected_food = st.selectbox(
            "Choose the closest match:",
            matches
        )

    elif len(matches) == 1:

        selected_food = matches[0]

    else:

        selected_food = None
        st.error("This food was not found in the Indian nutrition database.")


    if selected_food:

        st.subheader("⚖️ Enter the amount you ate")

        amount = st.number_input(
            "Amount (grams)",
            min_value=1,
            max_value=5000,
            value=100,
            step=10
        )

        if st.button("📊 Calculate Nutrition"):

            result = get_nutrition(
                food,
                amount,
                selected_food
            )

            if result:

                st.subheader(f"🍽️ {result['name']}")

                st.write("### Nutrition per 100 g")

                col1, col2, col3, col4, col5 = st.columns(5)

                col1.metric(
                    "Calories",
                    f"{result['standard']['calories']:.1f} kcal"
                )

                col2.metric(
                    "Protein",
                    f"{result['standard']['protein']:.2f} g"
                )

                col3.metric(
                    "Carbs",
                    f"{result['standard']['carbs']:.2f} g"
                )

                col4.metric(
                    "Fat",
                    f"{result['standard']['fat']:.2f} g"
                )

                col5.metric(
                    "Fiber",
                    f"{result['standard']['fiber']:.2f} g"
                )


                st.write(f"### Nutrition for {amount:.0f} g")

                col1, col2, col3, col4, col5 = st.columns(5)

                col1.metric(
                    "Calories",
                    f"{result['actual']['calories']:.1f} kcal"
                )

                col2.metric(
                    "Protein",
                    f"{result['actual']['protein']:.2f} g"
                )

                col3.metric(
                    "Carbs",
                    f"{result['actual']['carbs']:.2f} g"
                )

                col4.metric(
                    "Fat",
                    f"{result['actual']['fat']:.2f} g"
                )

                col5.metric(
                    "Fiber",
                    f"{result['actual']['fiber']:.2f} g"
                )