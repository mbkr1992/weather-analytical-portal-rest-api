def parse_order_by(order_by):
    if order_by:
        def to_order(v):
            key, _, value = v.partition(':')
            return '{} {}'.format(key, value)

        values = order_by.split('|')
        separated_values = [to_order(value) for value in values]
        return ','.join(separated_values)
    return 'date DESC'


def parse_path(path):
    if path:
        def to_latlon(v):
            lat, _, lon = v.partition(',')
            return '{} {}'.format(lat, lon)

        values = path.split('|')
        separated_values = [to_latlon(value) for value in values]
        polygon = 'LINESTRING({})'.format(','.join(separated_values))
        return polygon
    return None

