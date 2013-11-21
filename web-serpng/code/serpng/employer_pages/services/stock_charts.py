"""
Code for accessing job search results.

Copyright (c) 2013 Simply Hired, Inc. All rights reserved.
"""
from collections import namedtuple

from common_models_employers.models.employers import Employer

StockChartResults = namedtuple('StockChartResults',
                               ['src_name', 'src_symbol', 'src_url'])
url_yh = 'http://chart.finance.yahoo.com/t?' + \
         's=%s&t=1y&lang=en-US&region=US&width=290&height=180'
url_bb = 'http://www.bloomberg.com/apps/chart?' + \
         'ticks=%s&timeout=10&type=gp_line2&range=1y&cfg=ChartBuilderVol_bw.xml&img=png&w=290&h=225'
def get_stock_charts(emp):
    results = []
    traded_as = emp.get_traded_as()
    bw = emp.get_bw()
    
    if traded_as != '':
        if traded_as.startswith(('NYSE:', 'NASDAQ:')):
            symbol = traded_as.rsplit(':', 1)[1].strip()
            
            src_name = 'Yahoo'
            src_symbol = ''.join([symbol, ''])
            src_url = url_yh % (src_symbol)
            results.append(StockChartResults(src_name, src_symbol, src_url))
            
            src_name = 'Bloomberg'
            src_symbol = ''.join([symbol, ':US'])
            src_url = url_bb % (src_symbol)
            results.append(StockChartResults(src_name, src_symbol, src_url))
        
        if traded_as.startswith(('XETRA:')):
            symbol = traded_as.rsplit(':', 1)[1].strip()
            
            src_name = 'Yahoo'
            src_symbol = ''.join([symbol, '.DE'])
            src_url = url_yh % (src_symbol)
            results.append(StockChartResults(src_name, src_symbol, src_url))
            
            src_name = 'Bloomberg'
            src_symbol = ''.join([symbol, ':GR'])
            src_url = url_bb % (src_symbol)
            results.append(StockChartResults(src_name, src_symbol, src_url))
        
        if traded_as.startswith(('EN PARIS:')):
            symbol = traded_as.rsplit(':', 1)[1].strip()
            
            src_name = 'Yahoo'
            src_symbol = ''.join([symbol, '.PA'])
            src_url = url_yh % (src_symbol)
            results.append(StockChartResults(src_name, src_symbol, src_url))
            
            src_name = 'Bloomberg'
            src_symbol = ''.join([symbol, ':FP'])
            src_url = url_bb % (src_symbol)
            results.append(StockChartResults(src_name, src_symbol, src_url))
        
        if traded_as.startswith(('SIX SWISS:')):
            symbol = traded_as.rsplit(':', 1)[1].strip()
            
            src_name = 'Yahoo'
            src_symbol = ''.join([symbol, '.VX'])
            src_url = url_yh % (src_symbol)
            results.append(StockChartResults(src_name, src_symbol, src_url))
            
            src_name = 'Bloomberg'
            src_symbol = ''.join([symbol, ':VX'])
            src_url = url_bb % (src_symbol)
            results.append(StockChartResults(src_name, src_symbol, src_url))
        
        if traded_as.startswith(('TOKYO:')):
            symbol = traded_as.rsplit(':', 1)[1].strip()
            
            src_name = 'Bloomberg'
            src_symbol = ''.join([symbol, ':JP'])
            src_url = url_bb % (src_symbol)
            results.append(StockChartResults(src_name, src_symbol, src_url))
    elif bw is not None and bw.is_public:
        src_name = 'Bloomberg'
        src_symbol = bw.ticker
        src_url = url_bb % (src_symbol)
        results.append(StockChartResults(src_name, src_symbol, src_url))
        
    return results