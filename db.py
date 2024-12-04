# -*- coding: utf-8 -*-
import logging

import psycopg2
from ddapi import DDStatsDB, DDStatsSql

__all__ = (
    "DB"
)


class DB:
    def __init__(self, con: str):
        self._log = logging.getLogger(__name__)
        self.post = None
        self.con: str = con
        self.check_connect()

    def check_connect(self) -> bool:
        if self.post is not None and not self.post.closed:
            return False
        self.post = psycopg2.connect(self.con)
        self._log.info("postgresql connect to %s", self.post.info.host)
        print("postgresql connect to %s" % self.post.info.host)
        self.post.set_session(autocommit=True)
        return True

    def close(self):
        self.post.close()

    async def check_new_map(self, dd: DDStatsDB) -> None:
        maps = await dd.maps()
        self._log.info("start check_new_map")
        while True:
            with self.post.cursor() as cur:
                maps: DDStatsSql = await dd.next(maps)
                if maps is None or maps.rows is None:
                    return

                for _, _map, server, points, stars, mapper, timestamp in maps.rows:
                    try:
                        cur.execute("INSERT INTO maps VALUES(%s, %s, %s, %s, %s, %s);", (_map, server, points, stars, mapper, timestamp))
                    except psycopg2.errors.UniqueViolation:
                        pass

                if maps.next_url is None:
                    break

                self._log.info("next_url: %s", maps.next_url)
