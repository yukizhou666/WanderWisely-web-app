import helper_functions as uf
import pandas as pd
from ast import literal_eval
from constants import data_wd

# place = pd.read_csv(f'{data_wd}park_related_places.csv')
# thing = pd.read_csv(f'{data_wd}thingstodo.csv')
# loc = pd.read_csv(f'{data_wd}calculated_distances.csv', sep=';')

# place = place.rename(columns={'lat': 'ori_lat', 'lon': 'ori_lon'})
# place_w_loc = loc.merge(place, on='id')
#
# place_w_loc.to_csv(f'{data_wd}park_related_places_with_lat_lon.csv', index=False)
# place['tags'] = place['tags'].apply(lambda x: (literal_eval(x)))
# tags = place.groupby('parkCode', as_index=False)['tags'].sum()
# tags['tags'] = tags['tags'].apply(lambda x: list(set(x)))
# print(tags.head())
# tags.to_csv(f'{data_wd}place_tags.csv', index=False)


def filter_places(user_selected_park: str, user_selected_tags: list) -> pd.DataFrame:
    """

    :param user_selected_park:
    :param user_selected_tags:
    :return:
    """
    conn, engine = uf.conn_to_db()
    park_related_places = uf.import_data("select * from wanderwisely.park_related_places", conn)
    park_x_related_places = park_related_places[park_related_places['parkCode'] == user_selected_park].copy()
    park_x_related_places['tags'] = park_x_related_places['tags'].apply(lambda x: (literal_eval(x)))
    park_x_related_places['common_tags'] = park_x_related_places['tags'].apply(lambda x: list(set(x) & set(user_selected_tags)))
    park_x_related_places['score'] = park_x_related_places['common_tags'].apply(lambda x: len(x) / len(user_selected_tags))
    filtered_places = park_x_related_places[park_x_related_places['score'] > 0].sort_values(by='score', ascending=False)
    return filtered_places


if __name__ == '__main__':
    park = 'acad'
    tags = ['horse', 'beach', 'viewpoint', 'trails', 'geocache']
    places = filter_places(park, tags)
    print(places)