from sklearn.cluster import KMeans
from database_interaction import *
# Column -  0: Restaurants, 1: Food, 2: Museum, 3: Central Park Zoo
# Row - 0: Chicago Bean, Wildberry pancakes


def return_cluster_labels(dataset, clusters):
    # dataset = [(1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1), (0, 1, 0, 0), (1, 1, 0, 1), (0, 1, 1, 0)]
    kmeans = KMeans(n_clusters=clusters)
    kmeans.fit(dataset)
    return kmeans.labels_


def insert_recommend_location(tag_list, location):
    # Check if tags of the place exist in database, otherwise create it
    check_all_tags(location[0], location[1], tag_list)


def new_click_recommendation(location):
    # Get table in dataset format
    [recommend_table, location_table] = get_tag_columns()
    # Get labels for all elements
    labels = return_cluster_labels(recommend_table, 12)
    # Get label for current element
    item_position = location_table.index((location[0], location[1]))
    label_for_item = labels[item_position]
    # Get indices of all elements in the cluster
    indices = [i for i, x in enumerate(labels) if x == label_for_item]
    recommended_attractions = []
    for index in indices:
        recommended_attractions.append(location_table[index])
    return recommended_attractions
