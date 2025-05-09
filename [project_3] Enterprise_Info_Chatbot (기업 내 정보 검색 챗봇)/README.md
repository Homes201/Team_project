# 🚄 BRT: GPT 기반 신입사원 Q&A 챗봇

<p align="center">
  <img src="https://github.com/user-attachments/assets/19fa9782-5046-4bb4-b383-6cf727140fb4" width="1000"/>
</p>

---

## 📌 프로젝트 개요

**BRT(Bot for Railway Trainees)**는 신입사원이 복잡한 회사 규정과 정책을 빠르게 이해하고 적응할 수 있도록 돕는 **문서 기반 질의응답 챗봇**입니다.  
GPT API, LangChain, ChromaDB를 기반으로 구축되었으며, 신뢰성 있는 정보 제공을 목표로 개발하였습니다.

---

## 🎯 프로젝트 목표

- **Q&A 챗봇 개발**: 신입사원이 자주 묻는 질문에 대해 공식 문서 기반으로 답변 제공  
- **정보 신뢰성 확보**: RAG(Retrieval Augmented Generation)를 통해 할루시네이션 최소화

---

## 🧠 주요 기능

- PDF 문서 업로드 및 텍스트 추출  
- GPT 기반 문서 요약 제공  
- LangChain + VectorDB 기반 질의응답 챗봇  
- Streamlit UI로 실시간 인터페이스 제공

---

## 🔨 기술 스택

<div>
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/streamlit%20-%23FF0000.svg?style=for-the-badge&logo=streamlit&logoColor=white">
<img src="https://img.shields.io/badge/openai-0769AD?style=for-the-badge&logo=openai&logoColor=black">
<img src="https://img.shields.io/badge/langchain-F7DF1E?style=for-the-badge&logo=langchain&logoColor=black">
<img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white">
</div>

---

## 📁 데이터 수집 및 구성

- 실제 철도회사 문서 기반 수집 (규정/정책/가이드라인)
- 주요 카테고리:
  - 인사 및 근무  
  - 복지 및 혜택  
  - 행동 및 윤리  
  - 교육 및 훈련  
  - 보수 및 포상  
  - 안전관리, 자산관리, 정보보안 등  

---

## 🧹 전처리 및 AI 파이프라인

- **텍스트 정제**: 문서 내 불필요한 문구 제거 및 구조 정리  
- **임베딩**: OpenAI Embeddings → ChromaDB 저장  
- **RAG 체인 구성**:
  - Retriever: Chroma  
  - Model: GPT-4o-mini (ChatOpenAI)  
  - 프롬프트 템플릿 + parser 체인 구성

---

## 🏗️ 프로젝트 구조

``` python
project/
├── app.py # Streamlit 메인 앱
├── chains/ # LangChain 체인 모듈
├── utils/ # 텍스트 처리, 임베딩 유틸
├── db/ # Chroma 벡터 저장소
├── docs/ # 테스트용 문서 샘플
└── README.md
```

---

## ▶️ 실행 방법

```bash
# 의존성 설치
pip install -r requirements.txt

# 앱 실행
streamlit run app.py
```

---

## 🖥️ UI 미리보기
<img src="screenshots/ui_demo.png" width="700"/>

---

## 🧪 예시 질의응답 결과
Q . "교육 훈련 규정문서에서 제1조에 대해 말해줘"

<table>
  <tr>
    <td style="width: 50%; vertical-align: top;">
      <h3>할루시네이션 최소화 전 </h3>
      <p>챗봇이 정책 및 규정을 정확히 참고 못하고 엉뚱한 응답을 제공함.</p>
      <ul>
        <li>A1.  제1(목적)는 운전교육센터 운영규정의 목적을 규정하고 있습니다. 이 조항의 내용은 철도안전 법 제16조 제3항에 따라, 주식회사 비알(주)BR)이 시행하는 고속철도차량 운전면허 교육 및 직무 교육의 내용, 방법, 운전업무종사자의 안전교육 및 직무교육의 내용, 방법, 절차, 평가 등에 관한 필요한 사항을 정하는 것을 목적으로 하고 있습니다. 이는 고속철도 차량 운전업무 안정성과 효율성을 높이고, 철도 운영에 필요한 인재를 양성하기 위한 기준을 마련하는 데 그 의의가 있습니다. 이 조항은 규정의 전반적인 방향성과 목표를 제시하며, 교육을 통해 확보하고자 하는 안전과 전문성을 강조하고 있습니다.</li>
      </ul>
    </td>
    <td style="width: 50%; vertical-align: top;">
      <h3>할루시네이션 최소화 후</h3>
      <p>챗봇이 특정 질문에 정확한 문서에 답을 제공하는 모습을 제공함</p>
      <ul>
        <li>A2. 제1조 교육훈련 규정에 따르면, 본 규정의 목적은 직원의 직무능력 향상과 전문성을 강화하기 위한 세계적인 교육 훈련을 제공하는 것입니다. 이를 통해 직원들이 지속적으로 성장하고 조직의 목표에 기여할 수 있도록 지원합니다. 또한, 교육 훈련의 대상, 방법, 진행 절차 및 평가 기준에 대한 구체적인 사항이 포함되어 있으며, 직원들은 정기적으로 제공되는 교육에 참여해야할 의무가 있습니다. 회사는 교육 훈련의 기회를 균등하게 제공하며, 모든 직원이 공정하게 혜택을 받을 수 있도록 노력하고 있습니다.</li>
        <li>참고 서식: 교육 훈련 규정 제1조 내용 요약.</li>
      </ul>
    </td>
  </tr>
</table>

---

## 🧑‍🤝‍🧑 팀원 및 역할

| 이름   | 역할                                       |
|--------|--------------------------------------------|
| 안준용 | 데이터 전처리, 벡터 DB 구축, LangChain 구축     |
| 박진효 | 벡터 DB 구축, LangChain 구축                   |
| 권오셈 | LangChain 구축, Streamlit UI, Git 관리        |
| 전욱진 | 데이터 수집 및 전처리, 로고 디자인             |
| 하상집 | LangChain 구축, UI 개발, 문서화               |
| 김현재 | UI 개발, 문서화                             |

---

## 🧾 한 줄 회고

| 이름   | 회고                                                     |
|--------|----------------------------------------------------------|
| 안준용 | 어쩌다보니 팀장을 하게 되었는데, 팀원들 따라와줘서 고맙습니다.     |
| 박진효 | 처음엔 걱정됐지만 큰 문제 없이 마무리되어 다행입니다.             |
| 권오셈 | 함께한 시간이 값졌고 많이 배웠습니다.                        |
| 전욱진 | 시간이 촉박했지만 잘 마무리되어 감사드립니다.                   |
| 하상집 | 어려움 있었지만 협력으로 극복해서 좋았습니다.                 |
| 김현재 | 서포트하며 많이 배웠습니다. 고생 많으셨습니다.                 |
