# Import libraries:
import os
import pickle
import pandas as pd
from sklearn import metrics  # Additional scklearn functions
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
#from xgboost import XGBRegressor


# def main_model(h_zip, living, beds, baths, lot, year):
#     script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
#     model_filename = 'data/finalized_model.sav'
#     predictors = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'zipcode', 'year']
#     try:
#         xgb2 = pickle.load(open(os.path.join(script_dir, model_filename), 'rb'))
#         print('model is loaded')
#     except:
#         rel_path = 'data/processed_data.csv'
#         abs_file_path = os.path.join(script_dir, rel_path)
#         try:
#             df = pd.read_csv(abs_file_path)
#             print("Main dataset has {} samples with {} features each.".format(*df.shape))
#         except:
#             print("Dataset could not be loaded. Is the dataset missing?")
#
#         target = 'price'
#         X = df.ix[:, :-1]
#         Y = df[target]
#         x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
#         x_test, x_val, y_test, y_val = train_test_split(x_test, y_test, test_size=0.5, random_state=42)
#         df_train = pd.concat([x_train.reset_index(drop=True), y_train.reset_index(drop=True)], axis=1)
#         df_test = pd.concat([x_test.reset_index(drop=True), y_test.reset_index(drop=True)], axis=1)
#         # final model
#         xgb2 = XGBRegressor(
#             learning_rate=0.1,
#             n_estimators=406,
#             max_depth=5,
#             min_child_weight=1,
#             gamma=0,
#             subsample=0.7,
#             colsample_bytree=0.9,
#             objective='reg:linear',
#             reg_alpha=100,
#             nthread=4,
#             scale_pos_weight=1,
#             seed=100)
#         xgb2.fit(df_train[predictors], df_train['price'], eval_metric='rmse')
#         pickle.dump(xgb2, open(os.path.join(script_dir, model_filename), 'wb'))
#     idm = 10000
#     my_data2 = pd.DataFrame.from_records([{'id': idm, 'bedrooms': beds, 'bathrooms': baths, 'sqft_living': living,
#                                            'sqft_lot': lot, 'zipcode': h_zip, 'year': year}])
#     my_data2 = my_data2[['id', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'zipcode', 'year']]
#     #print(my_data2.head())
#     #dtest_predictions = xgb2.predict(df_test[predictors])
#     #print("r2 Score : %.4g" % metrics.r2_score(df_test['price'].values, dtest_predictions))
#     # print("MRSE Score : %.4g" % mean_relative_square_error(df_test['price'].values, dtest_predictions))
#     #print(df_test[predictors].head())
#     #print(y_test.head())
#     #print(dtest_predictions)
#     #print(xgb2.predict(my_data2[predictors]))
#     return int(xgb2.predict(my_data2[predictors])[0])


def model_rez(home_data):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = 'kc.csv'
    abs_file_path = os.path.join(script_dir, rel_path)
    data = pd.read_csv(abs_file_path)
    y = data.price
    predictors = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot']
    X = data[predictors]
    train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=0)

    forest_model = RandomForestRegressor(random_state=100)
    forest_model.fit(train_X, train_y)
    mydata = pd.read_json(
        home_data,
        orient='index')
    test_X = mydata[predictors]
    predicted_prices = forest_model.predict(test_X)
    print(int(predicted_prices[0]))
    return int(predicted_prices[0])

def model_random_forest(h_zip, living, beds, baths, lot, year):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    model_filename = 'data/random_forest_model.sav'
    predictors = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'zipcode', 'year']
    try:
        xgb2 = pickle.load(open(os.path.join(script_dir, model_filename), 'rb'))
        print('model is loaded')
    except:
        rel_path = 'data/processed_data.csv'
        abs_file_path = os.path.join(script_dir, rel_path)
        try:
            df = pd.read_csv(abs_file_path)
            print("Main dataset has {} samples with {} features each.".format(*df.shape))
        except:
            print("Dataset could not be loaded. Is the dataset missing?")

        target = 'price'
        X = df.ix[:, :-1]
        Y = df[target]
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
        x_test, x_val, y_test, y_val = train_test_split(x_test, y_test, test_size=0.5, random_state=42)
        df_train = pd.concat([x_train.reset_index(drop=True), y_train.reset_index(drop=True)], axis=1)
        df_test = pd.concat([x_test.reset_index(drop=True), y_test.reset_index(drop=True)], axis=1)
        # final model
        xgb2 = RandomForestRegressor(random_state=100)
        xgb2.fit(df_train[predictors], df_train['price'])
        pickle.dump(xgb2, open(os.path.join(script_dir, model_filename), 'wb'))
    idm = 10000
    my_data2 = pd.DataFrame.from_records([{'id': idm, 'bedrooms': beds, 'bathrooms': baths, 'sqft_living': living,
                                           'sqft_lot': lot, 'zipcode': h_zip, 'year': year}])
    my_data2 = my_data2[['id', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'zipcode', 'year']]
    # print(my_data2.head())
    # dtest_predictions = xgb2.predict(df_test[predictors])
    # print("r2 Score : %.4g" % metrics.r2_score(df_test['price'].values, dtest_predictions))
    # print("MRSE Score : %.4g" % mean_relative_square_error(df_test['price'].values, dtest_predictions))
    # print(df_test[predictors].head())
    # print(y_test.head())
    # print(dtest_predictions)
    # print(xgb2.predict(my_data2[predictors]))
    return int(xgb2.predict(my_data2[predictors])[0])
