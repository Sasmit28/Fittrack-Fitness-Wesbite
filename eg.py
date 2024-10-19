import joblib

# Function to calculate the nutrients based on serving size
def calculate_nutrients(food_item, serving_size, data):
    # Find the row corresponding to the food item
    food_data = data[data['name'].str.lower() == food_item.lower()]

    if food_data.empty:
        return f"Food item '{food_item}' not found in the dataset."

    # Drop non-nutrient columns like name and emoji
    nutrient_data = food_data[['Calories', 'Carbohydrates', 'Total_Fat']]

    # Scale nutrient values (which are per gram) by the serving size
    scaled_nutrients = nutrient_data * serving_size

    return scaled_nutrients.values.flatten().reshape(1, -1)  # Return as 2D array for prediction

# Example: Predict nutrients for 'chicken' with a serving size of 200 grams
food_item = 'chicken'
serving_size = 200
nutrients = calculate_nutrients(food_item, serving_size, data_emoji_foods_cleaned)
print(nutrients)
if isinstance(nutrients, str):
    print(nutrients)
else:
    # Load the trained model from Google Drive
    model = joblib.load("/content/drive/My Drive/ColabNotebooks/calorie.pkl")

    # Predict protein, carbs, fat, and calories using the trained model
    predicted_nutrients = model.predict(nutrients)
    
    # Extract and round the predicted values
    predicted_protein = round(predicted_nutrients[0][0])
    predicted_carbs = round(predicted_nutrients[0][1])
    predicted_fat = round(predicted_nutrients[0][2])
    predicted_calories = round(predicted_nutrients[0][3])

    # Print predicted values as integers
    print(f"Predicted Protein for {serving_size} grams of {food_item}: {predicted_protein} grams")
    print(f"Predicted Carbs for {serving_size} grams of {food_item}: {predicted_carbs} grams")
    print(f"Predicted Fat for {serving_size} grams of {food_item}: {predicted_fat} grams")
    print(f"Predicted Calories for {serving_size} grams of {food_item}: {predicted_calories} kcal")

