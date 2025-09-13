import streamlit as st
import pandas as pd
import os
import re
from datetime import datetime
from intervaltree import IntervalTree
import glob

# pandas future warning 해결
pd.set_option('future.no_silent_downcasting', True)

def convert_xls_to_xlsx(xls_file):
    """xls 파일을 xlsx로 변환하고 원본 삭제"""
    try:
        # xls 파일 읽기
        df = pd.read_excel(xls_file, header=None)
        # xlsx로 저장
        xlsx_file = xls_file.replace('.xls', '.xlsx')
        df.to_excel(xlsx_file, index=False, header=False)
        # 원본 xls 파일 삭제
        os.remove(xls_file)
        return xlsx_file
    except Exception as e:
        st.error(f"파일 변환 중 오류 발생: {e}")
        return None

def unmerge_cells(df):
    """병합된 셀을 해제하여 데이터를 채움"""
    # 병합된 셀의 값을 앞의 값으로 채움
    df = df.ffill(axis=0)
    df = df.ffill(axis=1)
    # downcasting 경고 해결
    df = df.infer_objects(copy=False)
    return df

def extract_schedule_info(text):
    """시간표 텍스트에서 요일, 시작시간, 종료시간, 강의실 정보 추출"""
    if pd.isna(text) or not isinstance(text, str):
        return None
    
    # 정규식 패턴: ^(?P<day>[월화수목금토일])(?P<start>\d{2}:\d{2})-(?P<end>\d{2}:\d{2}) \((?P<lecture_room>Y\d{4})\)$
    pattern = r'^(?P<day>[월화수목금토일])(?P<start>\d{2}:\d{2})-(?P<end>\d{2}:\d{2}) \((?P<lecture_room>Y\d{4})\)$'
    match = re.match(pattern, text.strip())
    
    if match:
        day = match.group('day')
        start_time = match.group('start')
        end_time = match.group('end')
        room = match.group('lecture_room')
        
        # 시간을 24시간제 정수로 변환 (분 단위)
        start_hour, start_min = map(int, start_time.split(':'))
        end_hour, end_min = map(int, end_time.split(':'))
        
        start_minutes = start_hour * 60 + start_min
        end_minutes = end_hour * 60 + end_min
        
        return {
            'day': day,
            'start': start_minutes,
            'end': end_minutes,
            'room': room
        }
    return None

def load_and_process_excel_files():
    """resources 디렉토리의 모든 Excel 파일을 로드하고 처리"""
    resources_dir = './resources'
    all_schedules = []
    
    # xls 파일들을 xlsx로 변환
    xls_files = glob.glob(os.path.join(resources_dir, '*.xls'))
    for xls_file in xls_files:
        xlsx_file = convert_xls_to_xlsx(xls_file)
        if xlsx_file:
            print(f"변환 완료: {os.path.basename(xls_file)} -> {os.path.basename(xlsx_file)}")
    
    # xlsx 파일들 처리
    xlsx_files = glob.glob(os.path.join(resources_dir, '*.xlsx'))
    
    for file_path in xlsx_files:
        try:
            # Excel 파일 읽기
            df = pd.read_excel(file_path, header=None)
            
            # 병합 셀 해제
            df = unmerge_cells(df)
            
            # L열(인덱스 11)에서 시간표 정보 추출
            for idx, row in df.iterrows():
                if len(row) > 11 and pd.notna(row.iloc[11]):
                    schedule_info = extract_schedule_info(row.iloc[11])
                    if schedule_info:
                        all_schedules.append(schedule_info)
            
        except Exception as e:
            st.error(f"파일 처리 중 오류 발생 {file_path}: {e}")
    
    return all_schedules

def get_all_rooms(schedules):
    """모든 스케줄에서 강의실 목록 추출 (요일에 관계없이)"""
    all_rooms = set()
    for schedule in schedules:
        all_rooms.add(schedule['room'])
    return sorted(list(all_rooms))

def calculate_empty_times(schedules, selected_day, all_rooms):
    """선택된 요일의 빈 시간 계산"""
    # 해당 요일의 스케줄만 필터링
    day_schedules = [s for s in schedules if s['day'] == selected_day]
    
    # 각 강의실별로 IntervalTree 생성
    room_trees = {}
    for room in all_rooms:
        tree = IntervalTree()
        for schedule in day_schedules:
            if schedule['room'] == room:
                tree[schedule['start']:schedule['end']] = True
        room_trees[room] = tree
    
    # 시간대별 빈 시간 계산 (9:00-21:00)
    time_slots = []
    for hour in range(9, 22):  # 9시부터 21시까지
        time_slots.append(f"{hour:02d}:00")
    
    # 결과 데이터프레임 생성
    result_data = []
    for time_slot in time_slots:
        hour = int(time_slot.split(':')[0])
        minute_start = hour * 60
        minute_end = (hour + 1) * 60
        
        row = {'시간': time_slot}
        for room in all_rooms:
            tree = room_trees[room]
            # 해당 시간대에 겹치는 스케줄이 있는지 확인
            overlapping = tree.overlap(minute_start, minute_end)
            if overlapping:
                row[room] = 'Impossible'
            else:
                row[room] = 'Possible'
        result_data.append(row)
    
    return pd.DataFrame(result_data)

def apply_table_styling(df):
    """테이블에 CSS 스타일 적용"""
    def style_cell(val):
        if val == 'Possible':
            return 'background-color: #455f8e; color: white; border: 1px solid white;'
        elif val == 'Impossible':
            return 'background-color: #b86666; color: white; border: 1px solid white;'
        else:
            return 'color: white; border: 1px solid white;'
    
    styled_df = df.style.map(style_cell)
    return styled_df

def main():
    st.set_page_config(
        page_title="컴퓨터공학과 빈 강의실 찾기",
        page_icon="🏫",
        layout="wide"
    )
    
    st.subheader("🏫 컴퓨터공학과 빈 강의실 찾기")
    
    # 요일 선택
    days = ['월', '화', '수', '목', '금']
    today = datetime.now().weekday()  # 0=월요일, 6=일요일
    
    # 오늘이 주말이면 월요일을 기본값으로, 아니면 오늘을 기본값으로
    if today >= 5:  # 토요일(5) 또는 일요일(6)
        default_day = '월'
    else:
        default_day = days[today]
    
    selected_day = st.selectbox(
        "요일을 선택하세요:",
        days,
        index=days.index(default_day)
    )
    
    def load_data():
        return load_and_process_excel_files()
    
    schedules = load_data()
    
    if not schedules:
        st.warning("처리된 스케줄 데이터가 없습니다. resources 폴더에 Excel 파일이 있는지 확인해주세요.")
        return
    
    # 모든 강의실 목록 추출 (요일에 관계없이)
    all_rooms = get_all_rooms(schedules)
    
    # 빈 시간 계산
    empty_times_df = calculate_empty_times(schedules, selected_day, all_rooms)
    
    if empty_times_df.empty:
        st.warning(f"{selected_day}요일의 데이터가 없습니다.")
        return
    
    # 스타일 적용된 테이블 표시
    styled_df = apply_table_styling(empty_times_df)
    st.dataframe(styled_df, width='stretch', height=492, hide_index=True)
    
if __name__ == "__main__":
    main()
