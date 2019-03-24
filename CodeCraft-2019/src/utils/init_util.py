# -*- coding: UTF-8 -*-
from abstracts.Car import Car
from abstracts.Road import Road
from abstracts.Lane import Lane
from abstracts.Cross import Cross


def create_object_from_file(path, class_name):
    """
    从文件中读取数据并创建相应对象

    @param path: str 文件路径
    @param class_name: str 类名，取值Car、Cross、Road
    @return: dict，id to 对象
    """
    id_2_objects = {}
    target_class = eval(class_name)
    with open(path, 'r') as f:
        next(f)
        for line in f:
            args = [int(ch) for ch in line.strip("()\n").split(",")]
            id_2_objects[args[0]] = target_class(*args)
    return id_2_objects


def build_objects_from_files(car_path, road_path, cross_path):
    # to read input file
    id_2_cars = create_object_from_file(car_path, 'Car')
    id_2_roads = create_object_from_file(road_path, 'Road')
    id_2_cross = create_object_from_file(cross_path, 'Cross')
    # 为所有的car设置source和destination
    for car_id, car in id_2_cars.items():
        source_id = car.get_source_id()
        destination_id = car.get_destination_id()
        car.set_source(id_2_cross[source_id])
        car.set_destination(id_2_cross[destination_id])

    # 为所有的road设置source和destination
    for road_id, road in id_2_roads.items():
        source_id = road.get_source_id()
        destination_id = road.get_destination_id()
        road.set_source(id_2_cross[source_id])
        road.set_destination(id_2_cross[destination_id])

    # 为所有的cross设置对应的road
    for cross_id, cross in id_2_cross.items():
        road_id_list = cross.get_road_id_list()
        roads = [id_2_roads[id] if id != -1 else None for id in road_id_list]
        cross.set_road_list(roads)
    return id_2_cars, id_2_roads, id_2_cross


def build_path_from_answer(id_2_cars, id_2_roads, answer_path):
    with open(answer_path, 'r') as f:
        next(f)
        for line in f:
            args = [int(ch) for ch in line.strip("()\n").split(",")]
            car_id, begin_tick = args[0], args[1]
            car = id_2_cars[car_id]
            car.set_begin_tick(begin_tick)
            path = []
            last_cross_id = car.get_source_id()
            for road_id in args[2:]:
                road = id_2_roads[road_id]
                if road.get_source_id() == last_cross_id:
                    path.append((road, 'positive'))
                    last_cross_id = road.get_destination_id()
                else:
                    path.append((road, 'negative'))
                    last_cross_id = road.get_source_id()
            car.set_path(path)

