import streamlit as st
import pandas as pd 
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from ebestapi import *
import inquiry
import pymysql
import numpy as np
import folium
from datetime import datetime
from pykrx import stock

# 현재 날짜 가져오기
now = datetime.now()
current_date = now.strftime("%Y%m%d")
current_date = '20240304'

# 데이터베이스 연결 (전역 변수로 선언)
db_id = ''
db_pw = ''
db_host = ''
db_port = 0
db_name = ''

connection = pymysql.connect(
    host=db_host,
    user=db_id,
    password=db_pw,
    db=db_name,
    port=db_port,
    charset='utf8'
)

def round_to_hundred_million(df):
    for column in df.columns:
        df[column] = round(df[column] / 100000000, 0)
def format_number(x):
    return '{:,}'.format(int(x))
# 조건에 따라 색상 변경
def color_change(value):
    if value < 0:
        return 'color: blue'
    elif value > 0:
        return 'color: red'
    else:
        return ''

# 커서 객체 생성 (전역 변수로 선언)
cursor = connection.cursor()

# get_session_state() 함수는 세션 상태를 초기화하는 함수입니다.
def get_session_state(**kwargs):
    session_state = {}
    for key, value in kwargs.items():
        session_state[key] = value
    return session_state

# session_state 변수를 생성하고, logged_in과 username 값을 False와 None으로 초기화합니다.
session_state = get_session_state(logged_in=False, username=None)

# if not session_state["logged_in"] 조건을 사용하여 로그인 페이지를 표시합니다.
if not session_state["logged_in"]:
# 사용자 이름과 비밀번호 입력 필드를 생성합니다.
    username = st.text_input("사용자 이름을 입력하세요")
    password = st.text_input("비밀번호를 입력하세요", type="password")
# login() 함수를 정의하고, 사용자 이름과 비밀번호를 인자로 받아 인증을 수행합니다. 인증에 성공하면 세션 상태를 업데이트하고 True를 반환합니다. 인증에 실패하면 오류 메시지를 출력하고 False를 반환합니다.
    def login(username, password):
        try:
            cursor.execute(
                f"SELECT * FROM users WHERE username = '{username}'"
            )
            result = cursor.fetchone()
            re = pd.DataFrame(result)
            if result is None:
                st.error("없는 사용자입니다.")
            elif password != result[1]:
                st.error("비밀번호가 틀렸습니다.")
            else:
                st.error("로그인이 성공했습니다.")
                session_state["logged_in"] = True
                session_state["username"] = username
                session_state['APP_KEY'] = re.iloc[2]
                session_state['APP_SECRET'] = re.iloc[3]
                return True
        except pymysql.Error as e:
            st.error(f"쿼리 실행 오류: {e}")
            return False

# logged_in 변수에 login() 함수의 반환 값을 저장합니다.
    logged_in = login(username, password)
# 로그인 후에는 인증된 사용자를 위한 페이지를 구현할 수 있습니다.
# 해당 코드를 실행하면, 사용자 인증을 위한 로그인 페이지가 표시됩니다. 사용자가 인증에 성공하면, 인증된 사용자를 위한 페이지가 표시됩니다.
# 로그인 후 실행할 코드
if session_state["logged_in"]:
    # 여기에 원하는 기능 코드를 작성합니다.
    # 필요하면 `connection` and `cursor` 객체를 사용하여 데이터베이스에 접근합니다.
    # 라디오 버튼 생성
    st.sidebar.title('주식정보🌸')
    options = ['과거지표', '통장잔고', '일일거래량', '종목정보', '지도']
    selected_option = st.sidebar.radio('원하는 기능을 눌러주세요', options)
    APP_KEY = session_state['APP_KEY']
    APP_SECRET = session_state['APP_SECRET']
    # 토큰구하는것
    token = eBESTAPI.eBESTConnect(APP_KEY,APP_SECRET) 
    token = token.access_token
    # 선택한 항목에 따라 다른 내용 보여주기
#사용자가 '과거지표'를 선택하면, 다음 작업을 수행합니다.
    if selected_option == '과거지표':
# '코스피 및 코스닥 데이터'라는 제목을 표시합니다.
        st.title('코스피 및 코스닥 데이터')
# '2017_02_24-2024_02_24.csv' 파일과 'kosdaq.csv' 파일을 읽어와 DataFrame으로 변환합니다.
        df = pd.read_csv('./2017_02_24-2024_02_24.csv')
        df1 = pd.read_csv('./kosdaq.csv')
# 'get_market_trading_value_by_date()' 함수를 사용하여 현재 날짜를 기준으로 한 코스피와 코스닥의 시장 거래대금을 가져옵니다.
        stockskospi = stock.get_market_trading_value_by_date(current_date,current_date, "KOSPI").iloc[:,:4]
        stockskosdaq = stock.get_market_trading_value_by_date(current_date,current_date, "KOSDAQ").iloc[:,:4]
# 'round_to_hundred_million()' 함수를 사용하여 시장 거래대금을 100억 단위로 반올림합니다.
        round_to_hundred_million(stockskospi)
        round_to_hundred_million(stockskosdaq)
# 'format_number()' 함수와 'color_change()' 함수를 사용하여 DataFrame의 값을 포맷하고 색상을 변경합니다.
        styled_kospi = stockskospi.style.format(format_number, subset=['기관합계','기타법인','개인','외국인합계'])
        styled_kospi = styled_kospi.applymap(color_change, subset=['기관합계','기타법인','개인','외국인합계'])
        styled_kosdaq = stockskosdaq.style.format(format_number, subset=['기관합계','기타법인','개인','외국인합계'])
        styled_kosdaq = styled_kosdaq.applymap(color_change, subset=['기관합계','기타법인','개인','외국인합계'])
        df['날짜'] = pd.to_datetime(df['날짜'])
        df['종가'] = df['종가'].str.replace(',','').astype(float)
# 종가 데이터를 기반으로한 캔들스틱 차트를 생성하고, 'st.plotly_chart()'를 사용하여 차트를 표시합니다.
        fig = go.Figure(data=[go.Candlestick(x=df['날짜'], open=df['시가'], high=df['고가'], low=df['저가'], close=df['종가'])])
        fig.update_layout(xaxis=dict(rangeslider=dict(visible=False)))
        fig.update_traces(increasing_line_color='red', decreasing_line_color='blue')
        st.plotly_chart(fig)
# 스타일이 적용된 코스피와 코스닥 DataFrame을 'st.dataframe()'을 사용하여 표시합니다
        st.dataframe(styled_kospi)
        df1['날짜'] = pd.to_datetime(df1['날짜'])
        df1['종가'] = df1['종가'].str.replace(',','').astype(float)
        fig1 = go.Figure(data=[go.Candlestick(x=df['날짜'], open=df['시가'], high=df['고가'], low=df['저가'], close=df['종가'])])
        fig1.update_layout(xaxis=dict(rangeslider=dict(visible=False)))
        fig1.update_traces(increasing_line_color='red', decreasing_line_color='blue')
        st.plotly_chart(fig1)
        # 결과 출력
        st.dataframe(styled_kosdaq)

# 사용자가 '일일거래량'을 선택하면, 다음 작업을 수행합니다.
    elif selected_option == '일일거래량':
# '일일거래량'이라는 제목을 표시합니다.
        st.title('일일거래량')
# 'GetT0150()' 함수를 사용하여 계좌의 일일거래량 정보를 가져옵니다.
        aa = inquiry.GetT0150(access_token=token)
        t0150_df = aa._data_frame
        if t0150_df.empty:
            st.warning("통장에 보유한 종목이 없습니다.")
        else:
            cursor = connection.cursor()
            t0150_df.columns = ['매매구분','종목코드','수량','가격','정산금액','수수료','세금','농특세','현재가','거래여부']
# 데이터베이스에서 모든 종목 정보를 가져옵니다.
            query1 = f"SELECT * FROM allstockINFO"
            cursor.execute(query1)
            result = cursor.fetchall()
# 가져온 정보를 DataFrame으로 변환하고, 필요한 컬럼명으로 변경합니다.
            ress = pd.DataFrame(result, columns = ['종목코드','종목이름'])
            cursor.close()
            # 이베스트에서 온데이터중 빈칸을 0으로 만들기
            t0150_df.replace('', '0', inplace=True)
# 0으로 만든 컬럼들 이전값을 채우기
            for i in range(len(t0150_df)):
                if t0150_df['종목코드'].iloc[i] == '0':
                    t0150_df['종목코드'].iloc[i] = t0150_df['종목코드'].iloc[i-1]
# 일일거래량 DataFrame과 종목 정보 DataFrame을 종목코드를 기준으로 병합합니다.
            dds = t0150_df.merge(ress, how='left', on='종목코드')
            dds.set_index(['종목이름'], inplace=True)
            #매매구분별데이터
            data = dds.loc[dds['매매구분'] == '매수'].iloc[:,2:5]
            data1 = dds.loc[dds['매매구분'] == '매도'].iloc[:,2:5]
            data2 = dds.loc[dds['매매구분'] == '종목소계'].iloc[:,2:10]

# 추출한 데이터를 페이지네이션하여 표시합니다.
            page_size = 10
            current_page = 1
            # 페이지네이션을 위한 데이터 slicing
            start_index = (current_page - 1) * page_size
            end_index = start_index + page_size
# 병합된 DataFrame에서 매매구분별로 데이터를 추출합니다.
            sliced_data = data[start_index:end_index]
            sliced_data1 = data1[start_index:end_index]
            sliced_data2 = data2[start_index:end_index]
# 각 페이지에서 사용자가 원하는 항목을 선택할 수 있도록 라디오 버튼을 제공합니다.
            options = ['매수', '매도', '종목소계']
            selected_option = st.radio('원하는 항목을 선택하세요', options, key='option')
# 선택한 항목에 따라 해당 데이터를 표시합니다.

            if selected_option == '매수':
                    if data.empty:
                        st.warning("오늘은 매수한 종목이 없습니다.")
                    else:
                        # 인덱스 제거
                        st.dataframe(sliced_data)
# 이전 페이지와 다음 페이지로 이동할 수 있는 버튼을 제공합니다.
                        if st.button("이전 페이지"):
                            if current_page > 1:
                                current_page -= 1
                        if st.button("다음 페이지"):
                            if current_page * page_size < len(data):
                                current_page += 1
            elif selected_option == '매도':
                if data.empty:
                        st.warning("오늘은 매수한 종목이 없습니다.")
                else:
                    st.dataframe(sliced_data1)
                    # 여기에 매수에 대한 로직 작성
                    if st.button("이전 페이지"):
                        if current_page > 1:
                            current_page -= 1
                    if st.button("다음 페이지"):
                        if current_page * page_size < len(data1):
                            current_page += 1
            elif selected_option == '종목소계':
                if data.empty:
                        st.warning("오늘은 매수한 종목이 없습니다.")
                else:
                    st.dataframe(sliced_data2)
                    # 여기에 매수에 대한 로직 작성
                    if st.button("이전 페이지"):
                        if current_page > 1:
                            current_page -= 1
                    if st.button("다음 페이지"):
                        if current_page * page_size < len(data2):
                            current_page += 1
    elif selected_option == '통장잔고':
            st.title('통장잔고')
            # OPEN API 키 설정

            # 여기에 통장잔고에 대한 로직 작성
            aa = inquiry.GetT0424(token)
            t0424_df = aa._data_frame
            if t0424_df.empty:
                st.warning("통장에 보유한 종목이 없습니다.")
            else:
                cols = ['hname', 'sunikrt', 'pamt', 'mamt','janqty','janrt','price', 'appamt', 'dtsunik']
                # 'hname' : 종목이름,  'sunikrt': 추정순자산, 'pamt': 평균단가, 'mamt': 매입금액,'janqty': 잔고수량,'janrt': 보유비중,
                # 'price':현재가, 'appamt': 평가금액, 'dtsunik': 실현손익
                new_df = t0424_df.loc[:, cols]
                df = new_df.reindex(columns=cols)
                cols = ['종목이름', '손익률', '평균단가', '매입금액','잔고수량','보유비중','현재가', '평가금액', '실현손익']
                df.columns = cols
                df.set_index(['종목이름'], inplace=True)
                fig1 = px.pie(new_df, values='janrt', names='hname', title='주식보유비중')      #plotly pie차트
                st.plotly_chart(fig1)
                st.dataframe(df)
    elif selected_option == '종목정보':
            st.title('종목별 정보')
            ticker_dict = {
            # 추가 옵션 및 티커값 추가
            "알체라":"A347860",
            "가온그룹":"A078890" ,
            "셀바스AI":"A108860" ,
            "라온피플":"A300120" ,
            "오픈베이스":"A049480" ,
            "데이타솔루션":"A263800" ,
            "브레인즈컴퍼니":"A099390" ,
            "솔트룩스":"A099390", # 중복된 코드는 제거
            "엑셈":"A205100" ,
            "마음AI":"A377480" ,
            "엠로":"A058970",
            "링크제니시스":"A219420" ,
        } 
            ticker_dicts = {
            # 추가 옵션 및 티커값 추가
            "포스코홀딩스":"005490",
            "에코프로비엠":"247540" 
        }       
            option1 = st.selectbox('원하는 테마를 골라주세요', ['AI','전기차','2차전지',  '정치테마주'])
            if option1 == 'AI':
                option2 = st.selectbox("원하는 종목을 골라주세요", list(ticker_dict.keys()))
                ticker = ticker_dict.get(option2)
                if option2: # option2가 선택된 경우에만 데이터베이스에서 데이터를 가져옵니다.
                    query1 = f"SELECT * FROM PRICE12 WHERE ticker = '{ticker}'"
                    query2 = f"SELECT * FROM news S WHERE TICKER = '{ticker}'"
                    # Execute queryzs
                    cursor.execute(query1)
                    result1 = cursor.fetchall()
                    cursor.execute(query2)
                    result2 = cursor.fetchall()
                    # Fetch results
                    # Create DataFrame
                    df1 = pd.DataFrame(result1)
                    df2 = pd.DataFrame(result2, columns=['news_date', 'ticker', 'title', 'url'])
                    df2 = df2.drop('ticker',axis=1)
                    # Close connection (no need to commit for SELECT queries)
                    df1[0] = pd.to_datetime(df1[2])
                    fig = go.Figure(data=[go.Candlestick(x=df1[2], open=df1[4], high=df1[5], low=df1[6], close=df1[7])])
                    fig.update_layout(xaxis=dict(rangeslider=dict(visible=False)))
                    fig.update_traces(increasing_line_color='red', decreasing_line_color='blue')
                    st.plotly_chart(fig)
                    df3 = df2.drop('url',axis=1)
                    new_data = pd.DataFrame({
                    "날짜": df2["news_date"],
                    "제목": df2["title"],
                    "URL": df2["url"]
                    })
                    new_data.set_index(['날짜'], inplace=True)
                    column_config={"URL": st.column_config.LinkColumn()}
                    st.dataframe(new_data, column_config=column_config)
                    connection.close()
            elif option1 == '2차전지':
                option2 = st.selectbox("원하는 종목을 골라주세요", list(ticker_dicts.keys()))
                ticker = ticker_dicts.get(option2)
                if option2: # option2가 선택된 경우에만 데이터베이스에서 데이터를 가져옵니다.
                    query1 = f"SELECT * FROM PRICE2 WHERE ticker = '{ticker}'"
                    query2 = f"SELECT * FROM news S WHERE TICKER = 'A{ticker}'"
                    # Execute queryzs
                    cursor.execute(query1)
                    result1 = cursor.fetchall()
                    cursor.execute(query2)
                    result2 = cursor.fetchall()
                    # Fetch results
                    # Create DataFrame
                    df1 = pd.DataFrame(result1)
                    df2 = pd.DataFrame(result2, columns=['news_date', 'ticker', 'title', 'url'])
                    df2 = df2.drop('ticker',axis=1)
                    # Close connection (no need to commit for SELECT queries)
                    df1[0] = pd.to_datetime(df1[2])
                    fig = go.Figure(data=[go.Candlestick(x=df1[2], open=df1[3], high=df1[4], low=df1[5], close=df1[6])])
                    fig.update_layout(xaxis=dict(rangeslider=dict(visible=False)))
                    fig.update_traces(increasing_line_color='red', decreasing_line_color='blue')
                    st.plotly_chart(fig)
                    df3 = df2.drop('url',axis=1)
                    new_data = pd.DataFrame({
                    "날짜": df2["news_date"],
                    "제목": df2["title"],
                    "URL": df2["url"]
                    })
                    new_data.set_index(['날짜'], inplace=True)
                    column_config={"URL": st.column_config.LinkColumn()}
                    st.dataframe(new_data, column_config=column_config)
                    connection.close()
                    
            else:
                st.write(f'다시골라주세요: {option1}')
    elif selected_option == '지도':

        data = pd.DataFrame({
        'latitude': [37.494630],
        'longitude': [127.030087]
        })

        # 데이터를 사용하여 지도 생성
        st.map(data)
        