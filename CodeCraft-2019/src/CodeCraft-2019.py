import logging
import sys
from init_util import build_objects_from_files
from src.algrithms.GeneralScheduler import GeneralScheduler


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
    id_2_cars, id_2_roads, id_2_cross, global_exit_queue = \
        build_objects_from_files(car_path, road_path, cross_path)
    scheduler = GeneralScheduler(id_2_cars, id_2_roads, id_2_cross)
    global_tick = 1
    while not scheduler.is_all_arrived():
        # 所有道路状态更新
        for road_id in id_2_roads:
            id_2_roads[road_id].go_by_tick(global_tick)
        # 要进入其他道路的车辆都进入对应的道路
        for road_id in id_2_roads:
            id_2_roads[road_id].enter_all(global_tick)
        global_exit_queue.clear()
        scheduler.scheduling(global_tick)
        # 新车上道
        # for car in scheduler.get_cars_just_run():
        #     car.start_running(global_tick)
        global_tick += 1

    # to write output file


if __name__ == "__main__":
    main()
