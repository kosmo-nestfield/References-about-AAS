# 1. 개요  
본 Repository는 AAS 및 AAS기반 제조데이터 수집/저장 솔루션의 여러 레퍼런스들을 포함합니다.  
  
# 2. AAS기반 제조데이터 수집/저장 솔루션  
* [**AAS기반 데이터 수집/저장 실행 가이드 문서**](https://github.com/kosmo-nestfield/References-about-AAS/tree/main/AAS%20%EA%B8%B0%EB%B0%98%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EC%88%98%EC%A7%91-%EC%A0%80%EC%9E%A5%20%EC%8B%A4%ED%96%89%20%EA%B0%80%EC%9D%B4%EB%93%9C%EB%AC%B8%EC%84%9C)  
> - Guide1 AAS 신규작성  
>   AAS 파일 신규 작성 방법에 대해 설명한 문서입니다.  
> - Guide2 AAS를 사용한 필드데이터 수집방법  
>   작성한 AAS를 기반으로 엣지 게이트웨이에서 필드 데이터 매핑 및 수집하는 방법에 대해 설명한 문서입니다.  
> - Guide3 AAS를 사용한 클라우드 데이터 수집저장 방법  
>   엣지 게이트웨이에서 수집한 제조 데이터를 클라우드에서 수집/저장, 시각화 한 방법에 대해 설명한 문서입니다.  
> - Guide4 AAS 검증 방법  
>   작성한 AAS가 스키마에 맞게 작성되었는지 검증하는 방법에 대해 설명한 문서입니다.  
  
* [**실습용 AAS 예제 파일**](https://github.com/kosmo-nestfield/References-about-AAS/tree/main/%EC%8B%A4%EC%8A%B5%EC%9A%A9%20AAS%20%EC%98%88%EC%A0%9C%20%ED%8C%8C%EC%9D%BC)  
> - 실습 교육용 예제  
>   AAS 신규 제작 실습 시 사용된 기본 뼈대 AAS 파일입니다.  
> - 완성 예제  
>   실습 교육용 AAS 파일을 기반으로 제작된 완성된 AAS 파일 예제입니다.  
  
# 3. AAS 레퍼런스
* [**AASX Package Explorer**](https://github.com/admin-shell-io/aasx-package-explorer/releases)
> 최신 버전의 AASX Package Explorer 실행파일 및 소스코드를 다운로드 받을 수 있는 링크입니다.  
> 링크 내의 **aasx-package-explorer.[최신 날짜].alpha.zip** 파일을 받아 사용하시면 됩니다.

* [**AAS Validation**](https://github.com/admin-shell-io/schema-validation)  
> AAS를 [**스키마**](https://github.com/admin-shell-io/aas-specs) 파일 기반으로 검증하는 파일의 소스코드 입니다.  
> .NET Core 3.1. 환경에서 동작하며, 명령 실행창(cmd)에서 src/ 디렉토리로 진입하여 아래 명령어를 사용해 검증작업을 할 수 있습니다.  
> ```dotnet publish -c Release -o out/schema-validation```  
  
* [**AAS Samples**](http://www.admin-shell-io.com/samples/)
> 여러 제조업체의 샘플 AAS 파일입니다. AASX Package Explorer에서 파일 내용 확인 가능합니다.  

