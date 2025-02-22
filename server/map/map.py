import math
import random
import osmnx as ox
import networkx as nx
from geopy.distance import great_circle


class Map:
    mock_cameras = [
        {'camera_id': 1, 'camera_url': 'https://s1.moidom-stream.ru/s/public/0000000088.m3u8',
         'coords': [61.80843, 34.319], 'parking_places': []},
        {'camera_id': 2, 'camera_url': 'https://s1.moidom-stream.ru/s/public/0000000088.m3u8',
         'coords': [61.81034, 34.32836], 'parking_places': []},
        {'camera_id': 3, 'camera_url': 'https://s1.moidom-stream.ru/s/public/0000000088.m3u8',
         'coords': [61.80943, 34.33114], 'parking_places': []},
        {'camera_id': 4, 'camera_url': 'https://s1.moidom-stream.ru/s/public/0000000088.m3u8',
         'coords': [61.80797, 34.33023], 'parking_places': []},
        {'camera_id': 5, 'camera_url': 'https://s1.moidom-stream.ru/s/public/0000000088.m3u8',
         'coords': [61.80657, 34.3396], 'parking_places': []},
        {'camera_id': 6, 'camera_url': 'https://s1.moidom-stream.ru/s/public/0000000088.m3u8',
         'coords': [61.8022, 34.32632], 'parking_places': []},
        {'camera_id': 7, 'camera_url': 'https://s1.moidom-stream.ru/s/public/0000000088.m3u8',
         'coords': [61.8015, 34.32481], 'parking_places': []},
        {'camera_id': 8, 'camera_url': 'https://s1.moidom-stream.ru/s/public/0000000088.m3u8',
         'coords': [61.80065, 34.33137], 'parking_places': []},
        {'camera_id': 9, 'camera_url': 'https://s1.moidom-stream.ru/s/public/0000000088.m3u8',
         'coords': [61.79444, 34.37681], 'parking_places': []},
        {'camera_id': 10, 'camera_url': 'https://s1.moidom-stream.ru/s/public/0000000088.m3u8',
         'coords': [61.7895, 34.36859], 'parking_places': []},
        {'camera_id': 11, 'camera_url': 'https://s1.moidom-stream.ru/s/public/0000000088.m3u8',
         'coords': [61.79047, 34.37184], 'parking_places': []},
        {'camera_id': 12, 'camera_url': 'https://s1.moidom-stream.ru/s/public/0000000088.m3u8',
         'coords': [61.78094, 34.32517], 'parking_places': []},
        {'camera_id': 13, 'camera_url': 'https://s1.moidom-stream.ru/s/public/0000000088.m3u8',
         'coords': [61.76542, 34.3142], 'parking_places': []},
        {'camera_id': 14, 'camera_url': 'https://s1.moidom-stream.ru/s/public/0000000088.m3u8',
         'coords': [61.75969, 34.31625], 'parking_places': []},
        {'camera_id': 15, 'camera_url': 'https://s1.moidom-stream.ru/s/public/0000000088.m3u8',
         'coords': [61.75903, 34.35843], 'parking_places': []},
        {'camera_id': 16, 'camera_url': 'https://s1.moidom-stream.ru/s/public/0000000088.m3u8',
         'coords': [61.76131, 34.36878], 'parking_places': []},
        {'camera_id': 17, 'camera_url': 'https://s1.moidom-stream.ru/s/public/0000000088.m3u8',
         'coords': [61.7681, 34.38785], 'parking_places': []},
        {'camera_id': 18, 'camera_url': 'https://s1.moidom-stream.ru/s/public/0000000088.m3u8',
         'coords': [61.76248, 34.41948], 'parking_places': []},
        {'camera_id': 19, 'camera_url': 'https://s1.moidom-stream.ru/s/public/0000000088.m3u8',
         'coords': [61.78496, 34.34497], 'parking_places': []},
        {'camera_id': 20, 'camera_url': 'https://s1.moidom-stream.ru/s/public/0000000088.m3u8',
         'coords': [61.78749, 34.38096], 'parking_places': []}
    ]
    __graph = None

    @staticmethod
    def init(center=(61.787439, 34.354423), dist=5000):
        """
        Инициализирует класс, загружает карту местности
        :param center: точка центра карты
        :param dist: расстояние от точки
        :return: None
        """
        Map.__graph = ox.graph_from_point(center, dist=dist, simplify=True, network_type='all')

    @staticmethod
    def generate_route_link(point_a, point_b, site='yandex'):
        """
        Возвращает ссылку на построенный маршрут из первой точки во вторую
        :param point_a: первая точка (lat, lng)
        :param point_b: вторая точка (lat, lng)
        :param site: сайт (yandex, 2gis)
        :return: web-ссылка на маршрут
        """
        link = ''
        lat2, lng2 = point_b

        if point_a is None:
            lat1, lng1 = '', ''
            avg_lat, avg_lng = lat2, lat1
        else:
            lat1, lng1 = point_a
            avg_lat, avg_lng = (lat1 + lat2) / 2, (lng1 + lng2) / 2

        if site == 'yandex':
            link += 'https://yandex.ru/maps/?ll='
            link += f'{avg_lng}%2C{avg_lat}'
            if point_a is None:
                link += f'&mode=routes&rtext=~{lat2}%2C{lng2}&rtt=auto&z=12'
            else:
                link += f'&mode=routes&rtext={lat1}%2C{lng1}~{lat2}%2C{lng2}&rtt=auto&z=12'

        elif site == '2gis':
            link += 'https://2gis.ru/directions/points/'
            if point_a is None:
                link += f'%7C{lng2}%2C{lat2}'
            else:
                link += f'{lng1}%2C{lat1}%7C{lng2}%2C{lat2}'
            link += f'?m={avg_lng}%2C{avg_lat}'

        else:
            raise ValueError(f'site=\'{site}\'')

        return link

    @staticmethod
    def get_euclid_distance(point_a, point_b):
        """
        Вычисляет Евклидово расстояние между двумя точками
        :param point_a: первая точка (lat, lng)
        :param point_b: вторая точка (lat, lng)
        :return: расстояние между точками
        """
        lat1, lng1 = point_a
        lat2, lng2 = point_b
        lat_dif, lng_dif = lat1 - lat2, lng1 - lng2
        return math.sqrt(lat_dif * lat_dif + lng_dif * lng_dif)

    @staticmethod
    def get_circle_distance(point_a, point_b):
        """
        Вычисляет сферическое расстояние между двумя точками
        :param point_a: первая точка (lat, lng)
        :param point_b: вторая точка (lat, lng)
        :return: расстояние между точками
        """
        return great_circle(point_a, point_b).m

    @staticmethod
    def get_dijkstra_distance(point_a, point_b):
        """
        Вычисляет расстояние между двумя точками на карте методом Дийкстры
        :param point_a: первая точка (lat, lng)
        :param point_b: вторая точка (lat, lng)
        :return: расстояние между точками
        """
        lat1, lng1 = point_a
        lat2, lng2 = point_b
        source = ox.nearest_nodes(Map.__graph, lng1, lat1)
        target = ox.nearest_nodes(Map.__graph, lng2, lat2)
        return nx.shortest_path_length(Map.__graph, source, target, weight='length')

    @staticmethod
    def get_point_point_distance(point_a, point_b, method='dijkstra'):
        """
        Вычисляет расстояние между двумя точками
        :param point_a: первая точка (lat, lng)
        :param point_b: вторая точка (lat, lng)
        :param method: способ расчета расстояния ['dijkstra', 'euclid', 'circle']
        :return: расстояние между точками
        """
        if method == 'dijkstra':
            distance = Map.get_dijkstra_distance(point_a, point_b)
        elif method == 'euclid':
            distance = Map.get_euclid_distance(point_a, point_b)
        elif method == 'circle':
            distance = Map.get_circle_distance(point_a, point_b)
        else:
            raise ValueError(f'Unknown method={method}')

        return distance

    @staticmethod
    def get_camera_point_distance(camera, point, method='dijkstra'):
        """
        Вычисляет расстояние между камерой и точкой
        :param camera: камера
        :param point: точка (lat, lng)
        :param method: способ расчета расстояния ['dijkstra', 'euclid', 'circle']
        :return: расстояние между камерой и точкой
        """
        lat, lng = camera['coords']
        return Map.get_point_point_distance((lat, lng), point, method)

    @staticmethod
    def __quicksort(cameras, point, fst, lst, method='dijkstra'):
        """
        Сортировка Хоара для камер по расстоянию до точки
        :param cameras: список камер
        :param point: точка
        :param fst: начальный индекс сортировки
        :param lst: конечный индекс сортировки
        :param method: способ расчета расстояния ['dijkstra', 'euclid', 'circle']
        :return: отсортированный лист камер
        """
        if fst >= lst:
            return cameras

        i, j = fst, lst
        camera = cameras[random.randint(fst, lst)]
        pivot = Map.get_camera_point_distance(camera, point, method)

        while i <= j:
            while Map.get_camera_point_distance(cameras[i], point, method) < pivot:
                i += 1
            while Map.get_camera_point_distance(cameras[j], point, method) > pivot:
                j -= 1
            if i <= j:
                cameras[i], cameras[j] = cameras[j], cameras[i]
                i, j = i + 1, j - 1
        Map.__quicksort(cameras, point, fst, j, method)
        Map.__quicksort(cameras, point, i, lst, method)
        return cameras

    @staticmethod
    def sort_cameras(cameras, point, method='dijkstra'):
        """
        Возвращает отсортированный по возрастанию расстояний до точки
        список камер
        :param cameras: начальный список камер
        :param point: точка
        :param method: способ расчета расстояния ['dijkstra', 'euclid', 'circle']
        :return: отсортированный лист камер
        """
        length = len(cameras)
        if length == 0:
            return cameras

        return Map.__quicksort(cameras, point, 0, length - 1, method)

    @staticmethod
    def sort_mock_cameras(point, method='dijkstra'):
        """
        Возвращает отсортированный по возрастанию расстояний до точки
        список фиксированных камер
        :param point: точка
        :param method: способ расчета расстояния ['dijkstra', 'euclid', 'circle']
        :return: отсортированный лист камер
        """
        return Map.sort_cameras(Map.mock_cameras, point, method)
