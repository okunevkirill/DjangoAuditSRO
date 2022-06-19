"""
Module with parsing logic on the site The National Association of
Stock Market Participants (NAUFOR) is a non-profit self-regulatory
 organization in the Russian financial market.
"""

import scrapy

_HOST = 'https://naufor.ru'


class NauforSpider(scrapy.Spider):
    name = 'naufor'
    start_urls = [_HOST]

    def parse(self, response, **kwargs):
        """Search on the main page of the site for links to the register of members"""
        link = response.css("div.main-top-member p a::attr('href')").get()
        if link is None:
            raise ConnectionError('No connection to site')

        link = self.get_absolute_url(link)
        yield response.follow(link, callback=self.parse_register_of_members)

    def parse_register_of_members(self, response):
        """Getting links to pages with information about the organization"""
        for link in response.css("div.tbl1 td a::attr('href')").getall():
            if link is None:
                continue
            yield response.follow(
                self.get_absolute_url(link.strip()),
                callback=self.parse_organization
            )

    def parse_organization(self, response):
        """Collection of necessary information about a member of a self-regulatory organization"""
        data = self._get_data_company(response)
        data['info_url'] = response.url
        yield data

    @staticmethod
    def get_absolute_url(url: str) -> str:
        """Converts a relative path to an absolute"""
        if url.startswith(('https:', 'http:')):
            return url
        return f'{_HOST}{url}'

    @staticmethod
    def _get_data_company(response) -> dict:
        """Collects data on the organization from html layout"""

        # ToDo - Подумать об упрощении логики сбора информации (возможно `regex`)
        data = dict(name='', tax_number='', legal_address='', verification_date='', info='')
        response_list = response.css("table td").getall()
        start_idx, end_idx = 0, 0
        is_search_date = False
        for index, tag_content in enumerate(response_list):
            if "Наименование организации на русском языке" in tag_content:
                # Имя компании идёт во 2 теге после текущего
                data['name'] = response_list[index + 2].replace('<td>', '').replace('</td>', '').strip()
            elif "1.5 Адрес юридического лица" in tag_content:
                # Юридический адрес в 1 теге после текущего
                data['legal_address'] = response_list[index + 1].replace(
                    '<td colspan="2">', '').replace('</td>', '').strip()
            elif "3.1 Идентификационный номер налогоплательщика" in tag_content:
                # ИНН в 1 теге после текущего
                data['tax_number'] = response_list[index + 1].replace(
                    '<td colspan="2">', '').replace('</td>', '').strip()
            elif "6.1 Дата начала и дата окончания проверки" in tag_content:
                # С данного индекса идёт нужная информация
                start_idx = index
                is_search_date = True
            elif "7.1 Мера" in tag_content or "Мер не назначено" in tag_content:
                # На данном индексе нужная информация заканчивается
                end_idx = index
                is_search_date = False

            if is_search_date and "<td><b>Д</b>ата окончания</td>" in tag_content:
                # дата проверки в 1 теге после текущего (будет обновляться последней из списка)
                data['verification_date'] = response_list[index + 1].replace('<td>', '').replace('</td>', '').strip()

        if start_idx < end_idx:
            text = ''.join(response_list[start_idx: end_idx])
            text = text.replace('* * *', '').replace(
                '<td colspan="2">', '\n').replace('<td>', ' ').replace(
                '</td>', ' ').replace('<b>', '').replace('</b>', '').strip()
            data['info'] = text

        return data
