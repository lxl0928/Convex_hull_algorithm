# coding: utf-8
from math import sin, cos, radians, degrees, atan2, asin, sqrt
from decimal import Decimal


class HullAlgorithm(object):
    @classmethod
    def get_coordinates_by_offset(cls, points, offset=0.00045):
        """

        :param points:
        :param offset:  表示便宜0.00045°
        :return:
        """
        offset = Decimal("{}".format(offset))
        res_points = cls.make_hull(points=points)
        center_point = cls.getOnePolyygen(geolocations=points)
        cent_lng, cent_lat = center_point
        latest_points = []
        print("中心点: {}".format(center_point))
        for coor in res_points:
            lng, lat = coor[0], coor[1]  # Decimal参与计算，需要转成float
            # print("偏移前: {}".format((lng, lat)))
            if lng >= cent_lng:
                lng += offset
            else:
                lng -= offset

            if lat >= cent_lat:
                lat += offset
            else:
                lat -= offset
            latest_points.append(
                (lng, lat)
            )
            print("偏移后: {}".format((lng, lat)))
        return latest_points, center_point

    @classmethod
    def make_hull(cls, points):
        return cls.make_hull_presorted(sorted(points))

    @classmethod
    def make_hull_presorted(cls, points):
        if len(points) <= 1:
            return list(points)

        # Andrew's monotone chain algorithm. Positive y coordinates correspond to "up"
        # as per the mathematical convention, instead of "down" as per the computer
        # graphics convention. This doesn't affect the correctness of the result.

        upperhull = []
        lowerhull = []
        for hull in (upperhull, lowerhull):
            for p in (points if (hull is upperhull) else reversed(points)):
                while len(hull) >= 2:
                    qx, qy = hull[-1]
                    rx, ry = hull[-2]
                    if (qx - rx) * (p[1] - ry) >= (qy - ry) * (p[0] - rx):
                        del hull[-1]
                    else:
                        break
                hull.append(p)
            del hull[-1]

        if not (len(upperhull) == 1 and upperhull == lowerhull):
            upperhull.extend(lowerhull)
        return upperhull

    @classmethod
    def center_geolocation(cls, geolocations):
        """
        输入多个经纬度坐标(格式：[[lon1, lat1],[lon2, lat2],....[lonn, latn]])，找出中心点
        :param geolocations:
        :return:中心点坐标  [lon,lat]
        """
        """
        # 求平均数  同时角度弧度转化 得到中心点
        x = 0  # lon
        y = 0  # lat
        z = 0
        lenth = len(geolocations)
        for lon, lat in geolocations:
            lon = radians(float(lon))
            #  radians(float(lon))   Convert angle x from degrees to radians
            # 	                    把角度 x 从度数转化为 弧度
            lat = radians(float(lat))
            x += cos(lat) * cos(lon)
            y += cos(lat) * sin(lon)
            z += sin(lat)
            x = float(x / lenth)
            y = float(y / lenth)
            z = float(z / lenth)
            print("{}, {}: {}, {}, {}".format(lon, lat, x, y, z))
        return degrees(atan2(y, x)), degrees(atan2(z, sqrt(x * x + y * y)))
        """
        average_lng, average_lat = 0, 0
        length = len(geolocations)
        if length:
            all_lng = sum([abs(item[0]) for item in geolocations])
            all_lat = sum([abs(item[1]) for item in geolocations])
            return all_lng / length, all_lat / length

    # 得到离中心点里程最近的里程
    @classmethod
    def geodistance(cls, lon1, lat1, lon2, lat2):
        """
        得到两个经纬度坐标距离 单位为千米 （计算不分前后顺序）
        :param lon1: 第一个坐标 维度
        :param lat1: 第一个坐标 经度
        :param lon2: 第二个坐标 维度
        :param lat2: 第二个坐标 经度
        :return: distance 单位千米
        """
        # lon1,lat1,lon2,lat2 = (120.12802999999997,30.28708,115.86572000000001,28.7427)
        lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])  # 经纬度转换成弧度
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        distance = 2 * asin(sqrt(a)) * 6371.393 * 1000  # 地球平均半径，6371km
        distance = round(distance / 1000, 3)
        return distance

    @classmethod
    def getMaxestDistance(cls, geolocations, centre):
        """
        中心点 距离 多个经纬度左边 最远的距离
        :param geolocations: 多个经纬度坐标(格式：[[lon1, lat1],[lon2, lat2],....[lonn, latn]])
        :param centre: 中心点   centre [lon,lat]
        :return: 最远距离  千米
        """
        distantces = []
        for lon, lat in geolocations:
            d = cls.geodistance(lat, lon, centre[1], centre[0])
            print(lon, lat, d)
            distantces.append(d)
        return max(distantces)

    @classmethod
    def getOnePolyygen(cls, geolocations):
        """
        输入多个经纬度坐标(格式：[[lon1, lat1],[lon2, lat2],....[lonn, latn]])，找出距该多边形中心点最远的距离
        :param geolocations:多个经纬度坐标(格式：[[lon1, lat1],[lon2, lat2],....[lonn, latn]])
        :return:center,neartDistance  多边形中心点  最远距离
        """
        center = cls.center_geolocation(geolocations)  # 得到中心点
        # neartDistance = cls.getMaxestDistance(geolocations=geolocations, centre=center)
        return center

