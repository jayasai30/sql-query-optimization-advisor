import pickle
import pandas as pd


# -------------------------------------------------
# LOAD ADVANCED ML MODEL
# -------------------------------------------------

with open("advanced_model.pkl", "rb") as file:
    model = pickle.load(file)


# -------------------------------------------------
# PREDICT OPTIMIZATION
# -------------------------------------------------

def predict_optimization(features):

    input_data = pd.DataFrame([features])

    input_data = input_data[
        [
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
    ]

    prediction = model.predict(input_data)

    return prediction[0]


# -------------------------------------------------
# TEST
# -------------------------------------------------

if __name__ == "__main__":

    test_features = {
        "joins": 1,
        "where": 1,
        "where_conditions": 1,
        "order_by": 0,
        "group_by": 0,
        "select_all": 0,
        "subquery": 0,
        "aggregate_functions": 0,
        "table_count": 2,
        "limit": 0,
        "table_size": 500,
        "index_available": 1
    }

    result = predict_optimization(test_features)

    print("\nSQL QUERY OPTIMIZATION ADVISOR")
    print("--------------------------------")
    print("Predicted Optimization:", result)