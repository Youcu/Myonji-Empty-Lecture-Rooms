# 🏫 컴퓨터공학과 빈 강의실 찾기

학과 강의실 시간표 Excel 파일을 기반으로 빈 강의실 정보를 시각화하는 Streamlit 웹 애플리케이션입니다.

## 📋 프로젝트 개요

### 목적
공강 시간에 빈 강의실을 활용해서 공부하거나, 미리 수업준비를 하는 학생들이 여럿 있습니다. 하지만, 본인의 시간표는 알아도 강의실 별 시간표는 모르기에 헛걸음하는 경우가 많습니다. 이를 보완하고자 해당 애플리케이션을 고안했습니다. 

### 구현 방법
학과 강의실 시간표 Excel 파일(.xls, .xlsx)을 분석하여 요일별 빈 강의실 정보를 직관적으로 제공하는 웹 애플리케이션을 개발합니다.
이때 컴퓨터공학과와 정보통신학과가 겹치는 강의실이 있으므로, 정보통신학과의 강의실 시간표도 같이 활용합니다. 

### 주요 기능
- **Excel 파일 자동 처리**: `./resources/` 디렉토리의 모든 Excel 파일을 자동으로 읽고 처리
- **파일 형식 변환**: `.xls` 파일을 `.xlsx`로 자동 변환 후 원본 삭제
- **병합 셀 처리**: Excel의 병합된 셀을 자동으로 해제하여 데이터 추출
- **스케줄 패턴 분석**: 정규식을 사용하여 강의 시간표에서 요일, 시간, 강의실 정보 추출
- **빈 시간 계산**: IntervalTree 알고리즘을 사용하여 효율적인 빈 시간대 계산
- **직관적인 UI**: Streamlit을 활용한 사용자 친화적인 웹 인터페이스

### 기술 스택
- **Programming Language**: Python 3.x
- **Web Framework**: Streamlit
- **Data Processing**: Pandas, OpenPyXL, xlrd
- **Algorithm**: IntervalTree
- **Environment**: Python Virtual Environment

## 🚀 (개발자 대상) 설치 및 실행

### 1. 저장소 클론
```bash
git clone <repository-url>
cd EmptyRoom
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv emptyroomVENV
source emptyroomVENV/bin/activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 애플리케이션 실행
```bash
streamlit run empty_lecture_room.py
```

## 🚀 (사용자 대상) 실행
⚠️ Notice: 본 서비스는 Streamlit 무료 호스팅을 기반으로 제공됩니다. 일정 시간 동안 사용하지 않으면, Streamlit 정책에 따라 앱이 자동으로 일시 중지됩니다. 이로 인해 접속 시 웹페이지가 즉시 표시되지 않을 수 있으며, 잠시 대기하시면 서버가 다시 활성화되면서 정상적으로 페이지가 열립니다.

Link: https://myonji-empty-lecture-rooms.streamlit.app

## 📁 프로젝트 구조

```
EmptyRoom/
├── empty_lecture_room.py    # 메인 애플리케이션 파일
├── requirements.txt         # Python 의존성 목록
├── prd.md                  # 프로젝트 요구사항 문서
├── README.md               # 프로젝트 설명서
├── resources/              # Excel 파일 저장 디렉토리
│   ├── *.xlsx             # 강의실 시간표 Excel 파일들
└── sample/                # 샘플 파일
    └── ui.png             # UI 참조 이미지
```

## 🔧 사용 방법

1. **Excel 파일 준비**: 강의실 시간표 Excel 파일을 `./resources/` 디렉토리에 저장
2. **애플리케이션 실행**: `streamlit run empty_lecture_room.py` 명령어로 실행
3. **요일 선택**: 웹 인터페이스에서 원하는 요일을 선택
4. **결과 확인**: 선택한 요일의 빈 강의실 시간표를 테이블로 확인

## 📊 데이터 형식

### Excel 파일 요구사항
- **파일 형식**: `.xls` 또는 `.xlsx`
- **시간표 위치**: L열(12번째 열)에 시간표 정보 포함
- **시간표 형식**: `요일HH:MM-HH:MM (강의실번호)`
  - 예시: `월09:00-11:50 (Y5407)`, `화13:00-14:50 (Y5401)`

### 정규식 패턴
```regex
^(?P<day>[월화수목금토일])(?P<start>\d{2}:\d{2})-(?P<end>\d{2}:\d{2}) \((?P<lecture_room>Y\d{4})\)$
```

## 🎨 UI 특징

- **요일 선택**: 월요일~금요일 중 선택 (주말인 경우 월요일 기본값)
- **시간 범위**: 09:00 ~ 21:00 (1시간 단위)
- **색상 구분**:
  - 🔵 **Possible** (#455f8e): 사용 가능한 강의실
  - 🔴 **Impossible** (#b86666): 사용 중인 강의실
- **반응형 테이블**: 전체 화면 너비 사용, 고정 높이로 모든 데이터 표시

## 🔍 주요 알고리즘

### IntervalTree 기반 빈 시간 계산
- 각 강의실별로 사용 중인 시간대를 IntervalTree로 관리
- 시간대별로 겹치는 스케줄이 있는지 효율적으로 확인
- O(log n) 시간 복잡도로 빠른 검색 가능

### 병합 셀 처리
- Excel의 병합된 셀을 자동으로 감지하고 해제
- Forward fill 방식을 사용하여 데이터 완성
- 정확한 스케줄 정보 추출 보장

---

**개발자**: Hooby  
**개발일**: 2025-09-14  
