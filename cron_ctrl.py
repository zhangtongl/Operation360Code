#!/usr/bin/env python 
# �������������windows�µ������������
#�������������һ��frame ���� ��linux�û��µ�crontab ��ʱ���� �������������Լ��ܼ�����ʱ�����״̬������Щ��ʱ���� �������ܣ�����������������/�رգ��ոսӴ�pythoh ʵ���������������
# ����ֻ��pythonʵ�ֵĽ���crontab�����ļ�����

import re, time, sys
from Core.FDateTime.FDateTime import FDateTime
  
def get_struct_time(time_stamp_int):
    """
    ������ʱ�����ȡ��ʽ��ʱ�� �� ʱ �� �� ��
    Args:
        time_stamp_int Ϊ�����ֵΪʱ���(����)���磺1332888820
        ����localtimeת������
        time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    Return:
        list____���� �� ʱ �� �� ��
    """
  
    st_time = time.localtime(time_stamp_int)
    return [st_time.tm_min, st_time.tm_hour, st_time.tm_mday, st_time.tm_mon, st_time.tm_wday]
  
  
def get_strptime(time_str, str_format):
    """���ַ�����ȡ ����ʱ���
    Args:
        time_str �ַ������͵�ʱ��� �� '31/Jul/2013:17:46:01'
        str_format ָ�� time_str �ĸ�ʽ �� '%d/%b/%Y:%H:%M:%S'
    Return:
        ����10λ����(int)ʱ������� 1375146861
    """
    return int(time.mktime(time.strptime(time_str, str_format)))
  
def get_str_time(time_stamp, str_format='%Y%m%d%H%M'):
    """
    ��ȡʱ���,
    Args:
        time_stamp 10λ����(int)ʱ������� 1375146861
        str_format ָ�����ظ�ʽ��ֵ����Ϊ �ַ��� str
    Rturn:
        ���ظ�ʽ Ĭ��Ϊ ������ʱ�֣���2013��7��9��1ʱ3�� :201207090103
    """
    return time.strftime("%s" % str_format, time.localtime(time_stamp))
  
def match_cont(patten, cont):
    """
    ����ƥ��(��ȷ���ϵ�ƥ��)
    Args:
        patten ������ʽ
        cont____ ƥ������
    Return:
        True or False
    """
    res = re.match(patten, cont)
    if res:
        return True
    else:
        return False
  
def handle_num(val, ranges=(0, 100), res=list()):
    """��������"""
    val = int(val)
    if val >= ranges[0] and val <= ranges[1]:
        res.append(val)
    return res
  
def handle_nlist(val, ranges=(0, 100), res=list()):
    """���������б� �� 1,2,3,6"""
    val_list = val.split(',')
    for tmp_val in val_list:
        tmp_val = int(tmp_val)
        if tmp_val >= ranges[0] and tmp_val <= ranges[1]:
            res.append(tmp_val)
    return res
  
def handle_star(val, ranges=(0, 100), res=list()):
    """�����Ǻ�"""
    if val == '*':
        tmp_val = ranges[0]
        while tmp_val <= ranges[1]:
            res.append(tmp_val)
            tmp_val = tmp_val + 1
    return res
  
def handle_starnum(val, ranges=(0, 100), res=list()):
    """�Ǻ�/���� ��� �� */3"""
    tmp = val.split('/')
    val_step = int(tmp[1])
    if val_step < 1:
        return res
    val_tmp = int(tmp[1])
    while val_tmp <= ranges[1]:
        res.append(val_tmp)
        val_tmp = val_tmp + val_step
    return res
  
def handle_range(val, ranges=(0, 100), res=list()):
    """�������� �� 8-20"""
    tmp = val.split('-')
    range1 = int(tmp[0])
    range2 = int(tmp[1])
    tmp_val = range1
    if range1 < 0:
        return res
    while tmp_val <= range2 and tmp_val <= ranges[1]:
        res.append(tmp_val)
        tmp_val = tmp_val + 1
    return res
  
def handle_rangedv(val, ranges=(0, 100), res=list()):
    """��������/���� ��� �� 8-20/3 """
    tmp = val.split('/')
    range2 = tmp[0].split('-')
    val_start = int(range2[0])
    val_end = int(range2[1])
    val_step = int(tmp[1])
    if (val_step < 1) or (val_start < 0):
        return res
    val_tmp = val_start
    while val_tmp <= val_end and val_tmp <= ranges[1]:
        res.append(val_tmp)
        val_tmp = val_tmp + val_step
    return res
  
def parse_conf(conf, ranges=(0, 100), res=list()):
    """����crontab ���ʱ������е�����һ��"""
    #ȥ���ո��ٲ��
    conf = conf.strip(' ').strip(' ')
    conf_list = conf.split(',')
    other_conf = []
    number_conf = []
    for conf_val in conf_list:
        if match_cont(PATTEN['number'], conf_val):
            #��¼��ֺ�Ĵ����ֲ���
            number_conf.append(conf_val)
        else:
            #��¼��ֺ���������Ĳ�������ͨ��� * , ���� 0-8, �� 0��8/3 ֮��
            other_conf.append(conf_val)
    if other_conf:
        #������������ֲ���
        for conf_val in other_conf:
            for key, ptn in PATTEN.items():
                if match_cont(ptn, conf_val):
                    res = PATTEN_HANDLER[key](val=conf_val, ranges=ranges, res=res)
    if number_conf:
        if len(number_conf) > 1 or other_conf:
            #�����ֶ���1���������������������棬��������Ϊʱ���б�
            res = handle_nlist(val=','.join(number_conf), ranges=ranges, res=res)
        else:
            #ֻ��һ�������ִ��ڣ�������Ϊʱ�� ���
            res = handle_num(val=number_conf[0], ranges=ranges, res=res)
    return res
  
def parse_crontab_time(conf_string):
    """
    ����crontabʱ�����ò���
    Args:
        conf_string  ��������(�����ֵ���� ʱ �� �� ��)
                     ȡֵ��Χ ����:0-59 Сʱ:1-23 ����:1-31 �·�:1-12 ����:0-6(0��ʾ����)
    Return:
    crontab_range    list��ʽ���� ʱ �� �� �� �����������ֱ��Ӧ��ȡֵ��Χ
    """
    time_limit  = ((0, 59), (1, 23), (1, 31), (1, 12), (0, 6))
    crontab_range = []
    clist = []
    conf_length = 5
    tmp_list = conf_string.split(' ')
    for val in tmp_list:
        if len(clist) == conf_length:
            break
        if val:
            clist.append(val)
  
    if len(clist) != conf_length:
        return -1, 'config error whith [%s]' % conf_string
    cindex = 0
    for conf in clist:
        res_conf = []
        res_conf = parse_conf(conf, ranges=time_limit[cindex], res=res_conf)
        if not res_conf:
            return -1, 'config error whith [%s]' % conf_string
        crontab_range.append(res_conf)
        cindex = cindex + 1
    return 0, crontab_range
  
def time_match_crontab(crontab_time, time_struct):
    """
    ��ʱ�����crontab������һ��ʱ������Աȣ��жϸ�ʱ����Ƿ��������趨��ʱ�䷶Χ��
    Args:
        crontab_time____crontab�����е����ʱ�䣨�� ʱ �� �� ��)������Ӧʱ��ȡֵ��Χ
        time_struct____ ĳ������ʱ������磺1375027200 ��Ӧ�� �� ʱ �� �� ��
    Return:
    tuple ״̬��, ״̬����
    """
    cindex = 0
    for val in time_struct:
        if val not in crontab_time[cindex]:
            return 0, False
        cindex = cindex + 1
    return 0, True
  
def close_to_cron(crontab_time, time_struct):
    """coron��ָ����Χ(crontab_time)�� ��ӽ� ָ��ʱ�� time_struct ��ֵ"""
    close_time = time_struct
    cindex = 0
    for val_struct in time_struct:
        offset_min = val_struct
        val_close = val_struct
        for val_cron in crontab_time[cindex]:
            offset_tmp = val_struct - val_cron
            if offset_tmp > 0 and offset_tmp < offset_min:
                val_close = val_struct
                offset_min = offset_tmp
        close_time[cindex] = val_close
        cindex = cindex + 1
    return close_time
  
def cron_time_list(
        cron_time,
        year_num=int(get_str_time(time.time(), "%Y")),
        limit_start=get_str_time(time.time(), "%Y%m%d%H%M"),
        limit_end=get_str_time(time.time() + 86400, "%Y%m%d%H%M")
    ):
    #print "\nfrom ", limit_start , ' to ' ,limit_end
    """
    ��ȡcrontabʱ�����ò���ȡֵ��Χ�ڵ�����ʱ��� �� ʱ���
    Args:
        cron_time ����crontab����ָ��������ʱ���
        year_num____ָ������һ���� ��ȡ
        limit_start ��ʼʱ��
    Rturn:
        List  ����ʱ�����ɵ��б�(������ʱ�� ��ɵ�ʱ�䣬��2013��7��29��18ʱ56�֣�201307291856)
    """
    #��Сʱ �� ������װ
    hour_minute = []
    for minute in cron_time[0]:
        minute = str(minute)
        if len(minute) < 2:
            minute = '0%s' % minute
        for hour in cron_time[1]:
            hour = str(hour)
            if len(hour) < 2:
                hour = '0%s' % hour
            hour_minute.append('%s%s' % (hour, minute))
    #���� �� Сʱ��װ
    day_hm = []
    for day in cron_time[2]:
        day = str(day)
        if len(day) < 2:
            day = '0%s' % day
        for hour_mnt in hour_minute:
            day_hm.append('%s%s' % (day, hour_mnt))
    #���� �� ����װ
    month_dhm = []
    #ֻ��30����·�
    month_short = ['02', '04', '06', '09', '11']
    for month in cron_time[3]:
        month = str(month)
        if len(month) < 2:
            month = '0%s' % month
        for day_hm_s in day_hm:
            if month == '02':
                if (((not year_num % 4 ) and (year_num % 100)) or (not year_num % 400)):
                    #����2�·���29��
                    if int(day_hm_s[:2]) > 29:
                        continue
                else:
                    #����2�·���28��
                    if int(day_hm_s[:2]) > 28:
                        continue
            if month in month_short:
                if int(day_hm_s[:2]) > 30:
                    continue
            month_dhm.append('%s%s' % (month, day_hm_s))
    #���� �� ����װ
    len_start = len(limit_start)
    len_end = len(limit_end)
    month_dhm_limit = []
    for month_dhm_s in month_dhm:
        time_ymdhm = '%s%s' % (str(year_num), month_dhm_s)
        #��ʼʱ��\����ʱ��������ų�
        if (int(time_ymdhm[:len_start]) < int(limit_start)) or \
         (int(time_ymdhm[:len_end]) > int(limit_end)):
            continue
        month_dhm_limit.append(time_ymdhm)
    if len(cron_time[4]) < 7:
        #������ÿ��ָ��ʱ����ų�
        month_dhm_week = []
        for time_minute in month_dhm_limit:
            str_time = time.strptime(time_minute, '%Y%m%d%H%M%S')
            if str_time.tm_wday in cron_time[4]:
                month_dhm_week.append(time_minute)
        return month_dhm_week
    return month_dhm_limit
  
  
#crontabʱ���������д�� �� ����ƥ��
PATTEN = {
    #������
    'number':'^[0-9]+$',
    #�����б�,�� 1,2,3,6
    'num_list':'^[0-9]+([,][0-9]+)+$',
    #�Ǻ� *
    'star':'^\*$',
    #�Ǻ�/���� ��ϣ��� */3
    'star_num':'^\*\/[0-9]+$',
    #���� �� 8-20
    'range':'^[0-9]+[\-][0-9]+$',
    #����/���� ��� �� 8-20/3
    'range_div':'^[0-9]+[\-][0-9]+[\/][0-9]+$'
    #����/���� �б� ��ϣ��� 8-20/3,21,22,34
    #'range_div_list':'^([0-9]+[\-][0-9]+[\/][0-9]+)([,][0-9]+)+$'
    }
#�������Ӧ�Ĵ�����
PATTEN_HANDLER = {
    'number':handle_num,
    'num_list':handle_nlist,
    'star':handle_star,
    'star_num':handle_starnum,
    'range':handle_range,
    'range_div':handle_rangedv
}
  
  
def isdo(strs,tips=None):
    """
    �ж��Ƿ�ƥ��ɹ���
    """
    try:
        tips = tips==None and "�ļ����Ƹ�ʽ����job_��-��-��-ʱ-��_�ļ���.txt" or tips
        timer = strs.replace('@',"*").replace('%','/').split('_')[1]
        month,week,day,hour,mins = timer.split('-')
        conf_string = mins+" "+hour+" "+day+" "+month+" "+week
        res, desc = parse_crontab_time(conf_string)
        if res == 0:
            cron_time = desc
        else:
            return False
  
        now =FDateTime.now()
        now = FDateTime.datetostring(now, "%Y%m%d%H%M00")
  
        time_stamp = FDateTime.strtotime(now, "%Y%m%d%H%M00")
  
        #time_stamp = int(time.time())
        #���� ʱ�����Ӧ�� �� ʱ �� �� ��
        time_struct = get_struct_time(time_stamp)
        match_res = time_match_crontab(cron_time, time_struct)
        return match_res[1]
    except:
        print tips
        return False
  
def main():
    """������ʵ��"""
    #crontab������һ��ʱ�����
    #conf_string = '*/10 * * * * (cd /opt/pythonpm/devpapps; /usr/local/bin/python2.5 data_test.py>>output_error.txt)'
    conf_string = '*/10 * * * *'
    #ʱ���
    time_stamp = int(time.time())
  
    #����crontabʱ�����ò��� �� ʱ �� �� �� ����ȡֵ��Χ
    res, desc = parse_crontab_time(conf_string)
  
    if res == 0:
        cron_time = desc
    else:
        print desc
        sys, exit(-1)
  
    print "\nconfig:", conf_string
    print "\nparse result(range for crontab):"
  
    print " minute:", cron_time[0]
    print " hour: ", cron_time[1]
    print " day: ", cron_time[2]
    print " month: ", cron_time[3]
    print " week day:", cron_time[4]
  
    #���� ʱ�����Ӧ�� �� ʱ �� �� ��
    time_struct = get_struct_time(time_stamp)
    print "\nstruct time(minute hour day month week) for %d :" % \
         time_stamp, time_struct
  
    #��ʱ�����crontab������һ��ʱ������Աȣ��жϸ�ʱ����Ƿ��������趨��ʱ�䷶Χ��
    match_res = time_match_crontab(cron_time, time_struct)
    print "\nmatching result:", match_res
  
    #crontab�����趨��Χ������ӽ�ʱָ�������һ��ʱ��
    most_close = close_to_cron(cron_time, time_struct)
    print "\nin range of crontab time which is most colse to struct ", most_close
  
    time_list = cron_time_list(cron_time)
    print "\n\n %d times need to tart-up:\n" % len(time_list)
    print time_list[:10], '...'
  
  
if __name__ == '__main__':
    #�뿴 ʹ��ʵ��
    strs = 'job_@-@-@-@-@_test02.txt.sh'
    print isdo(strs)
  
    #main()0")





