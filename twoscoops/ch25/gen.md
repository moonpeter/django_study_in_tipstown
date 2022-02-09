# Chap25. Documentation - Be Obsessed

### 문서화 도구들

- Markdown
- MkDocs
- Sphinx

## 25.1 Use GitHub-Flavored Markdown for Docs

최근에는 GitHub Flavored Markdown(GFM)을 많은 회사에서 채택하고 있습니다.

- github.github.com/gfm/
- django-rest-framework.org/

## 25.2 Use MkDocs or Sphinx with Myst to Generate Documentation From Markdown

MkDocs와 Sphinx with Myst는 .md 파일을 랜더링해주는 도구입니다.

HTML, 레이텍(LaTex), 메뉴얼 페이지, 평문으로 출력합니다.

- [https://www.mkdocs.org/#getting-started](https://www.mkdocs.org/#getting-started)
- [https://myst-parser.readthedocs.io/en/latest/sphinx/intro.html](https://myst-parser.readthedocs.io/en/latest/sphinx/intro.html)

문서를 주기적으로 빌드하세요.

문서를 오랫만에 빌드를 하면 실패하거나 포맷 양식이 바뀌는 증 문제가 생길 수 있고, 그러한 문제들을 역추적하는 것은 굉장히 귀찮은 일입니다. 정기적으로 빌드하는 습관을 들이세요. 아니면 CI/CD 프로세스의 일부로 만드는 것도 좋은 방법입니다.

## 25.3 What Docs Should Django Projects Contain?

Developer-facing documentation은 개발자가 프로젝트를 셋업하고 관리하는데 필요한 설명과 가이드 라인입니다.

설치, 개발, 아키텍처 노트, 테스트 케이스를 실행하는 방법, 코드의 PR 방법 등이 포함됩니다.

파일 이름 / 디렉터리 | 문서 성격 | 주의
---|---|---
README.md | 모든 파이썬 프로젝트 소스 저장소 루트에 있어야 한다. | 이 프로젝트가 어떤 프로젝트인지 짧은 문장이라도 설명을 제공해야 한다. docs/ 디렉터리 안에 설치 방법에 대한 링크를 제공해야 한다.
docs/ | 프로젝트 문서들이 위치하게 된다. 파이썬 커뮤니티 표준이다. | 디렉터리
docs/deployment.md | 이 문서 덕분에 하루정도 쉴 수 있을 것이다. | 프로젝트 설치/업데이트에 대한 단계별 정리를 제공
docs/installation.md | 프로젝트를 처음 접하거나, 새로운 환경에서 프로젝트를 세팅할때 유용할 것이다. | 프로젝트 셋업에 대해 다른 개발자와 자신을 위해 단계별로 정리를 제공
docs/architecture.md | 프로젝트가 진행됨에 따라 각 요소가 어떻게 구성되어 있는지에 대한 이해를 돕는 가이드 | 프로젝트를 간단 명료하게 표현하는 문서이다. 최대한 명료하게하거나 최대한 세세하게 상황에 맞게 작성하자. 프로젝트 초창기부터 관심을 갖고 작성하면 좋다.

## 25.4 Additional Markdown Documentation Resources

- [https://www.python.org/dev/peps/pep-0257/](https://www.python.org/dev/peps/pep-0257/)
- [https://readthedocs.org/](https://readthedocs.org/)
- [https://pythonhosted.org/](https://pythonhosted.org/)
- [https://en.wikipedia.org/wiki/Markdown](https://en.wikipedia.org/wiki/Markdown)
- [https://documentup.com/](https://documentup.com/)

## 25.5 The ReStructuredText Alternative

ReStructuredText는 Markdown보다 많은 기능이 내장되어 있어서 배우기가 어렵고 쓰기가 느립니다.

Django나 파이썬 및 오래된 라이브러리에서 여전히 사용되고 있습니다.

### 25.5.1 ReStructuredText Resources

- [https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html](https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html)
- [https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html)
- [https://www.sphinx-doc.org/en/master/](https://www.sphinx-doc.org/en/master/)

## 25.6 When Documentation Needs to Be Convert to/from Markdown or ReStructuredText

Pandoc은 한 마크업 포맷을 다른 포맷으로 변환해 주는 명령행 도구입니다.

```bash
# To convert a ReStructuredText document to GitHub-Flavored Markdown
$ pandoc -t gfm README.rst -o README.md
# To convert a Markdown document to ReStructuredText 
$ pandoc -f gfm README.md -o README.rst
```

- [https://pandoc.org/](https://pandoc.org/)

## 25.7 Wikis and Other Documentation Methods

개발자를 위한 문서를 프로젝트 안에 포함시킬 수 없는 경우

- 위키나 온라인 문서에 저장
- 워드 프로세스 문서

어떤 형식이든 없는 것보다는 낫습니다.

## 25.8 Ensuring that Code is Documented

문서도 커버리지를 관리할 수 있습니다.

아래의 라이브러리를 사용해서 관리할 수 있습니다.

- [https://interrogate.readthedocs.io/en/latest/](https://interrogate.readthedocs.io/en/latest/)

