import requests
class NSEFETCHER:

    def __init__(self,stock_codes):
        if isinstance(stock_codes, str):
            stock_codes = [stock_codes]
        self.stock_codes = stock_codes
        self.base_url = "https://www.nseindia.com/"
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
            "like Gecko) "
            "Chrome/80.0.3987.149 Safari/537.36",
            "accept-language": "en,gu;q=0.9,hi;q=0.8",
            "accept-encoding": "gzip, deflate, br",
        }
        self.counter = 0

    def create_session_for_nse(self,params={},request_url="",payload={}):
        session = requests.Session()
        request = session.get(self.base_url, headers=self.headers, timeout=5)
        cookies = dict(request.cookies)
        response = None
        if not payload:
            response = session.get(
                request_url, headers=self.headers,params=params, timeout=5, cookies=cookies
            )
        else:
            response  = session.post(request_url, headers=self.headers,params=params, timeout=5, cookies=cookies,json=payload)       
        return response  
    
    def process_request(self,url,params={},payload={}):
        try:
            response = self.create_session_for_nse(request_url=url,params=params,payload=payload)
            if response.status_code == 200:
                return response.json()
            else:
                return {}
        except requests.exceptions.ConnectionError as e:
            if self.counter < 5:
                self.process_request(url)
                self.counter += 1
            else:
                self.counter = 0
                return {}
                        
    def fetch_option_chain_for_indices(self):
        '''
        Work Pending for dynamic Option Chain
        '''
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY"        
        return self.process_request(url)

    def fetch_option_chain_for_equity(self,stock_code):
        url = f'https://www.nseindia.com/api/option-chain-equities?symbol={stock_code}'
        return self.process_request(url)

    def fetch_quote_data_for_equity(self,stock_code):
        url_1 = 'https://www.nseindia.com/api/quote-equity?symbol='+stock_code
        data_1 = self.process_request(url_1)
        url_2= 'https://www.nseindia.com/api/quote-equity?symbol='+stock_code+'&section=trade_info'
        data_2 = self.process_request(url_2)
        if data_1 and data_2:
            data_1.update(data_2)
        return data_1
          
    def get_corporate_actions(self,stock_code):
        url = f'https://www.nseindia.com/api/corp-info?symbol={stock_code}&corpType=corpactions&market=equities'
        return self.process_request(url)  
    
    def get_announcement(self,stock_code):
        url = f'https://www.nseindia.com/api/corp-info?symbol={stock_code}&corpType=announcement&market=equities'
        return self.process_request(url)
 
    def get_company_annual_reports(self,stock_code):
        url = f'https://www.nseindia.com/api/corp-info?symbol={stock_code}&corpType=annualreport&market=cm'
        return self.process_request(url)
    
    def get_company_board_meeting_details(self,stock_code):
        url = f'https://www.nseindia.com/api/corp-info?symbol={stock_code}&corpType=boardmeeting&market=equities'
        return self.process_request(url)

    def get_financial_results_details(self,stock_code):
        url = f'https://www.nseindia.com/api/corp-info?symbol={stock_code}&corpType=financialResult&market=equities'
        return self.process_request(url)

    def get_insider_trading_details(self,stock_code):
        url = f'https://www.nseindia.com/api/corp-info?symbol={stock_code}&corpType=insidertrading&market=equities'
        return self.process_request(url)
    
    def get_shareholding_pattern(self,stock_code):
        url = f'https://www.nseindia.com/api/corp-info?symbol={stock_code}&corpType=shp&market=equities'
        return self.process_request(url)

    def get_quote_for_stock_derivative(self,stock_code):
        url = f'https://www.nseindia.com/api/quote-derivative?symbol={stock_code}'
        data = self.process_request(url)
        return self.process_quote_derivative(data)
    
    def process_quote_derivative(self,data):
        final_data = {}
        futures = []
        options = []
        for key,val in data.items():
            if key == 'stocks':
                for meta in data[key]:
                    if meta['metadata']['instrumentType'] == "Stock Futures":
                        futures.append(meta)
                    else:
                        options.append(meta)
            else:
                final_data[key] = val
        final_data['futures'] = futures
        final_data['options'] = options
        return final_data
    
    def getChartDataOfIndex(self,index):
        '''
            Work in Progress
        '''
        ''' OPTSTKASTRAL30-11-2023CE1940.00 Index value like'''
        url = f'https://www.nseindia.com/api/chart-databyindex?index={index}'
        return self.process_request(url)

    def getHistoricalOHLCDataDailyTimeFrame(self,stock_code):
        '''only Last 1 year data i can fetch'''
        from datetime import datetime,timedelta
        from_date = datetime.strftime(datetime.now(),'%d-%m-%Y')
        to_date =  datetime.strftime(datetime.now() - timedelta(days=365),'%d-%m-%Y') 
        url = f'https://www.nseindia.com/api/historical/cm/equity?symbol={stock_code}&series=["EQ"]&from={to_date}&to={from_date}'
        return self.process_request(url=url)
    
    def getQuoteEquityOrderBookTradeInfo(self,stock_code):
        url = f'https://www.nseindia.com/api/quote-equity?symbol={stock_code}&section=trade_info'
        return self.process_request(url)
  
    def gather_all_data_for_stock(self, stock_code):
        data = {
            "stock_code": stock_code,
            "quote_data": self.fetch_quote_data_for_equity(stock_code),
            "share_holding_pattern": self.get_shareholding_pattern(stock_code),
            "insider_trading_details": self.get_insider_trading_details(stock_code),
            "financial_results_details": self.get_financial_results_details(stock_code),
            "company_board_meeting_details": self.get_company_board_meeting_details(stock_code),
            "company_annual_reports": self.get_company_annual_reports(stock_code),
            "announcements": self.get_announcement(stock_code),
            "corporate_actions": self.get_corporate_actions(stock_code),
            "quote_derivative_data": self.get_quote_for_stock_derivative(stock_code),
        }
        return data
    
    def gather_all_data(self):
        all_data = {}
        for stock_code in self.stock_codes:
            stock_data = self.gather_all_data_for_stock(stock_code)
            if stock_data:
                all_data[stock_code] = stock_data
        return all_data