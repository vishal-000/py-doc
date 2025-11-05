import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Data: Hours studied and corresponding marks
X = np.array([[1], [2], [3], [4], [5], [6], [7], [8]])   # Input features
y = np.array([30, 35, 45, 50, 60, 65, 70, 80])          # Target/output

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Let user input the number of hours studied
try:
    hours_input = float(input("Enter the number of hours studied: "))
    predicted_marks = model.predict(np.array([[hours_input]]))
    print(f"Predicted marks for {hours_input} hours studied: {predicted_marks[0]:.2f}")
except Exception as e:
    print(f"Error: {e}")
