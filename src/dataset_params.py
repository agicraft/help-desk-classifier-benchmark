ds_root_dir = "./data/dataset1"

ds_train_file = ds_root_dir + "/train_data.csv"
ds_predict_file = ds_root_dir + "/predict__{name}.csv"
ds_scores_file = ds_root_dir + "/scores.csv"

DS_ATTR_ID = "index"

DS_ATTR_TOPIC = "Тема"
DS_ATTR_MESSAGE = "Описание"

DS_ATTR_SERIAL = "Серийный номер"
DS_ATTR_FAILURE_POINT = "Точка отказа"
DS_ATTR_EQUIPMENT_TYPE = "Тип оборудования"

API_ATTR_SERIAL = "serial_number"
API_ATTR_FAILURE_POINT = "failure_point"
API_ATTR_EQUIPMENT_TYPE = "equipment_type"

ds_attrs = [
    DS_ATTR_EQUIPMENT_TYPE,
    DS_ATTR_FAILURE_POINT,
    DS_ATTR_SERIAL,
]

api_attrs = [
    API_ATTR_EQUIPMENT_TYPE,
    API_ATTR_FAILURE_POINT,
    API_ATTR_SERIAL,
]
