import os
import json
import pandas as pd
import mysql.connector
import tensorflow as tf
import matplotlib.pyplot as plt
import keras.backend as K
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from keras.callbacks import EarlyStopping

mydb = mysql.connector.connect(
    host="localhost",
    user="cj",
    password="1701",
    database="sCO2db"
)

componant = "comp"
param = "mass"
table = f"`{componant}`"

if componant == "turb":
    features = "`FLUID.mdot`,`FLUID.PRatio`,`FLUID.Plow`,`FLUID.Phigh`,`eta.turb`,`FLUID.Tin`,`RPM`,`mass.turb`,`W.turb`"
elif componant == "comp":
    features = "`FLUID.mdot`,`FLUID.PRatio`,`FLUID.Plow`,`FLUID.Phigh`,`eta.comp`,`FLUID.Tin`,`RPM`,`mass.comp`,`W.comp`"
else:
    raise KeyError(f"componant name {componant} not found")

query = f"SELECT {features} FROM {table}"

df = pd.read_sql_query(query, mydb)

mydb.close()

# Apply Min-Max scaling to normalize data between 0 and 1
min_values = df.min()
max_values = df.max()
df_normalized = (df - min_values) / (max_values - min_values)

# Save the min-max values to a JSON file for later denormalization
min_max_values = {
    "min_values": min_values.to_dict(),
    "max_values": max_values.to_dict()
}
#print(f'Normalized Dataset: {df_normalized}')

# Split Data and Train TensorFlow Model
output = f'{param}.{componant}'
X = df_normalized.drop(columns=[output])
y = df_normalized[output]

#print(X)
#print(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=X_train.shape[1]),  # Input layer
    tf.keras.layers.Dense(64, activation='relu'),   # Hidden layer with 64 units and ReLU activation
    tf.keras.layers.Dropout(0.4),  # Add dropout with a dropout rate
    tf.keras.layers.Dense(64, activation='relu'),   # Hidden layer with 64 units and ReLU activation
    tf.keras.layers.Dropout(0.2),  # Add dropout with a dropout rate
    tf.keras.layers.Dense(32, activation='relu'),   # Hidden layer with 64 units and ReLU activation
    tf.keras.layers.Dropout(0.2),  # Add dropout with a dropout rate
    tf.keras.layers.Dense(1, activation='linear')  # Output layer
])

# Compile model
def rmse(y_true, y_pred):
    return K.sqrt(K.mean(K.square(y_pred - y_true)))

model.compile(optimizer='adam', loss='mean_squared_error', metrics=[rmse])

# Print model summary to check the number of trainable parameters
model.summary()

# Train the TF Model
batch_size = 64
epochs = 100

early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2, callbacks=[early_stopping])

# Train RandomForestRegressor for Feature Importance
rf_regressor = RandomForestRegressor(random_state=42)
rf_regressor.fit(X_train, y_train)

# Calculate Permutation Importance
perm_importance = permutation_importance(rf_regressor, X_test, y_test, n_repeats=30, random_state=42)

# Normalize feature importances to the range [0, 1]
min_importance = perm_importance.importances_mean.min()
max_importance = perm_importance.importances_mean.max()
normalized_importances = (perm_importance.importances_mean - min_importance) / (max_importance - min_importance)

# Display Feature Importance
feature_names = X.columns
sorted_idx = normalized_importances.argsort()[::-1]  # Sort features by importance

def generate_and_save_plot():
    plt.figure(figsize=(12, 8), layout='constrained')
    plt.bar(range(X.shape[1]), normalized_importances[sorted_idx], align="center")
    plt.xticks(range(X.shape[1]), feature_names[sorted_idx], rotation=45)
    #plt.xlabel("Feature")
    plt.ylabel("Normalized Importance")
    #plt.title(f"Normalized Feature Importance (Permutation Importance), {table}")
    plt.ylim(0, 1)  # Set the y-axis limit to [0, 1]

    # Specify the directory and filename for the plot
    plot_dir = r"C:\Users\hylandc2\Documents\Research\Images"
    plot_filename = f"NFI_{table}_{param}.png"  # Define a meaningful filename

    # Ensure the directory exists (create if not) and save the plot
    os.makedirs(plot_dir, exist_ok=True)
    plot_path = os.path.join(plot_dir, plot_filename)
    plt.savefig(plot_path, bbox_inches='tight')  # Save the figure before displaying
    print(f"Plot saved as {plot_path}")

    plt.show()  # Now display the figure
    
    # Save normalized feature importances to a JSON file
    normalized_feature_importances = {name: float(importance) for name, importance in zip(feature_names[sorted_idx], normalized_importances[sorted_idx])}
    feature_importance_filename = f'normalized_feature_importances_{table}_{param}.json'
    feature_importances_dir = os.path.join(plot_dir, "feature_importances")  # Save in the same main directory as the plots
    os.makedirs(feature_importances_dir, exist_ok=True)
    feature_importance_path = os.path.join(feature_importances_dir, feature_importance_filename)
    with open(feature_importance_path, "w") as f:
        json.dump(normalized_feature_importances, f)
    print(f"Normalized feature importances saved as {feature_importance_path}")

# Evaluate the Model
test_loss, test_accuracy = model.evaluate(X_test, y_test)

# Predict the target values
y_pred = model.predict(X_test)

# Calculate R-squared (R^2) value
r2 = r2_score(y_test, y_pred)

print(f"Test Loss: {test_loss}, Test Accuracy (RMSE): {test_accuracy}, R^2 Value: {r2}")
print(f"RSME: {test_accuracy}\nR^2 value: {r2}")

filename = f'{componant}_model'
paramname = f'normalization_params_{componant}_{param}.json'

# Prompt the user to save the trained model
save_model = input("Do you want to save the trained model and normalization parameters? (yes/no): ")
if save_model.lower() == 'yes':
    generate_and_save_plot()
    
    # Create a directory if it doesn't exist
    save_dir = "saved_models"
    os.makedirs(save_dir, exist_ok=True)
    
    # Save the model to the current working directory
    model_filename = os.path.join(save_dir, f"{componant}_model_{param}.h5")
    model.save(model_filename)
    print(f"Model saved as {model_filename}")
    
    # Create a directory for normalization parameters if it doesn't exist
    normalization_params_dir = "normalization_parameters"
    os.makedirs(normalization_params_dir, exist_ok=True)
    
    # Save the normalization parameters
    normalization_params_filename = os.path.join(normalization_params_dir, paramname)
    with open(f"{paramname}", "w") as f:
        json.dump(min_max_values, f)
    print(f"Normalization parameters saved as {paramname}")