# 모듈 import

# 연결 및 공통 모듈
from ebestapi import eBESTAPI

# warning
import warnings

warnings.filterwarnings("ignore")


# 주식잔고2(t0424) Class
class GetT0424(eBESTAPI):

    def __init__(self, access_token):
        super().__init__(access_token)

        # URL 주소 재설정
        self._path = "stock/accno"

        # 거래코드와 바디 설정
        self.tr_cd = "t0424"
        self.body = self.make_body()

        # 데이터프레임으로 저장할 블록 설정
        self.outblock_list = ["OutBlock1"]
        # Select할 컬럼, 새로 명명할 컬럼 설정
        self._sel_col = {}
        self._new_col_name = {}

        self._json_data = self.make_request(self._path, self.tr_cd, self.body)
        self._data_frame = self.make_df(
            self._json_data,
            self.tr_cd,
            self.outblock_list,
            self._sel_col,
            self._new_col_name,
        )

        # DF를 저장하는 CSV
        # self.output_csv = self.save_csv(self._data_frame, self.tr_cd)

    def make_body(self):
        """바디 생성 함수
        Returns:
            _body (dict) : Request body
        """
        _body = {
            "t0424InBlock": {
                "prcgb": "",  # 단가구분
                "chegb": "",  # 체결구분
                "dangb": "",  # 단일가구분
                "charge": "",  # 제비용포함여부
                "cts_expcode": "",  # CTS_종목번호
            }
        }
        return _body


# 종목별 주식체결/미체결(t0425) Class
class GetT0425(eBESTAPI):

    def __init__(self, access_token):
        super().__init__(access_token)

        # URL 주소 재설정
        self._path = "stock/accno"

        # 거래코드와 바디 설정
        self.tr_cd = "t0425"
        # self.ticker = ticker
        self.body = self.make_body()

        # 데이터프레임으로 저장할 블록 설정
        self.outblock_list = ["OutBlock"]
        # Select할 컬럼, 새로 명명할 컬럼 설정
        self._sel_col = {}
        self._new_col_name = {}

        # JSON, 데이터프레임 설정
        self._json_data = self.make_request(self._path, self.tr_cd, self.body)
        self._data_frame = self.make_df(
            self._json_data,
            self.tr_cd,
            self.outblock_list,
            self._sel_col,
            self._new_col_name,
        )

    def make_body(self, ticker=""):
        """바디 생성 함수
        Args:
            ticker : 종목코드()

        Returns:
            _body : Request 바디
        """
        _body = {
            "t0425InBlock": {
                "expcode": ticker,  # 종목번호 (비워둘 시 전종목 체결상황의 총합 조회)
                "chegb": "0",  # 체결구분 (0:전체, 1:체결, 2:미체결)
                "medosu": "0",  # 매매구분 (0:전체, 1:매도, 2:매수)
                "sortgb": "1",  # 정렬순서 (1:주문번호 역순, 2:주문번호 순)
                "cts_ordno": "",  # 연속조회시 OutBlock의 동일필드 입력
            }
        }

        return _body


# 주식현재가(시세)조회(t1102) Class
class GetT1102(eBESTAPI):

    def __init__(self, access_token, _ticker):
        super().__init__(access_token)

        # URL 주소 재설정
        self._path = "stock/market-data"

        # 거래코드와 종목코드, 바디 설정
        self.tr_cd = "t1102"
        self._ticker = _ticker
        self.body = self.make_body(self._ticker)

        # 데이터프레임으로 저장할 블록 설정
        self.outblock_list = ["OutBlock"]
        # Select할 컬럼, 새로 명명할 컬럼 설정
        self._sel_col = {}
        self._new_col_name = {}

        # JSON, 데이터프레임 설정
        self._json_data = self.make_request(self._path, self.tr_cd, self.body)
        self._data_frame = self.make_df(self._json_data, self.tr_cd, self.outblock_list, self._sel_col, self._new_col_name)

    def make_body(self, _ticker):
        """바디 생성 함수
        Returns:
            _body (dict) : Request body
        """
        _body = {"t1102InBlock": {"shcode": _ticker}}
        return _body


# 주식당일매매일지/수수료(t0150) Class
class GetT0150(eBESTAPI):

    def __init__(self, access_token):
        super().__init__(access_token)

        # URL 주소 재설정
        self._path = "stock/accno"

        # 거래코드와 바디 설정
        self.tr_cd = "t0150"
        self.body = self.make_body()

        # 데이터프레임으로 저장할 블록 설정
        self.outblock_list = ["OutBlock1"]
        # Select할 컬럼, 새로 명명할 컬럼 설정
        self._sel_col = {}
        self._new_col_name = {}

        # JSON, 데이터프레임 설정
        self._json_data = self.make_request(self._path, self.tr_cd, self.body)
        self._data_frame = self.make_df(
            self._json_data,
            self.tr_cd,
            self.outblock_list,
            self._sel_col,
            self._new_col_name,
        )

    def make_body(self):
        """
        바디 딕셔너리 생성
  
        Returns:
            _body : Request body
        """
        _body = {
            "t0150InBlock": {
                "cts_medosu": "1",  # CTS_매매구분
                "cts_expcode": "1",  # CTS_종목번호
                "cts_price": "1",  # CTS_단가
                "cts_middiv": "1",  # CTS_매체
            }
        }
        return _body


# 주식당일매매일지/수수료(전일) (t0151) Class
class GetT0151(eBESTAPI):

    def __init__(self, access_token, date):
        super().__init__(access_token)

        # URL 주소 재설정
        self._path = "stock/accno"

        # 거래코드와 바디 설정
        self.tr_cd = "t0151"
        self.body = self.make_body(date)

        # 날짜 설정
        self.date = date

        # 데이터프레임으로 저장할 블록 설정
        self.outblock_list = ["OutBlock1"]
        # Select할 컬럼, 새로 명명할 컬럼 설정
        self._sel_col = {}
        self._new_col_name = {}

        # JSON, 데이터프레임 설정
        self._json_data = self.make_request(self._path, self.tr_cd, self.body)
        self._data_frame = self.make_df(
            self._json_data,
            self.tr_cd,
            self.outblock_list,
            self._sel_col,
            self._new_col_name,
        )

    def make_body(self, date):
        """
        바디 딕셔너리 생성
        Args:
            date : 조회할 일자

        Returns:
            _body : Request body
        """
        _body = {
            "t0151InBlock": {
                "date": date,  # 일자
                "cts_medosu": "1",  # CTS_매매구분
                "cts_expcode": "1",  # CTS_종목번호
                "cts_price": "1",  # CTS_단가
                "cts_middiv": "1",  # CTS_매체
            }
        }
        return _body
