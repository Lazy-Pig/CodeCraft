# -*- coding: UTF-8 -*-
import logging
import sys
from utils.init_util import build_objects_from_files, build_path_from_answer, all_is_done
from schedulers.GeneralScheduler import GeneralScheduler
from schedulers.Scheduler import Scheduler
import time


MODE = 'scheduling'
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

    if MODE == 'scheduling':
        scheduler = GeneralScheduler(id_2_cars, id_2_roads, id_2_cross)
    else:
        scheduler = Scheduler(id_2_cars, id_2_roads, id_2_cross)
        build_path_from_answer(id_2_cars, id_2_roads, answer_path)

    for i in id_2_roads:
        id_2_roads[i].set_scheduler(scheduler)

    global_tick = 1
    start = time.time()
    while not scheduler.is_all_arrived():
        logging.info("current tick: %d" % global_tick)
        # 所有道路状态更新
        for road_id in id_2_roads:
            id_2_roads[road_id].go_by_tick(global_tick)
        # 所有路口状态更新
        unfinished_cross_ids = list(sorted(id_2_cross.keys()))
        while len(unfinished_cross_ids) > 0:
            dead = True
            next_cross_ids = []
            for cross_id in unfinished_cross_ids:
                cross = id_2_cross[cross_id]
                cross.go_by_tick(global_tick)
                if not id_2_cross[cross_id].is_done():
                    next_cross_ids.append(cross_id)
                if cross.has_updated() or cross.is_done():
                    dead = False
            unfinished_cross_ids = next_cross_ids
            assert dead is False, print("dead lock in", unfinished_cross_ids)
        assert all_is_done(id_2_roads)
        scheduler.scheduling(global_tick)
        global_tick += 1
    end = time.time()
    logging.info("all cars have arrived, total ticks: %d, total time %d s" % (global_tick - 1, end-start))

    if MODE == 'scheduling':
        # to write output file
        with open(answer_path, 'w') as f:
            for car_id in sorted(id_2_cars.keys()):
                f.write("(%d, %d, %s)\n" % (car_id,
                                          id_2_cars[car_id].get_begin_tick(),
                                          ", ".join([str(road_id) for road_id in id_2_cars[car_id].get_pass_path()])))
            f.truncate(f.tell() - 1)


if __name__ == "__main__":
    main()
