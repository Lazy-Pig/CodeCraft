import logging
import sys
import abstracts


logging.basicConfig(level=logging.DEBUG,
                    # filename='../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')


def main():
    if len(sys.argv) != 5:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("answer_path is %s" % (answer_path))

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

    return


    # to write output file


def create_object_from_file(path, class_name):
    """
    从文件中读取数据并创建相应对象

    @param path: str 文件路径
    @param class_name: str 类名，取值Car、Cross、Road
    @return: dict，id to 对象
    """
    id_2_objects = {}
    target_class = getattr(abstracts, class_name)
    with open(path, 'r') as f:
        next(f)
        for line in f:
            args = [int(ch) for ch in line.strip("()\n").split(",")]
            id_2_objects[args[0]] = target_class(*args)
    return id_2_objects


if __name__ == "__main__":
    main()