# 모듈 import
# 접속 및 API 공통 모듈
from ebestapi import eBESTConnect, ExecuteSQL
from ebestapi import eBESTAPI

# 조회 모듈
from inquiry import *

# schedule
import schedule

# time 모듈
from datetime import datetime
import time

# warning
import warnings
warnings.filterwarnings("ignore")

# 현물주문 Class
class StockOrder(eBESTAPI):
    # 초기화 함수
    def __init__(self, access_token, _order_body_params):
        super().__init__(access_token)
        # URL 재설정
        self._path = "stock/order"

        # 거래코드와 바디 설정
        self.tr_cd = "CSPAT00601"
        self._order_body_params = _order_body_params
        self.body = self.make_body(self._order_body_params)

        # 주문결과 JSON 데이터 확인
        self._json_data = self.make_request(self._path, self.tr_cd, self.body)

    # 바디 생성 함수
    def make_body(self, _order_body_params):
        _body = {
            "CSPAT00601InBlock1": {
                "IsuNo": _order_body_params["ticker"],  # 종목번호(앞에 A 필수)
                "OrdQty": _order_body_params["ord_qty"],  # 주문수량
                "OrdPrc": _order_body_params["ord_price"],  # 주문가
                "BnsTpCode":
                _order_body_params["bnstp_code"],  # 매매구분(1:매도, 2:매수)
                "OrdprcPtnCode": _order_body_params["ord_prc_code"],  # 호가유형코드
                "MgntrnCode": "000",  # 신용거래코드
                "LoanDt": "",  # 대출일 (없으면 빈칸)
                "OrdCndiTpCode": "0",  # 주문조건(0:없음, 1:IOC, 2:FOK)
            }
        }

        return _body


# 현물정정주문 Class
class CorrectionOrder(eBESTAPI):

    def __init__(self, access_token, _order_body_params):
        super().__init__(access_token)
        # URL 재설정
        self._path = "stock/order"

        # 거래코드와 바디 설정
        self.tr_cd = "CSPAT00701"
        self._order_body_params = _order_body_params
        self.body = self.make_body(self._order_body_params)

        # 주문결과 JSON 데이터 확인
        self._json_data = self.make_request(self._path, self.tr_cd, self.body)

        # 데이터프레임으로 변환
        # self.outblock_list = ["OutBlock1", "OutBlock2"]
        # self._data_frame = self.make_df(self._json_data, self.tr_cd, self.outblock_list)

    # 바디 생성 함수
    def make_body(self, _order_body_params):
        _body = {
            "CSPAT00701InBlock1": {
                "OrgOrdNo": _order_body_params["org_ord_no"],
                "IsuNo": _order_body_params["ticker"],
                "OrdQty": _order_body_params["ord_qty"],
                "OrdprcPtnCode": _order_body_params["ord_prc_code"],
                "OrdCndiTpCode": _order_body_params["ord_cnd_tp_code"],
                "OrdPrc": _order_body_params["ord_price"],
            }
        }

        return _body


# 현물취소주문 Class
class CancelOrder(eBESTAPI):

    def __init__(self, access_token, _order_body_params):
        super().__init__(access_token)
        # URL 재설정
        self._path = "stock/order"

        # 거래코드와 바디 설정
        self.tr_cd = "CSPAT00801"
        self._order_body_params = _order_body_params
        self.body = self.make_body(self._order_body_params)

        # 주문결과 JSON 데이터 확인
        self._json_data = self.make_request(self._path, self.tr_cd, self.body)

    # 바디 생성 함수
    def make_body(self, _order_body_params):
        _body = {
            "CSPAT00801InBlock1": {
                "OrgOrdNo": _order_body_params["org_ord_no"],
                "IsuNo": _order_body_params["ticker"],
                "OrdQty": _order_body_params["ord_qty"],
            }
        }

        return _body


# 데이 트레이드 class
class AutoTrade(eBESTAPI):
    # 초기화 함수
    def __init__(self, access_token):
        super().__init__(access_token)
        # 오늘의 날짜
        self.today = self.time_now.date().strftime("%Y%m%d")
        # 모든 매매종목 리스트 받기
        self.all_ticker_list = self.get_all_ticker_list()
        # 주문 바디 파라미터
        self._body_params = None
        # 트레이드 함수 실행
        self.auto_trade = self.run_trade_schedule()

    # 매매종목 리스트 받는 함수
    def get_all_ticker_list(self):
        sql = "select ticker from trading_list"
        exec_sql = ExecuteSQL(sql)
        _result = exec_sql._result
        all_ticker_list = _result["ticker"].tolist()
        return all_ticker_list

    def make_order_params(self, ticker, ord_qty, ord_price, bnstp_code):
        """
        # 바디에 넣어줄 파라미터 설정
        # 테스트에서는 편의상 전부 시장가로 주문하겠습니다.
        # 추후 모델이 산출한 변수들로 대입
        """
        _order_body_params = {
            "ticker": ticker,  # 종목번호(앞에 A 필수)
            "ord_qty": ord_qty,  # 주문수량
            "ord_price": ord_price,  # 주문가
            "bnstp_code": bnstp_code,  # 매매구분(1:매도, 2:매수)
            "ord_prc_code": "03",  # 호가유형코드, 테스트에서는 시장가 대입
        }
        return _order_body_params

    def select_buy_list(self, all_ticker_list):
        # 매수할 종목 리스트
        _buy_list = []
        """
        [모델이 선정한 타겟을 _buy_list에 추가하는 코드]
        """

        return _buy_list

    def select_sell_list(self, ACCESS_TOKEN):
        """매도할 종목 선정 함수
        Args:
            access_token : 접근 토큰

        Returns:
            _sell_list : 매도할 종목 리스트
        """

        # 잔고조회 함수 실행
        t0424 = GetT0424(ACCESS_TOKEN)
        t0424_df = t0424._data_frame

        # 수익률이 문자로 들어옴 -> 실수로 변환
        t0424_df["sunikrt"] = t0424_df["sunikrt"].astype(float)
        """
        ['잔고가 남아있는 종목 중' 모델이 선정한 타겟을 _sell_list에 추가하는 코드]
        """
        # 종목명과 매도가능수량을 리턴
        _sell_list = t0424_df[["expcode", "mdposqt"]]

        return _sell_list

    # 매수 실행 함수
    def auto_buy_order(self, all_ticker_list):
        """매수 종목과 수량 정해서 주문하는 함수

        Returns:
            _buy_order: 매수 주문 object
        """
        _buy_list = self.select_buy_list(all_ticker_list)
        ord_qty = 100
        for ticker in _buy_list:
            if ord_qty > 0:
                _body_params = self.make_order_params(ticker, ord_qty, 0, "2")
                _buy_order = StockOrder(ACCESS_TOKEN, _body_params)

        return _buy_order

    # 매도 실행 함수
    def auto_sell_order(self):
        """매도 종목과 수량 정해서 주문하는 함수

        Returns:
            _sell_order : 매도 주문 object
        """
        _sell_list = self.select_sell_list(ACCESS_TOKEN)
        for row in _sell_list.iterrows():
            # 매도는 무조건 전량 매도
            ticker = row[1]["expcode"]
            ord_qty = row[1]["mdposqt"]
            # 모의투자는 앞에 'A' 붙여줘야 함
            if ord_qty > 0:
                _ticker = "A" + ticker
                _body_params = self.make_order_params(_ticker, ord_qty, 0, "1")
                _sell_order = StockOrder(ACCESS_TOKEN, _body_params)

        return _sell_order

    # 메시지 출력함수 모음
    def print_open_message(self):
        print("시장이 개장했습니다. 자동 매매를 개시합니다.")

    def print_order_message(self):
        print("자동주문 스케줄 실행중...")

    # 스케줄 실행 함수
    def run_trade_schedule(self):
        """1분 단위로 자동 주문 실행하는 함수"""
        # 자동주문 실행주기 설정 : 1분
        job_buy_order = schedule.every(1).minutes.do(self.auto_buy_order,
                                                     self.all_ticker_list)
        job_sell_order = schedule.every(1).minutes.do(self.auto_sell_order)
        job_message = schedule.every(1).minutes.do(self.print_order_message)

        job_list = [job_buy_order, job_sell_order, job_message]

        # 스케쥴 시작
        while True:
            # 모든 스케쥴 실행
            schedule.run_pending()
            time.sleep(5)

            # 15:20이 되면 자동주문 종료
            now_hour_minute = datetime.now().strftime("%H:%M")
            if now_hour_minute == "15:20":
                print("자동 주문을 종료합니다.")
                for job in job_list:
                    schedule.cancel_job(job)
                break

        return


# 일일 결산 Class
class DayClosing:
    # 초기화 함수
    def __init__(self, access_token):
        # 일일 매매일지
        self.t0150_df = self.get_t0150_df(access_token)
        # 일일 최종 잔고
        self.t0424_df = self.get_t0424_df(access_token)
        # 결산 함수 실행
        self.run_closing_schedule()

    def get_t0150_df(self, ACCESS_TOKEN):
        """일일 매매일지 받아오는 함수
        Args:
            ACCESS_TOKEN: 접속 토큰
        Returns:
            t0150_df : 일일 매매일지
        """
        t0150 = GetT0150(ACCESS_TOKEN)
        t0150_df = t0150._data_frame
        return t0150_df

    def get_t0424_df(self, ACCESS_TOKEN):
        """일일 최종 잔고 받아오는 함수
        Args:
            ACCESS_TOKEN: 접속 토큰
        Returns:
            t0424_df : 일일 최종 잔고
        """
        t0424 = GetT0424(ACCESS_TOKEN)
        t0424_df = t0424._data_frame
        return t0424_df

    def run_closing_schedule(self, ACCESS_TOKEN):
        """결산 함수"""
        # 결산 스케쥴 설정
        job_t0150 = (schedule.every().days.at("15:30").do(
            self.get_t0150_df, ACCESS_TOKEN))
        job_t0424 = (schedule.every().days.at("15:30").do(
            self.get_t0424_df, ACCESS_TOKEN))

        job_list = [job_t0150, job_t0424]

        count = 0

        # 스케쥴 시작
        while True:
            # 모든 스케쥴 실행
            schedule.run_pending()
            time.sleep(5)

            count += 1

            if count > 0:
                print("자동 주문을 종료합니다.")
                for job in job_list:
                    schedule.cancel_job(job)
                break

        return


# OPEN API 키 설정
APP_KEY = ''
APP_SECRET = ''

# 토큰 생성함수 실행
conn = eBESTConnect(APP_KEY, APP_SECRET)
ACCESS_TOKEN = conn.access_token
