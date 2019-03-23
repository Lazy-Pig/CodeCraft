# -*- coding: UTF-8 -*-
import logging
import sys
from utils.init_util import build_objects_from_files
from schedulers.GeneralScheduler import GeneralScheduler
import time


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
    id_2_cars, id_2_roads, id_2_cross = \
        build_objects_from_files(car_path, road_path, cross_path)
    scheduler = GeneralScheduler(id_2_cars, id_2_roads, id_2_cross)
    for i in id_2_roads:
        id_2_roads[i].set_scheduler(scheduler)

    global_tick = 1
    start = time.time()
    while not scheduler.is_all_arrived():
        # 所有道路状态更新
        for road_id in id_2_roads:
            id_2_roads[road_id].go_by_tick(global_tick)
        # 所有路口状态更新
        for cross_id in sorted(id_2_cross.keys()):
            id_2_cross[cross_id].go_by_tick(global_tick)
        scheduler.scheduling(global_tick)
        global_tick += 1
    end = time.time()
    logging.info("all cars have arrived, total ticks: %d, total time %d s" % (global_tick - 1, end-start))

    # to write output file
    with open(answer_path, 'w') as f:
        f.write('#(carId,StartTime,RoadId...)\n')
        for car_id in sorted(id_2_cars.keys()):
            f.write("(%d, %d, %s)\n" % (car_id,
                                      id_2_cars[car_id].get_begin_tick(),
                                      ", ".join([str(road_id) for road_id in id_2_cars[car_id].get_pass_path()])))
        f.truncate(f.tell() - 1)


if __name__ == "__main__":
    main()
