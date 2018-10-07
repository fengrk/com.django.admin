# -*- coding:utf-8 -*-
from __future__ import unicode_literals, absolute_import

import codecs
import logging
import os
import shutil

from django.db.utils import IntegrityError

from zhwiki.models import WikiPaper


class MigrateWikiData(object):
    def __init__(self):
        self._file_name = os.path.join(os.path.dirname(__file__), "wiki_00_chs")
        self.logger = logging.getLogger(self.__class__.__name__)
        self._file = None
        self._file_tmp_lines = []

    def run(self):
        self._restore()
        count = 1
        record_list = []

        for data in self._iter_data():
            if data is None:
                self.logger.info("job done!")
                break

            record = WikiPaper()
            record.title = data["title"]
            record.content = data["content"]
            record.url = data["url"]
            record_list.append(record)

            count += 1
            if count % 100 == 0:
                try:
                    WikiPaper.objects.bulk_create(record_list)
                    record_list = []
                except IntegrityError:
                    for record in record_list:
                        record.save()
                    record_list = []

    def _iter_data(self):
        """

        :rtype: dict
        """
        count = 1
        _find_start = False
        _find_end = False

        while True:
            try:
                for line in self._file:
                    self._file_tmp_lines.append(line)
                    if _find_start is False:
                        if line.find('<doc id="') == 0:
                            _find_start = True
                    elif _find_end is False:
                        if line.find('</doc>') == 0:
                            yield self._parse_data(self._file_tmp_lines)
                            self._file_tmp_lines = []
                            _find_start = False
                            _find_end = False
                            count += 1
                            if count % 50000 == 0:
                                self._store(recreate_file=True)
                break
            except ValueError:
                pass
            self._restore()

        yield None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._store(recreate_file=False)

    def _restore(self):
        self._file = codecs.open(self._file_name, "r", encoding="utf-8")

    def _store(self, recreate_file=False):
        with codecs.open(self._file_name + "_tmp", "w", encoding="utf-8") as fw:
            for line in self._file_tmp_lines:
                fw.write(line)
            self._file_tmp_lines = []

            line_list = []
            _count = 1
            for line in self._file:
                line_list.append(line)

                _count += 1
                if _count % 1000 == 0:
                    fw.writelines(line_list)
                    line_list = []

            if line_list:
                fw.writelines(line_list)

        self._file.close()

        shutil.move(self._file_name + "_tmp", self._file_name)

        if recreate_file:
            self._file = codecs.open(self._file_name, "r", encoding="utf-8")

    @staticmethod
    def _parse_data(data_line):
        """

        :type data_line: list
        :rtype: dict
        """
        data = {}
        if not data_line:
            return data

        def _parse_header(line):
            _line = line.split('"')
            _id = _line[1]
            _url = _line[3]
            _title = _line[5]
            return int(_id), _url, _title

        data["id"], data["url"], data["title"] = _parse_header(data_line[0])

        data["content"] = "\n".join(data_line[3:-1])

        return data


def migrate_wiki_data():
    with MigrateWikiData() as migration_manager:
        migration_manager.run()
