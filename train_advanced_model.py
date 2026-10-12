import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# -------------------------------------------------
# LOAD ADVANCED DATASET
# -------------------------------------------------

data = pd.read_csv("advanced_dataset.csv")

print("\nADVANCED ML MODEL TRAINING")
print("--------------------------------")

print("Dataset size:", len(data))


# -------------------------------------------------
# INPUT FEATURES
# -------------------------------------------------
features = [
    "joins",
    "where",
    "where_conditions",
    "order_by",
    "group_by",
    "select_all",
    "subquery",
    "aggregate_functions",
    "table_count",
    "limit",
    "table_size",
    "index_available"
]

X = data[features]

# Target
y = data["optimization"]


# -------------------------------------------------
# SPLIT DATA
# -------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42
)


print("Training rows:", len(X_train))
print("Testing rows :", len(X_test))


# -------------------------------------------------
# CREATE RANDOM FOREST MODEL
# -------------------------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)


# -------------------------------------------------
# TRAIN MODEL
# -------------------------------------------------

model.fit(X_train, y_train)


# -------------------------------------------------
# TEST MODEL
# -------------------------------------------------

y_pred = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    y_pred
)


print("\nModel Accuracy:")
print(round(accuracy * 100, 2), "%")


# -------------------------------------------------
# CLASSIFICATION REPORT
# -------------------------------------------------

print("\nClassification Report")
print("--------------------------------")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# -------------------------------------------------
# SAVE MODEL
# -------------------------------------------------

with open(
    "advanced_model.pkl",
    "wb"
) as file:

    pickle.dump(
        model,
        file
    )


print("\nAdvanced model saved successfully!")

print("File: advanced_model.pkl")