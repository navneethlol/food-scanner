import streamlit as st
from food_ai import identify_food
from nutrition import get_nutrition, find_food

st.title("🍎 AI Food Scanner")

st.write(
    "Upload a picture of your food to identify it and estimate its nutrition."
)

image = st.file_uploader(
    "Choose a food image",
    type=["jpg", "jpeg", "png"]
)


# -----------------------------
# STEP 1: Upload and identify
# -----------------------------

if image:

    st.image(
        image,
        caption="Uploaded food",
        width=400
    )

    if st.button("🔍 Identify Food"):

        with st.spinner("AI is analyzing your food..."):

            with open("uploaded_food.jpg", "wb") as file:
                file.write(image.getbuffer())

            result = identify_food("uploaded_food.jpg")

        st.session_state["food_result"] = result

        # Clear old nutrition results
        if "nutrition_results" in st.session_state:
            del st.session_state["nutrition_results"]


# -----------------------------
# STEP 2: Show detected food
# -----------------------------

if "food_result" in st.session_state:

    result = st.session_state["food_result"]

    dish = result["dish"]
    components = result["components"]

    st.subheader("🍽️ Detected Food")

    st.write(f"### {dish}")

    st.info(
        f"AI-estimated total weight: "
        f"**{result['estimated_total_weight_g']} g**"
    )

    st.write("### ⚖️ Estimated Components")

    st.caption(
        "These weights are AI estimates. You can edit them before calculating nutrition."
    )

    # Store edited weights
    if "component_weights" not in st.session_state:
        st.session_state["component_weights"] = {}

    for i, component in enumerate(components):

        name = component["name"]
        estimated_weight = component["estimated_weight_g"]

        weight = st.number_input(
            f"{name} (grams)",
            min_value=0.0,
            max_value=5000.0,
            value=float(estimated_weight),
            step=5.0,
            key=f"component_{i}"
        )

        st.session_state["component_weights"][name] = weight


    # -----------------------------
    # STEP 3: Calculate nutrition
    # -----------------------------

    if st.button("📊 Calculate Nutrition"):

        nutrition_results = []

        with st.spinner("Calculating nutrition..."):

            for component in components:

                name = component["name"]

                weight = st.session_state["component_weights"][name]

                if weight <= 0:
                    continue

                result = get_nutrition(
                    name,
                    weight
                )

                if result:
                    nutrition_results.append(result)

        st.session_state["nutrition_results"] = nutrition_results


# -----------------------------
# STEP 4: Display nutrition
# -----------------------------

if "nutrition_results" in st.session_state:

    results = st.session_state["nutrition_results"]

    st.subheader("📊 Nutrition Results")

    if results:

        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        total_fiber = 0

        # Create table data
        table_data = []

        for result in results:

            amount = result["actual"]

            table_data.append({
                "Food": result["name"],
                "Calories (kcal)": round(amount["calories"], 1),
                "Protein (g)": round(amount["protein"], 2),
                "Carbs (g)": round(amount["carbs"], 2),
                "Fat (g)": round(amount["fat"], 2),
                "Fiber (g)": round(amount["fiber"], 2)
            })

            total_calories += amount["calories"]
            total_protein += amount["protein"]
            total_carbs += amount["carbs"]
            total_fat += amount["fat"]
            total_fiber += amount["fiber"]

        # Display component nutrition table
        st.dataframe(
            table_data,
            use_container_width=True,
            hide_index=True
        )

        # -----------------------------
        # Total nutrition
        # -----------------------------

        st.divider()

        st.subheader("🍽️ Total Nutrition")

        total_data = [{
            "Calories (kcal)": round(total_calories, 1),
            "Protein (g)": round(total_protein, 2),
            "Carbs (g)": round(total_carbs, 2),
            "Fat (g)": round(total_fat, 2),
            "Fiber (g)": round(total_fiber, 2)
        }]

        st.dataframe(
            total_data,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.error(
            "None of the detected components were found in the Indian nutrition database."
        )




     