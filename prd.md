# PRD: Empty Lecture Rooms Streamlit App
## 1. Overview 
- 목적 : 학과 강의실 시간표 Excel 파일(.xls, .xlsx)을 기반으로 빈 강의실 정보를 시각화하는 Streamlit 앱을 실행한다.
- 실행 환경: Cursor IDE + Python 3.x (venv)
- 주요 기능:
  - ./resources/ 디렉토리에 존재하는 모든 Excel 파일을 자동으로 읽기
  - xls 이면 xlsx로 변환 
  - 모든 xlsx 파일 병합
  - xlsx의 병합셀 해제 처리 (unmerge_)
  - 강의 시간(start, end)을 24시간제 정수형으로 변환
  - 요일별, 강의실별 빈 시간대를 IntervalTree로 계산
  - Streamlit UI를 통해 선택된 요일의 빈 강의실 테이블 시각화
  
## 2. Requirements
### 기능 요구사항 
1. ./resources/ 디렉토리 내의 모든 .xls / .xlsx 파일 탐색
2. .xls 파일은 .xlsx로 변환 후 원본 삭제
3. Excel 병합 셀 해제 후 데이터 읽기
4. L열(Time Table)에서 요일+시간+강의실 패턴 추출
   - RegEX: 
        ```^(?P<day>[월화수목금토일])(?P<start>\d{2}:\d{2})-(?P<end>\d{2}:\d{2}) \((?P<lecture_room>Y\d{4})\)$```
5. 요일별 room_list 및 빈 시간 계산 
6. Streamlit UI 제공
   - 요일 선택 박스 (월~금, default: 오늘 혹은 주말이면 월)
   - 빈 강의실 시간표 테이블 표시 (색상 강조: Possible->#455f8e, Impossible->#b86666)
   - st.table로 데이터프레임을 띄운다. 
   - th, td에 대해서 border는 solid 1px white, font-color는 white로 지정한다. 
   - th는 X-axis 방향(Column Schema)으로 강의실 번호(ex. Y5401)를 띄우고, Y-axis 방향 ((0, *)|except(0,0))으로는 HH:MM을 한시간 단위로 띄운다. 
   - UI는 ./sample/ui.png를 참조한다.  

### 비기능 요구사항 
- Python venv 기반 실행 (이미 emptyroomVENV 생성된거 이용)

## 3. Installation 
기능 구현에 필요한 모듈을 pip3 으로 설치하고, 코드 구현 완료 후 pip3 freeze > requirements.txt 진행