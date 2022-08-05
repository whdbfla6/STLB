## 분석과제

[빅콘테스트](https://www.bigcontest.or.kr)


- **제주도 쓰레기 배출량을 예측, 배출량 감소 방안 도출**
- 빅콘테스트 데이터 분석 공모전에 참여해 최우수상 수상(신한카드 대표이사상)
- 대회기간 : 2021년 8월 3일 ~ 2021년 11월
- [모델링(STLB) 코드](https://github.com/whdbfla6/STLB/blob/main/module/stlb.py)

## 프로젝트 내 역할


1. **모델링**

[](https://github.com/whdbfla6/STLB)

![모델링](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/58a9f7d2-b79d-41fb-8bbd-1f3ec546b8cb/스크린샷_2022-03-21_오후_12.43.17.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220805%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220805T061838Z&X-Amz-Expires=86400&X-Amz-Signature=d1bca2ba4f66123fef3f8a41c6fbe9f202a86a9b847c22169277fc13c7726c97&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22%25EC%258A%25A4%25ED%2581%25AC%25EB%25A6%25B0%25EC%2583%25B7%25202022-03-21%2520%25EC%2598%25A4%25ED%259B%2584%252012.43.17.png%22&x-id=GetObject)

- 주어진 데이터는 시계열 데이터이기 때문에 기존 배깅 모형을 수정하여 새로운 모형을 직접 구축
- STL 시계열 분해를 통해 X와 Y를 각각 추세성, 계절성, 잔차 세가지로 분해 → 추세는 추세끼리 계절은 계절끼리 그리고 잔차는 잔차끼리 예측하고, 각각의 예측값을 곱해 원래의 값으로 복원
- 추세성으로 추세성을 예측하고, 계절성으로 계절성을 예측하기 때문에 모형이 시간이라는 속성을 학습하지 못하더라도 문제가 되지 않는다고 판단. (예를들어 시간에 따라 내국인 유동인구가 1 2 3 으로 증가하는 값을 가질 때 쓰레기 배출량이 10 20 30으로 증가하는 추세를 보인다고 가정 →  데이터를 학습하는 경우 내국인 유동인구가 큰 값을 가질수록 쓰레기 배출량이 큰 값을 가진다고 학습하기 때문에 시간이라는 속성이 반영되지 않더라도 문제가 되지 않는다)
- 잔차가 정상성을 보이는 주기를 개별적으로 찾아서 분해

2. **검색데이터 활용 아이디어 제안** 

**기상데이터 확보**

- 쓰레기 배출량 그래프를 그려보았을 때 눈에 띄게 감소하는 구간을 확인할 수 있었음 → 그 시기에 강풍, 한파 및 태풍 특보가 있었다는 것을 확인

![기상데이터](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/43a99221-3779-4d25-b0fe-1199f92fb7fc/스크린샷_2022-03-21_오후_12.47.05.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220805%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220805T061740Z&X-Amz-Expires=86400&X-Amz-Signature=8e22259774210aa3debb1c6137d7b2d3b4d57898cd183588251a36546bc7bed8&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22%25EC%258A%25A4%25ED%2581%25AC%25EB%25A6%25B0%25EC%2583%25B7%25202022-03-21%2520%25EC%2598%25A4%25ED%259B%2584%252012.47.05.png%22&x-id=GetObject)

- 기상데이터를 확보하고 싶었으나 현재시점의 데이터를 구하는 것이 쉽지 않음 → 검색데이터로 대체하여 데이터 수집
    - 포털사이트에서 제공하고 있는 검색 데이터를 통해 `태풍` `한파` `강풍` 에 대한 검색량이 급증하는 시기에 기상악화가 있다는 것을 확인할 수 있었음
    - 실질적 강풍 수치나 태풍의 정도가 아닌 기상악화 현상의 여부(binary data)만 알아도 급감 요인을 캐치할 수 있을 거라 판단 → 기상데이터가 아닌 검색데이터를 수집
    - 모델 성능을 높이는 데 큰 기여

**동네 특성 파악을 위해 검색 데이터 활용**

- 기상검색데이터 수집 후 다른 방면에도 검색데이터를 활용하고자 함
- 동네의 특성 별로 쓰레기 배출 양상이 다르다는 것을 확인하였으나 구분하기 위한 명확한 기준을 정하지 못한 상태 → 해결책으로 동네 별 검색데이터 활용
- `검색_관광 변수` : 사람들이 검색 포털 사이트에 '제주 관광' '제주 갈만한 곳' '제주 맛집' 등 검색키워드를 해당 일자에 얼마나 많이 검색을 하였는지를 나타낸 변수
    - 검색빈도가 높은 경우에 해당 날짜에 관광객이 급증했다는 것을 간접적으로 보여준다
    - 쓰레기 배출량에도 직접적으로 영향을 주는 요인이 됨
