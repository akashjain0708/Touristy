from sklearn.cluster import KMeans
from database_interaction import *
# Column -  0: Restaurants, 1: Food, 2: Museum, 3: Central Park Zoo
# Row - 0: Chicago Bean, Wildberry pancakes


def return_cluster_labels(dataset, clusters):
    # dataset = [(1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1), (0, 1, 0, 0), (1, 1, 0, 1), (0, 1, 1, 0)]
    print("Dataset:" +str(dataset))
    kmeans = KMeans(n_clusters=clusters)
    kmeans.fit(dataset)
    return kmeans.labels_


def insert_recommend_location(tag_list, location):
    # Check if tags of the place exist in database, otherwise create it
    check_all_tags(location[0], location[1], tag_list)


def new_click_recommendation(location):
    # Get table in dataset format
    [location_table, recommend_table] = get_tag_columns()
    # Get labels for all elements
    print("Recommend table:" +str(recommend_table))
    print("Length of table:" +str(len(recommend_table)))
    print("Length of columns:" +str(len(recommend_table[0])))
    if len(recommend_table) < len(recommend_table[0]):
        clusters = len(recommend_table)
    elif len(recommend_table[0]) < 10:
        clusters = len(recommend_table[0])
    else:
        clusters = len(recommend_table[0]) - 2
    labels = return_cluster_labels(recommend_table, clusters)
    # Get label for current element
    item_position = location_table.index((location[0], location[1]))
    label_for_item = labels[item_position]
    # Get indices of all elements in the cluster
    indices = [i for i, x in enumerate(labels) if x == label_for_item]
    recommended_attractions = []
    for index in indices:
        if location_table[index][0] != location[0] and location_table[index][1] != location[1]:
            recommended_attractions.append(location_table[index])
    return recommended_attractions
