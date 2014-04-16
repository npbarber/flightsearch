def build_url(base_url, depdate, retdate, origin, dest, num_pax):
    dep_month, dep_day, _ = depdate.split('/')
    ret_month, ret_day, _ = retdate.split('/')
    result = '%s/%s-to-%s#!' % (base_url, origin, dest)
    result += 'dates=%s%s' % (_map_month(dep_month), dep_day)
    result += ',%s%s' % (_map_month(ret_month), ret_day)
    result += '&pax=%s' % num_pax
    return result



def _map_month(month):
    month_map = {
        '01': 'Jan',
        '02': 'Feb',
        '03': 'Mar',
        '04': 'Apr',
        '05': 'May',
        '06': 'Jun',
        '07': 'Jul',
        '08': 'Aug',
        '09': 'Sep',
        '10': 'Oct',
        '11': 'Nov',
        '12': 'Dec',
    }
    return month_map.get(month)
