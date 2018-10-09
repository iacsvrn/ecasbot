#!/usr/bin/python3
# coding=utf-8

# EC AntiSpam bot for Telegram Messenger
# Copyright (c) 2017 - 2018 EasyCoding Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re


class CheckUsername:
    @classmethod
    def __find_methods(cls, prefix: str) -> set:
        """
        Find available check methods to call them dynamically later.
        :param prefix: Prefix for check methods.
        :return: Set with available methods.
        """
        return {s for s in cls.__dict__.keys() if s.startswith(prefix)}

    def check_chinese_bots(self) -> int:
        """
        Find chinese bots and score them to +100.
        :return: Score result.
        """
        return 100 if re.search(self.__settings.chkrgx, self.__username, re.I | re.M | re.U) else 0

    def check_with_url(self) -> int:
        """
        Check and score users with URLs in username.
        :return: Score result.
        """
        return 100 if re.search(self.__settings.urlrgx, self.__username, re.I | re.M | re.U) else 0

    def check_restricted_words(self) -> int:
        """
        Check and score users with restricted words in username.
        :return: Score result.
        """
        return 100 if any(w in self.__username for w in self.__settings.stopwords) else 0

    def check_too_long(self) -> int:
        """
        Check and score users with very long usernames.
        :return: Score result.
        """
        return 50 if len(self.__username) > self.__settings.maxname else 0

    def check_hieroglyphs(self) -> int:
        """
        Check and score users with chinese hieroglyphs.
        :return: Score result.
        """
        return 50 if re.search('[\u4e00-\u9fff]+', self.__username, re.I | re.M | re.U) else 0

    @property
    def score(self) -> int:
        """
        Return final score after running checks.
        :return: Final score.
        """
        score = 0
        for chk in self.__scorers:
            score += getattr(self, chk)()
        return score

    def __init__(self, fname, lname, settings) -> None:
        """
        Main constructor of CheckUsername class.
        :param fname: First name.
        :param lname: Last name.
        :param settings: Object of Settings class.
        """
        self.__username = '{} {}'.format(fname, lname) if lname else fname
        self.__settings = settings
        self.__scorers = self.__find_methods('check')