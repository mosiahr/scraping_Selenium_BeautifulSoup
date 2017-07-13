#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import csv
import requests
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://aquaterm-lux.com.ua'

BASE_URL = 'https://aquaterm-lux.com.ua/g7286801-rasshiritelnye-baki-elbi'

FILE = 'aquaterm_10.csv'


def get_html(url):
    response = requests.get(url)
    return response.content.decode('utf-8')


def get_category(html):
    soup = BeautifulSoup(html, 'html.parser')
    groups = soup.find('div', class_='b-product-groups-gallery')
    categories = groups.find_all('a', class_='b-product-groups-gallery__title-link')
    categories = ['{}{}'.format(BASE, category['href']) for category in categories]
    return categories


def get_link_el(html):
    soup = BeautifulSoup(html, 'html.parser')
    pages_all = []
    content = soup.find('div', class_='b-layout__clear')
    pages = content.find_all('a', class_='b-product-line__product-name-link')
    pages = [page['href'] for page in pages]
    pages_all.extend(pages)
    return pages_all


def get_page(html, url):
    pg = []
    soup = BeautifulSoup(html, 'html.parser')
    try:
        page_count = soup.find('div', class_='b-pager').find_all('a')
        page_count = [int(p['href'].split('/page_')[-1]) for p in page_count]
        page_count = max(page_count)
    except Exception:
        page_count = 1

    for p in range(1, page_count+1):
        pg.append('{}/page_{}'.format(url, p))
    return pg


def parser(html):
    soup = BeautifulSoup(html, 'html.parser')
    name = soup.find('h1', class_='b-title b-title_type_b-product').text.strip()
    try:
        price = soup.find('p', class_='b-product__price')
        price = price.find_all('span')[0]['content']
    except Exception:
        price = None
    if soup.find('div', class_='b-content__body b-user-content').h2:
        description = soup.find('div', class_='b-content__body b-user-content')
        h = description.h2
        description = [re.sub(r'\s+', ' ', el.text) for el in h.find_all_previous('p') if el in description]
        description.reverse()
        description = ' '.join(description)
    else:
        description = re.sub(r'\s+', ' ', soup.find('div', class_='b-content__body b-user-content').text)

    categories = soup.find('div', class_='path b-breadcrumb__bar')
    categories = categories.find_all('a', class_='b-breadcrumb__link')
    categories = [re.sub(r'\s+', ' ', cat.text).strip() for cat in categories]
    category1 = category2 = None
    try:
        category = categories[2]
    except Exception:
        category = None
    try:
        if categories[3] != name:
            category1 = categories[3]
    except Exception:
        category1 = None
    try:
        if categories[4] != name:
            category2 = categories[4]
    except Exception:
        category2 = None

    product_info = soup.find('table', class_='b-product-info')
    product_info = product_info.find_all('tr')
    product_info = {'{}'.format(re.sub(r'\s+', ' ', p.find_all('td')[0].text)).strip():
                    '{}'.format(re.sub(r'\s+', ' ', p.find_all('td')[1].text)).strip()
                    for p in product_info if p.find_all('td')}

    try:
        country = product_info['Страна производитель']
    except Exception:
        country = None
    try:
        manufacturer = product_info['Производитель']
    except Exception:
        manufacturer = None
    try:
        type_pump = product_info['Вид насоса']
    except Exception:
        type_pump = None
    try:
        if product_info['Способ установки насоса']:
            installation_method = product_info['Способ установки насоса']
        elif product_info['Способ установки']:
            installation_method = product_info['Способ установки']
        else:
            installation_method = None
    except Exception:
        installation_method = None
    try:
        max_pressure = product_info['Максимальный напор']
    except Exception:
        max_pressure = None
    try:
        throughput = product_info['Пропускная способность']
    except Exception:
        throughput = None
    try:
        if product_info['Потребляемая мощность']:
            power = product_info['Потребляемая мощность']
        elif product_info['Мощность']:
            power = product_info['Мощность']
        else:
            power = None
    except Exception:
        power = None
    try:
        voltage_network = product_info['Напряжение сети']
    except Exception:
        voltage_network = None
    try:
        if product_info['Частота']:
            current_frequency = product_info['Частота']
        elif product_info['Частота тока']:
            current_frequency = product_info['Частота тока']
        else:
            current_frequency = None
    except Exception:
        current_frequency = None
    try:
        increase_pressure = product_info['Повышение давления']
    except Exception:
        increase_pressure = None
    try:
        max_immersion_depth = product_info['Максимальная глубина погружения']
    except Exception:
        max_immersion_depth = None
    try:
        water_quality = product_info['Качество воды']
    except Exception:
        water_quality = None
    try:
        min_temp_work_fluid = product_info['Минимальная температура рабочей жидкости']
    except Exception:
        min_temp_work_fluid = None
    try:
        max_temp_work_fluid = product_info['Максимальная температура рабочей жидкости']
    except Exception:
        max_temp_work_fluid = None
    try:
        diameter_pumped_particles = product_info['Диаметр перекачиваемых частиц']
    except Exception:
        diameter_pumped_particles = None
    try:
        weight = product_info['Вес']
    except Exception:
        weight = None
    try:
        guarantee_period = product_info['Гарантийный срок']
    except Exception:
        guarantee_period = None

    try:
        width = product_info['Ширина']
    except Exception:
        width = None
    try:
        length = product_info['Длина']
    except Exception:
        length = None
    try:
        height = product_info['Высота']
    except Exception:
        height = None

    try:
        cutting_attachment = product_info['Режущая насадка']
    except Exception:
        cutting_attachment = None
    try:
        volume_tank = product_info['Объем гидробака']
    except Exception:
        volume_tank = None
    try:
        installing_pump = product_info['Установка насоса']
    except Exception:
        installing_pump = None
    try:
        housing_material = product_info['Материал корпуса']
    except Exception:
        housing_material = None
    try:
        class_protection_electronic_equipment = product_info['Класс защиты корпусов электронного оборудования']
    except Exception:
        class_protection_electronic_equipment = None
    try:
        connector_diameter = product_info['Диаметр разъема соединения']
    except Exception:
        connector_diameter = None
    try:
        length_power_cord = product_info['Длина сетевого шнура']
    except Exception:
        length_power_cord = None
    try:
        max_suction_depth = product_info['Максимальная глубина всасывания']
    except Exception:
        max_suction_depth = None

    try:
        total_volume_tank = product_info['Общий объём резервуара (ов)']
    except Exception:
        total_volume_tank = None
    try:
        type_pump_switch = product_info['Тип выключателя насоса']
    except Exception:
        type_pump_switch = None
    try:
        automatic_level_control_working_environment = product_info['Автоматический контроль уровня рабочей среды  ']
    except Exception:
        automatic_level_control_working_environment = None
    try:
        if product_info['Потребляемая мощность']:
            power_consumption = product_info['Потребляемая мощность']
        elif product_info['Потребляемая мощность (W)']:
            power_consumption = product_info['Потребляемая мощность (W)']
        else:
            power_consumption = None
    except Exception:
        power_consumption = None

    try:
        maximum_throughput = product_info['Максимальная пропускная способность']
    except Exception:
        maximum_throughput = None
    try:
        pumped_media = product_info['Перекачиваемые среды']
    except Exception:
        pumped_media = None
    try:
        count_pumps = product_info['Количество насосов']
    except Exception:
        count_pumps = None
    try:
        overheat_protection = product_info['Защита от перегрева']
    except Exception:
        overheat_protection = None
    try:
        power_factor = product_info['Коэффициент мощности']
    except Exception:
        power_factor = None
    try:
        number_poles = product_info['Количество полюсов']
    except Exception:
        number_poles = None
    try:
        rotation_frequency = product_info['Частота вращения']
    except Exception:
        rotation_frequency = None
    try:
        ratio = product_info['Отношение максимального момента к номинальному моменту']
    except Exception:
        ratio = None
    try:
        efficiency = product_info['КПД, не менее']
    except Exception:
        efficiency = None
    try:
        degree_protection_IP = product_info['Степень защиты IP']
    except Exception:
        degree_protection_IP = None
    try:
        maximum_ambient_temperature = product_info['Максимальная температура окружающей среды']
    except Exception:
        maximum_ambient_temperature = None
    try:
        scope = product_info['Объем']
    except Exception:
        scope = None
    try:
        maximum_working_pressure = product_info['Максимальное рабочее давление']
    except Exception:
        maximum_working_pressure = None
    try:
        max_operating_temperature = product_info['Максимальная рабочая температура']
    except Exception:
        max_operating_temperature = None
    try:
        location_accumulator = product_info['Расположение гидроаккумулятора']
    except Exception:
        location_accumulator = None
    try:
        diameter = product_info['Диаметр']
    except Exception:
        diameter = None
    try:
        diameter_connecting_pipe = product_info['Диаметр присоединительного патрубка']
    except Exception:
        diameter_connecting_pipe = None
    try:
        tank_material = product_info['Материал резервуара']
    except Exception:
        tank_material = None
    try:
        tank_volume = product_info['Объем резервуара']
    except Exception:
        tank_volume = None
    try:
        maximum_filling_capacity_tank = product_info['Максимальный объем наполнения резервуара']
    except Exception:
        maximum_filling_capacity_tank = None
    try:
        wall_thickness = product_info['Толщина стенок']
    except Exception:
        wall_thickness = None
    try:
        type_tank_according_to_installation = product_info['Тип резервуара по способу установки']
    except Exception:
        type_tank_according_to_installation = None
    try:
        tank_type_installation = product_info['Тип резервуара по способу монтажа']
    except Exception:
        tank_type_installation = None
    try:
        tank_type_number_walls = product_info['Тип резервуара по количеству стенок']
    except Exception:
        tank_type_number_walls = None
    try:
        tank_type_number_sections = product_info['Тип резервуара по количеству секций']
    except Exception:
        tank_type_number_sections = None
    try:
        maximum_temperature_working_medium = product_info['Максимальная температура рабочей среды']
    except Exception:
        maximum_temperature_working_medium = None
    try:
        inspection_hole_d = product_info['Смотровое отверстие d']
    except Exception:
        inspection_hole_d = None
    try:
        volume_expansion_vessel = product_info['Объем расширительного бака']
    except Exception:
        volume_expansion_vessel = None
    try:
        type_expansion_tank = product_info['Тип расширительного бака']
    except Exception:
        type_expansion_tank = None
    try:
        design_tank = product_info['Конструктивное исполнение бака']
    except Exception:
        design_tank = None
    try:
        membrane_material = product_info['Материал мембраны']
    except Exception:
        membrane_material = None
    try:
        with_replaceable_diaphragm = product_info['С заменяемой мембраной']
    except Exception:
        with_replaceable_diaphragm = None
    try:
        colour = product_info['Цвет']
    except Exception:
        colour = None

    img = soup.find('div', class_='b-product__image-panel')
    img = img.find('img')['src'].strip()

    products = {
        'name': name,
        'price': price,
        'description': description,
        # 'product_info': product_info,
        'img': img,
        'category': category,
        'category1': category1,
        'category2': category2,

        'country': country,
        'manufacturer': manufacturer,
        'type_pump': type_pump,
        'installation_method': installation_method,

        'max_pressure': max_pressure,
        'throughput': throughput,
        'power': power,
        'voltage_network': voltage_network,
        'current_frequency': current_frequency,
        'increase_pressure': increase_pressure,
        'max_immersion_depth': max_immersion_depth,
        'water_quality': water_quality,
        'min_temp_work_fluid': min_temp_work_fluid,
        'max_temp_work_fluid': max_temp_work_fluid,
        'diameter_pumped_particles': diameter_pumped_particles,

        'weight': weight,
        'guarantee_period': guarantee_period,

        'width': width,
        'length': length,
        'height': height,

        'cutting_attachment': cutting_attachment,

        'volume_tank': volume_tank,
        'installing_pump': installing_pump,
        'class_protection_electronic_equipment': class_protection_electronic_equipment,
        'connector_diameter': connector_diameter,
        'length_power_cord': length_power_cord,
        'max_suction_depth': max_suction_depth,

        'total_volume_tank': total_volume_tank,
        'type_pump_switch': type_pump_switch,
        'automatic_level_control_working_environment': automatic_level_control_working_environment,
        'power_consumption': power_consumption,
        'maximum_throughput': maximum_throughput,
        'pumped_media': pumped_media,
        'count_pumps': count_pumps,

        'overheat_protection': overheat_protection,
        'power_factor': power_factor,
        'number_poles': number_poles,
        'rotation_frequency': rotation_frequency,
        'ratio': ratio,
        'efficiency': efficiency,
        'degree_protection_IP': degree_protection_IP,
        'maximum_ambient_temperature': maximum_ambient_temperature,
        'scope': scope,
        'maximum_working_pressure': maximum_working_pressure,
        'max_operating_temperature': max_operating_temperature,
        'location_accumulator': location_accumulator,
        'diameter': diameter,
        'diameter_connecting_pipe': diameter_connecting_pipe,
        'housing_material': housing_material,

        'tank_material': tank_material,
        'tank_volume': tank_volume,
        'maximum_filling_capacity_tank': maximum_filling_capacity_tank,
        'wall_thickness': wall_thickness,
        'type_tank_according_to_installation': type_tank_according_to_installation,
        'tank_type_installation': tank_type_installation,
        'tank_type_number_walls': tank_type_number_walls,
        'tank_type_number_sections': tank_type_number_sections,
        'maximum_temperature_working_medium': maximum_temperature_working_medium,
        'inspection_hole_d': inspection_hole_d,

        'volume_expansion_vessel': volume_expansion_vessel,
        'type_expansion_tank': type_expansion_tank,
        'design_tank': design_tank,
        'membrane_material': membrane_material,
        'with_replaceable_diaphragm': with_replaceable_diaphragm,
        'colour': colour,
    }
    return products


def save(products, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow((
            'Имя',
            'Категория',
            'Категория1',
            'Категория2',
            'Цена',
            'URL картинки',
            'Описание',

            'Страна производитель',
            'Производитель',
            'Вид насоса',
            'Способ установки',

            'Максимальный напор',
            'Пропускная способность',
            'Потребляемая мощность',
            'Напряжение сети',
            'Частота',
            'Повышение давления',
            'Максимальная глубина погружения',
            'Качество воды',
            'Минимальная температура рабочей жидкости',
            'Максимальная температура рабочей жидкости',
            'Диаметр перекачиваемых частиц',
            'Вес',
            'Гарантийный срок',

            'Ширина',
            'Длина',
            'Высота',
            'Режущая насадка',

            'Объем гидробака',
            'Установка насоса',
            'Материал корпуса',
            'Класс защиты корпусов электронного оборудования',
            'Диаметр разъема соединения',
            'Длина сетевого шнура',
            'Максимальная глубина всасывания',

            'Общий объём резервуара (ов)',
            'Тип выключателя насоса',
            'Автоматический контроль уровня рабочей среды',
            'Потребляемая мощность',
            'Максимальная пропускная способность',
            'Перекачиваемые среды',
            'Количество насосов',

            'Защита от перегрева',
            'Коэффициент мощности',
            'Количество полюсов',
            'Частота вращения',
            'Отношение максимального момента к номинальному моменту',
            'КПД, не менее',
            'Степень защиты IP',
            'Максимальная температура окружающей среды',
            'Объем',
            'Максимальное рабочее давление',
            'Максимальная рабочая температура',
            'Расположение гидроаккумулятора',
            'Диаметр',
            'Диаметр присоединительного патрубка',

            'Материал резервуара',
            'Объем резервуара',
            'Максимальный объем наполнения резервуара',
            'Толщина стенок',
            'Тип резервуара по способу установки',
            'Тип резервуара по способу монтажа',
            'Тип резервуара по количеству стенок',
            'Тип резервуара по количеству секций',
            'Максимальная температура рабочей среды',
            'Смотровое отверстие d',

            'Объем расширительного бака',
            'Тип расширительного бака',
            'Конструктивное исполнение бака',
            'Материал мембраны',
            'С заменяемой мембраной',
            'Цвет',
         ))

        for product in products:
            writer.writerow((
                (product['name']),
                (product['category']),
                (product['category1']),
                (product['category2']),
                (product['price']),
                (product['img']),
                (product['description']),

                (product['country']),
                (product['manufacturer']),
                (product['type_pump']),
                (product['installation_method']),
                (product['max_pressure']),
                (product['throughput']),
                (product['power']),
                (product['voltage_network']),
                (product['current_frequency']),
                (product['increase_pressure']),
                (product['max_immersion_depth']),
                (product['water_quality']),
                (product['min_temp_work_fluid']),
                (product['max_temp_work_fluid']),
                (product['diameter_pumped_particles']),

                (product['weight']),
                (product['guarantee_period']),
                (product['width']),
                (product['length']),
                (product['height']),

                (product['cutting_attachment']),
                (product['volume_tank']),
                (product['installing_pump']),
                (product['housing_material']),
                (product['class_protection_electronic_equipment']),
                (product['connector_diameter']),
                (product['length_power_cord']),
                (product['max_suction_depth']),

                (product['total_volume_tank']),
                (product['type_pump_switch']),
                (product['automatic_level_control_working_environment']),
                (product['power_consumption']),
                (product['maximum_throughput']),
                (product['pumped_media']),
                (product['count_pumps']),

                (product['overheat_protection']),
                (product['power_factor']),
                (product['number_poles']),
                (product['rotation_frequency']),
                (product['ratio']),
                (product['efficiency']),
                (product['degree_protection_IP']),
                (product['maximum_ambient_temperature']),
                (product['scope']),
                (product['maximum_working_pressure']),
                (product['max_operating_temperature']),
                (product['location_accumulator']),
                (product['diameter']),
                (product['diameter_connecting_pipe']),
                (product['tank_material']),
                (product['tank_volume']),
                (product['maximum_filling_capacity_tank']),
                (product['wall_thickness']),
                (product['type_tank_according_to_installation']),
                (product['tank_type_installation']),
                (product['tank_type_number_walls']),
                (product['tank_type_number_sections']),
                (product['maximum_temperature_working_medium']),
                (product['inspection_hole_d']),
                (product['volume_expansion_vessel']),
                (product['type_expansion_tank']),
                (product['design_tank']),
                (product['membrane_material']),
                (product['with_replaceable_diaphragm']),
                (product['colour']),
            ))


def main():
    print('Scrape START')
    print('-------------------------------')
    products = []
    link_all = []

    pages = get_page(get_html(BASE_URL), BASE_URL)
    for p in pages:
        link_all.extend(get_link_el(get_html(p)))

    for link in link_all:
        print("Scrape:", link)
        products.append(parser(get_html(link)))

    save(products, FILE)
    print('-------------------------------')
    print('All data is saved to the %s.' % FILE)
    print('Scrape END')

if __name__ == '__main__':
    main()

