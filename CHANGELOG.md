# Changelog

## v2.2.0 (2022-05-16)

### :sparkles: New
  -  Support for async.

### :arrow_up: Dependencies
  -  Add dep pytest-asyncio for async testing.

  -  Bump coverage from 6.3.2 to 6.3.3

  -  Bump flake8-comprehensions from 3.8.0 to 3.9.0

  -  Bump flake8-tidy-imports from 4.7.0 to 4.8.0

  -  Bump types-toml from 0.10.6 to 0.10.7

  -  Bump pre-commit from 2.18.1 to 2.19.0

  -  Bump flake8-tidy-imports from 4.6.0 to 4.7.0

  -  Bump types-toml from 0.10.5 to 0.10.6

  -  Bump mypy from 0.942 to 0.950

  -  Bump flake8-eradicate from 1.2.0 to 1.2.1

  -  Bump flake8-bugbear from 22.3.23 to 22.4.25

  -  Bump pytest from 7.1.1 to 7.1.2

### :memo: Documentation
  -  Added &quot;Mentions&quot; in README.md

## v2.1.0 (2022-04-24)

### :sparkles: New
  -  Now the parameters passed through &quot;args&quot; are also serialized.

    &#x60;&#x60;&#x60;python
    def func(i: int):
        return i
    
    assert func(&#x27;1&#x27;) &#x3D;&#x3D; 1
    &#x60;&#x60;&#x60;
    

### :recycle: Changes
  -  Small changes for release config

  -  no need &#x60;cfg&#x60; settings in editorconfig.

### :arrow_up: Dependencies
  -  Bump types-toml from 0.10.4 to 0.10.5

  -  Upgrade dependency black -&gt; black[d]

  -  Bump types-setuptools from 57.4.12 to 57.4.14

  -  Bump types-setuptools from 57.4.11 to 57.4.12

  -  Bump pre-commit from 2.17.0 to 2.18.1

  -  Bump black from 22.1.0 to 22.3.0

  -  Bump mypy from 0.941 to 0.942

  -  Bump flake8-bugbear from 22.3.20 to 22.3.23

  -  Bump flake8-bugbear from 22.1.11 to 22.3.20

  -  Bump pytest from 7.1.0 to 7.1.1

  -  Bump types-setuptools from 57.4.10 to 57.4.11

  -  Bump mypy from 0.940 to 0.941

  -  Bump mypy from 0.931 to 0.940

  -  Bump pytest from 7.0.1 to 7.1.0

## v2.0.1 (2022-03-09)

### :bug: Bugs
  -  Fixed a bug with working with the config of a model that does not have extra.

### :arrow_up: Dependencies
  -  Bump types-setuptools from 57.4.9 to 57.4.10

## v2.0.0 (2022-03-08)

### :boom: Breaking Changes
  -  Global refactoring. (Issues: [`#72`](https://github.com/mom1/api-client-pydantic/issues/72))

    - support for more use cases (fix #72).
    - &#x60;serialize_response&#x60; and &#x60;serialize_request&#x60; and &#x60;serialize&#x60; call signature changed.
    - &#x60;serialize_response&#x60; and &#x60;serialize_request&#x60; names are left for compatibility,
       it is better to use &#x60;params_serializer&#x60; and &#x60;response_serializer&#x60; instead.
    - Removed unnecessary dependencies.
    - Tests completely rewritten.
    - Decorating will only be done if necessary, which will positively affect performance.
    

### :arrow_up: Dependencies
  -  Bump pycln from 1.2.0 to 1.2.4

# [v1.2.2](https://github.com/mom1/api-client-pydantic/compare/1.2.1...1.2.2) (2022-02-24)

## :arrow_up: Dependencies
  -  Bump pytest from 6.2.5 to 7.0.1
    Bumps [pytest](https://github.com/pytest-dev/pytest) from 6.2.5 to 7.0.1.
    - [Release notes](https://github.com/pytest-dev/pytest/releases)
    - [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst)
    - [Commits](https://github.com/pytest-dev/pytest/compare/6.2.5...7.0.1)
    
    ---
    updated-dependencies:
    - dependency-name: pytest
      dependency-type: direct:development
      update-type: version-update:semver-major
    ...
    
    Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
  -  Bump pre-commit from 2.15.0 to 2.17.0
    Bumps [pre-commit](https://github.com/pre-commit/pre-commit) from 2.15.0 to 2.17.0.
    - [Release notes](https://github.com/pre-commit/pre-commit/releases)
    - [Changelog](https://github.com/pre-commit/pre-commit/blob/master/CHANGELOG.md)
    - [Commits](https://github.com/pre-commit/pre-commit/compare/v2.15.0...v2.17.0)
    
    ---
    updated-dependencies:
    - dependency-name: pre-commit
      dependency-type: direct:development
      update-type: version-update:semver-minor
    ...
    
    Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
  -  Bump flake8-comprehensions from 3.7.0 to 3.8.0
    Bumps [flake8-comprehensions](https://github.com/adamchainz/flake8-comprehensions) from 3.7.0 to 3.8.0.
    - [Release notes](https://github.com/adamchainz/flake8-comprehensions/releases)
    - [Changelog](https://github.com/adamchainz/flake8-comprehensions/blob/main/HISTORY.rst)
    - [Commits](https://github.com/adamchainz/flake8-comprehensions/compare/3.7.0...3.8.0)
    
    ---
    updated-dependencies:
    - dependency-name: flake8-comprehensions
      dependency-type: direct:development
      update-type: version-update:semver-minor
    ...
    
    Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
  -  Bump flake8-bugbear from 21.9.2 to 22.1.11
    Bumps [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) from 21.9.2 to 22.1.11.
    - [Release notes](https://github.com/PyCQA/flake8-bugbear/releases)
    - [Commits](https://github.com/PyCQA/flake8-bugbear/compare/21.9.2...22.1.11)
    
    ---
    updated-dependencies:
    - dependency-name: flake8-bugbear
      dependency-type: direct:development
      update-type: version-update:semver-major
    ...
    
    Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
  -  Bump isort from 5.9.3 to 5.10.1
    Bumps [isort](https://github.com/pycqa/isort) from 5.9.3 to 5.10.1.
    - [Release notes](https://github.com/pycqa/isort/releases)
    - [Changelog](https://github.com/PyCQA/isort/blob/main/CHANGELOG.md)
    - [Commits](https://github.com/pycqa/isort/compare/5.9.3...5.10.1)
    
    ---
    updated-dependencies:
    - dependency-name: isort
      dependency-type: direct:development
      update-type: version-update:semver-minor
    ...
    
    Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
## :memo: Documentation
  -  Update README.md

# [v1.2.1](https://github.com/mom1/api-client-pydantic/compare/v1.2.0...1.2.1) (2022-02-24)

## :recycle: Changes
  -  fix release template
  -  Improve &#x60;.gitignore&#x60;
  -  Improved all dev things
    - Changed formater to black
    - Reformat code
    - Added checks
    - pre-commit autoupdate
    
  -  commitlint is off, need research
  -  Upgrading a dependency doesn&#x27;t increase the version
  -  Small changes due to coverage analysis
  -  remove walrus operator for python 3.7 compatibility (#73) (Issues: [`#73`](https://github.com/mom1/api-client-pydantic/issues/73))
  -  Changelog generation job because now pre-commit generate changelog
## :memo: Documentation
  -  Update CHANGELOG.md

#### api-client-pydantic `v1.2.0` (2021-10-24)

##### ✨ New

- Set a new signature for function.

##### ♻️ Changes

- New changelog generation.
- New configs and pre-commit.

##### ⬆️ Dependencies

- ⬆️ Bumps [emoji](https://github.com/carpedm20/emoji) from 1.5.0 to 1.6.1.
  - [Release notes](https://github.com/carpedm20/emoji/releases)
  - [Changelog](https://github.com/carpedm20/emoji/blob/master/CHANGES.md)
  - [Commits](carpedm20/emoji@v1.5.0...v1.6.1)
- ⬆️ Bump all for flake8 4.

##### 📝 Docs

- Update README.md.


#### api-client-pydantic `v1.1.1` (2021-10-13)

##### 🐛 Bugs

- Fix case with typing.
  `def function(q: Optional[str]):`

##### ⬆️ Dependencies

- ⬆️ Bump pytest-cov from 2.12.1 to 3.0.0 (#54)
  Bumps [pytest-cov](https://github.com/pytest-dev/pytest-cov) from 2.12.1 to 3.0.0.
  - [Release notes](https://github.com/pytest-dev/pytest-cov/releases)
  - [Changelog](https://github.com/pytest-dev/pytest-cov/blob/master/CHANGELOG.rst)
  - [Commits](https://github.com/pytest-dev/pytest-cov/compare/v2.12.1...v3.0.0)
- ⬆️ Bump flake8-bugbear from 21.4.3 to 21.9.2 (#53)
  Bumps [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) from 21.4.3 to 21.9.2.
  - [Release notes](https://github.com/PyCQA/flake8-bugbear/releases)
  - [Commits](https://github.com/PyCQA/flake8-bugbear/compare/21.4.3...21.9.2)
- ⬆️ Bump emoji from 1.4.2 to 1.5.0 (#52)
  Bumps [emoji](https://github.com/carpedm20/emoji) from 1.4.2 to 1.5.0.
  - [Release notes](https://github.com/carpedm20/emoji/releases)
  - [Changelog](https://github.com/carpedm20/emoji/blob/master/CHANGES.md)
  - [Commits](https://github.com/carpedm20/emoji/compare/v.1.4.2...v1.5.0)
- ⬆️ Bump pytest from 6.2.4 to 6.2.5 (#50)
  Bumps [pytest](https://github.com/pytest-dev/pytest) from 6.2.4 to 6.2.5.
  - [Release notes](https://github.com/pytest-dev/pytest/releases)
  - [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst)
  - [Commits](https://github.com/pytest-dev/pytest/compare/6.2.4...6.2.5)
- ⬆️ Bump flake8-quotes from 3.2.0 to 3.3.0 (#49)
  Bumps [flake8-quotes](https://github.com/zheller/flake8-quotes) from 3.2.0 to 3.3.0.
  - [Release notes](https://github.com/zheller/flake8-quotes/releases)
  - [Commits](https://github.com/zheller/flake8-quotes/compare/3.2.0...3.3.0)
- ⬆️ Bump flake8-comprehensions from 3.5.0 to 3.6.1 (#48)
  Bumps [flake8-comprehensions](https://github.com/adamchainz/flake8-comprehensions) from 3.5.0 to 3.6.1.
  - [Release notes](https://github.com/adamchainz/flake8-comprehensions/releases)
  - [Changelog](https://github.com/adamchainz/flake8-comprehensions/blob/main/HISTORY.rst)
  - [Commits](https://github.com/adamchainz/flake8-comprehensions/compare/3.5.0...3.6.1)

##### 🌱 Other

- Release 1.1.1.


#### api-client-pydantic `v1.1.0` (2021-08-09)

##### ♻️ Changes

- Correct recognition of functions (#46)

##### ⬆️ Dependencies

- ⬆️ Bump pep8-naming from 0.12.0 to 0.12.1 (#45)
  Bumps [pep8-naming](https://github.com/PyCQA/pep8-naming) from 0.12.0 to 0.12.1.
  - [Release notes](https://github.com/PyCQA/pep8-naming/releases)
  - [Changelog](https://github.com/PyCQA/pep8-naming/blob/master/CHANGELOG.rst)
  - [Commits](https://github.com/PyCQA/pep8-naming/compare/0.12.0...0.12.1)

  ---
  updated-dependencies:
  - dependency-name: pep8-naming
    dependency-type: direct:development
    update-type: version-update:semver-patch
  ...
- ⬆️ Bump emoji from 1.2.0 to 1.4.2 (#44)
  Bumps [emoji](https://github.com/carpedm20/emoji) from 1.2.0 to 1.4.2.
  - [Release notes](https://github.com/carpedm20/emoji/releases)
  - [Changelog](https://github.com/carpedm20/emoji/blob/master/CHANGES.md)
  - [Commits](https://github.com/carpedm20/emoji/compare/v.1.2.0...v.1.4.2)

  ---
  updated-dependencies:
  - dependency-name: emoji
    dependency-type: direct:development
    update-type: version-update:semver-minor
  ...
- ⬆️ Bump isort from 5.9.1 to 5.9.3 (#43)
  Bumps [isort](https://github.com/pycqa/isort) from 5.9.1 to 5.9.3.
  - [Release notes](https://github.com/pycqa/isort/releases)
  - [Changelog](https://github.com/PyCQA/isort/blob/main/CHANGELOG.md)
  - [Commits](https://github.com/pycqa/isort/compare/5.9.1...5.9.3)

  ---
  updated-dependencies:
  - dependency-name: isort
    dependency-type: direct:development
    update-type: version-update:semver-patch
  ...
- ⬆️ Bump pep8-naming from 0.11.1 to 0.12.0 (#40)
  Bumps [pep8-naming](https://github.com/PyCQA/pep8-naming) from 0.11.1 to 0.12.0.
  - [Release notes](https://github.com/PyCQA/pep8-naming/releases)
  - [Changelog](https://github.com/PyCQA/pep8-naming/blob/master/CHANGELOG.rst)
  - [Commits](https://github.com/PyCQA/pep8-naming/compare/0.11.1...0.12.0)

  ---
  updated-dependencies:
  - dependency-name: pep8-naming
    dependency-type: direct:development
    update-type: version-update:semver-minor
  ...
- ⬆️ Bump flake8-eradicate from 1.0.0 to 1.1.0 (#39)
  Bumps [flake8-eradicate](https://github.com/wemake-services/flake8-eradicate) from 1.0.0 to 1.1.0.
  - [Release notes](https://github.com/wemake-services/flake8-eradicate/releases)
  - [Changelog](https://github.com/wemake-services/flake8-eradicate/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/wemake-services/flake8-eradicate/compare/1.0.0...1.1.0)
- ⬆️ Bump isort from 5.8.0 to 5.9.1 (#38)
  Bumps [isort](https://github.com/pycqa/isort) from 5.8.0 to 5.9.1.
  - [Release notes](https://github.com/pycqa/isort/releases)
  - [Changelog](https://github.com/PyCQA/isort/blob/main/CHANGELOG.md)
  - [Commits](https://github.com/pycqa/isort/compare/5.8.0...5.9.1)

  ---
  updated-dependencies:
  - dependency-name: isort
    dependency-type: direct:development
    update-type: version-update:semver-minor
  ...
- ⬆️ Bump ipdb from 0.13.8 to 0.13.9 (#37)
  Bumps [ipdb](https://github.com/gotcha/ipdb) from 0.13.8 to 0.13.9.
  - [Release notes](https://github.com/gotcha/ipdb/releases)
  - [Changelog](https://github.com/gotcha/ipdb/blob/master/HISTORY.txt)
  - [Commits](https://github.com/gotcha/ipdb/compare/0.13.8...0.13.9)

  ---
  updated-dependencies:
  - dependency-name: ipdb
    dependency-type: direct:development
    update-type: version-update:semver-patch
  ...
- ⬆️ Bump pytest-cov from 2.12.0 to 2.12.1 (#36)
  Bumps [pytest-cov](https://github.com/pytest-dev/pytest-cov) from 2.12.0 to 2.12.1.
  - [Release notes](https://github.com/pytest-dev/pytest-cov/releases)
  - [Changelog](https://github.com/pytest-dev/pytest-cov/blob/master/CHANGELOG.rst)
  - [Commits](https://github.com/pytest-dev/pytest-cov/compare/v2.12.0...v2.12.1)

  ---
  updated-dependencies:
  - dependency-name: pytest-cov
    dependency-type: direct:development
    update-type: version-update:semver-patch
  ...
- ⬆️ Bump requests-mock from 1.9.2 to 1.9.3 (#35)
  Bumps [requests-mock](https://github.com/jamielennox/requests-mock) from 1.9.2 to 1.9.3.
  - [Release notes](https://github.com/jamielennox/requests-mock/releases)
  - [Commits](https://github.com/jamielennox/requests-mock/compare/1.9.2...1.9.3)
- ⬆️ Bump ipdb from 0.13.7 to 0.13.8 (#34)
  Bumps [ipdb](https://github.com/gotcha/ipdb) from 0.13.7 to 0.13.8.
  - [Release notes](https://github.com/gotcha/ipdb/releases)
  - [Changelog](https://github.com/gotcha/ipdb/blob/master/HISTORY.txt)
  - [Commits](https://github.com/gotcha/ipdb/compare/0.13.7...0.13.8)
- ⬆️ Bump pytest-cov from 2.11.1 to 2.12.0 (#33)
  Bumps [pytest-cov](https://github.com/pytest-dev/pytest-cov) from 2.11.1 to 2.12.0.
  - [Release notes](https://github.com/pytest-dev/pytest-cov/releases)
  - [Changelog](https://github.com/pytest-dev/pytest-cov/blob/master/CHANGELOG.rst)
  - [Commits](https://github.com/pytest-dev/pytest-cov/compare/v2.11.1...v2.12.0)
- ⬆️ Bump pydantic from 1.8.1 to 1.8.2.
  Bumps [pydantic](https://github.com/samuelcolvin/pydantic) from 1.8.1 to 1.8.2.
  - [Release notes](https://github.com/samuelcolvin/pydantic/releases)
  - [Changelog](https://github.com/samuelcolvin/pydantic/blob/master/HISTORY.md)
  - [Commits](https://github.com/samuelcolvin/pydantic/compare/v1.8.1...v1.8.2)
- ⬆️ Bump flake8-comprehensions from 3.4.0 to 3.5.0 (#31)
  Bumps [flake8-comprehensions](https://github.com/adamchainz/flake8-comprehensions) from 3.4.0 to 3.5.0.
  - [Release notes](https://github.com/adamchainz/flake8-comprehensions/releases)
  - [Changelog](https://github.com/adamchainz/flake8-comprehensions/blob/main/HISTORY.rst)
  - [Commits](https://github.com/adamchainz/flake8-comprehensions/compare/3.4.0...3.5.0)
- ⬆️ Bump flake8 from 3.9.1 to 3.9.2 (#30)
  Bumps [flake8](https://gitlab.com/pycqa/flake8) from 3.9.1 to 3.9.2.
  - [Release notes](https://gitlab.com/pycqa/flake8/tags)
  - [Commits](https://gitlab.com/pycqa/flake8/compare/3.9.1...3.9.2)
- ⬆️ Bump pytest from 6.2.3 to 6.2.4 (#29)
  Bumps [pytest](https://github.com/pytest-dev/pytest) from 6.2.3 to 6.2.4.
  - [Release notes](https://github.com/pytest-dev/pytest/releases)
  - [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst)
  - [Commits](https://github.com/pytest-dev/pytest/compare/6.2.3...6.2.4)
- ⬆️ Bump requests-mock from 1.9.1 to 1.9.2 (#28)
  Bumps [requests-mock](https://github.com/jamielennox/requests-mock) from 1.9.1 to 1.9.2.
  - [Release notes](https://github.com/jamielennox/requests-mock/releases)
  - [Commits](https://github.com/jamielennox/requests-mock/compare/1.9.1...1.9.2)
- ⬆️ Bump requests-mock from 1.8.0 to 1.9.1 (#27)
  Bumps [requests-mock](https://github.com/jamielennox/requests-mock) from 1.8.0 to 1.9.1.
  - [Release notes](https://github.com/jamielennox/requests-mock/releases)
  - [Commits](https://github.com/jamielennox/requests-mock/compare/1.8.0...1.9.1)
- ⬆️ Bump requests-mock from 1.8.0 to 1.9.1 (#25)
  Bumps [requests-mock](https://github.com/jamielennox/requests-mock) from 1.8.0 to 1.9.1.
  - [Release notes](https://github.com/jamielennox/requests-mock/releases)
  - [Commits](https://github.com/jamielennox/requests-mock/compare/1.8.0...1.9.1)
- ⬆️ Bump flake8 from 3.9.0 to 3.9.1 (#24)
  Bumps [flake8](https://gitlab.com/pycqa/flake8) from 3.9.0 to 3.9.1.
  - [Release notes](https://gitlab.com/pycqa/flake8/tags)
  - [Commits](https://gitlab.com/pycqa/flake8/compare/3.9.0...3.9.1)
- ⬆️ Bump pytest from 6.2.2 to 6.2.3 (#22)
  Bumps [pytest](https://github.com/pytest-dev/pytest) from 6.2.2 to 6.2.3.
  - [Release notes](https://github.com/pytest-dev/pytest/releases)
  - [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst)
  - [Commits](https://github.com/pytest-dev/pytest/compare/6.2.2...6.2.3)
- ⬆️ Bump flake8-bugbear from 21.3.2 to 21.4.3 (#21)
  Bumps [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) from 21.3.2 to 21.4.3.
  - [Release notes](https://github.com/PyCQA/flake8-bugbear/releases)
  - [Commits](https://github.com/PyCQA/flake8-bugbear/compare/21.3.2...21.4.3)
- ⬆️:lock: Bump urllib3 from 1.26.3 to 1.26.4 (#23)
  Bumps [urllib3](https://github.com/urllib3/urllib3) from 1.26.3 to 1.26.4. **This update includes a security fix.**
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/1.26.3...1.26.4)
- ⬆️ Bump api-client from 1.3.0 to 1.3.1 (#20)
  Bumps [api-client](https://github.com/MikeWooster/api-client) from 1.3.0 to 1.3.1.
  - [Release notes](https://github.com/MikeWooster/api-client/releases)
  - [Commits](https://github.com/MikeWooster/api-client/compare/v1.3.0...v1.3.1)
- ⬆️ Bump isort from 5.7.0 to 5.8.0 (#19)
  Bumps [isort](https://github.com/pycqa/isort) from 5.7.0 to 5.8.0.
  - [Release notes](https://github.com/pycqa/isort/releases)
  - [Changelog](https://github.com/PyCQA/isort/blob/develop/CHANGELOG.md)
  - [Commits](https://github.com/pycqa/isort/compare/5.7.0...5.8.0)
- ⬆️:lock: Bump urllib3 from 1.26.2 to 1.26.3 (#18)
  Bumps [urllib3](https://github.com/urllib3/urllib3) from 1.26.2 to 1.26.3. **This update includes a security fix.**
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/1.26.2...1.26.3)
- ⬆️ Bump flake8-comprehensions from 3.3.1 to 3.4.0 (#17)
  Bumps [flake8-comprehensions](https://github.com/adamchainz/flake8-comprehensions) from 3.3.1 to 3.4.0.
  - [Release notes](https://github.com/adamchainz/flake8-comprehensions/releases)
  - [Changelog](https://github.com/adamchainz/flake8-comprehensions/blob/main/HISTORY.rst)
  - [Commits](https://github.com/adamchainz/flake8-comprehensions/compare/3.3.1...3.4.0)
- ⬆️ Bump yapf from 0.30.0 to 0.31.0 (#15)
  Bumps [yapf](https://github.com/google/yapf) from 0.30.0 to 0.31.0.
  - [Release notes](https://github.com/google/yapf/releases)
  - [Changelog](https://github.com/google/yapf/blob/main/CHANGELOG)
  - [Commits](https://github.com/google/yapf/compare/v0.30.0...v0.31.0)
- ⬆️ Bump ipdb from 0.13.6 to 0.13.7 (#16)
  Bumps [ipdb](https://github.com/gotcha/ipdb) from 0.13.6 to 0.13.7.
  - [Release notes](https://github.com/gotcha/ipdb/releases)
  - [Changelog](https://github.com/gotcha/ipdb/blob/master/HISTORY.txt)
  - [Commits](https://github.com/gotcha/ipdb/compare/0.13.6...0.13.7)
- ⬆️ Bump flake8 from 3.8.4 to 3.9.0 (#14)
  Bumps [flake8](https://gitlab.com/pycqa/flake8) from 3.8.4 to 3.9.0.
  - [Release notes](https://gitlab.com/pycqa/flake8/tags)
  - [Commits](https://gitlab.com/pycqa/flake8/compare/3.8.4...3.9.0)
- ⬆️ Bump flake8-bugbear from 21.3.1 to 21.3.2 (#12)
  Bumps [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) from 21.3.1 to 21.3.2.
  - [Release notes](https://github.com/PyCQA/flake8-bugbear/releases)
  - [Commits](https://github.com/PyCQA/flake8-bugbear/commits)
- ⬆️ Bump ipdb from 0.13.4 to 0.13.6.
  Bumps [ipdb](https://github.com/gotcha/ipdb) from 0.13.4 to 0.13.6.
  - [Release notes](https://github.com/gotcha/ipdb/releases)
  - [Changelog](https://github.com/gotcha/ipdb/blob/master/HISTORY.txt)
  - [Commits](https://github.com/gotcha/ipdb/compare/0.13.4...0.13.6)
- ⬆️ Bump pydantic from 1.7.3 to 1.8.1.
  Bumps [pydantic](https://github.com/samuelcolvin/pydantic) from 1.7.3 to 1.8.1.
  - [Release notes](https://github.com/samuelcolvin/pydantic/releases)
  - [Changelog](https://github.com/samuelcolvin/pydantic/blob/master/HISTORY.md)
  - [Commits](https://github.com/samuelcolvin/pydantic/compare/v1.7.3...v1.8.1)
- ⬆️ Bump flake8-bugbear from 20.11.1 to 21.3.1.
  Bumps [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) from 20.11.1 to 21.3.1.
  - [Release notes](https://github.com/PyCQA/flake8-bugbear/releases)
  - [Commits](https://github.com/PyCQA/flake8-bugbear/commits)
- ⬆️ Bump api-client from 1.2.2 to 1.3.0.
  Bumps [api-client](https://github.com/MikeWooster/api-client) from 1.2.2 to 1.3.0.
  - [Release notes](https://github.com/MikeWooster/api-client/releases)
  - [Commits](https://github.com/MikeWooster/api-client/compare/v1.2.2...v1.3.0)
- ⬆️ Bump emoji from 1.1.0 to 1.2.0.
  Bumps [emoji](https://github.com/carpedm20/emoji) from 1.1.0 to 1.2.0.
  - [Release notes](https://github.com/carpedm20/emoji/releases)
  - [Changelog](https://github.com/carpedm20/emoji/blob/master/CHANGES.md)
  - [Commits](https://github.com/carpedm20/emoji/compare/v.1.1.0...v.1.2.0)
- ⬆️ Bump pytest from 6.2.1 to 6.2.2.
  Bumps [pytest](https://github.com/pytest-dev/pytest) from 6.2.1 to 6.2.2.
  - [Release notes](https://github.com/pytest-dev/pytest/releases)
  - [Changelog](https://github.com/pytest-dev/pytest/blob/master/CHANGELOG.rst)
  - [Commits](https://github.com/pytest-dev/pytest/compare/6.2.1...6.2.2)
- ⬆️ Bump emoji from 0.6.0 to 1.1.0.
  Bumps [emoji](https://github.com/carpedm20/emoji) from 0.6.0 to 1.1.0.
  - [Release notes](https://github.com/carpedm20/emoji/releases)
  - [Changelog](https://github.com/carpedm20/emoji/blob/master/CHANGES.md)
  - [Commits](https://github.com/carpedm20/emoji/commits/v.1.1.0)

##### 🌱 Other

- Release 1.1.0.
- Upgrade to GitHub-native Dependabot (#26)


#### api-client-pydantic `v1.0.2` (2021-01-21)

##### ♻️ Changes

- Refactoring use args and kwargs.

##### ⬆️ Dependencies

- ⬆️ Bump pytest-cov from 2.11.0 to 2.11.1.
  Bumps [pytest-cov](https://github.com/pytest-dev/pytest-cov) from 2.11.0 to 2.11.1.
  - [Release notes](https://github.com/pytest-dev/pytest-cov/releases)
  - [Changelog](https://github.com/pytest-dev/pytest-cov/blob/master/CHANGELOG.rst)
  - [Commits](https://github.com/pytest-dev/pytest-cov/compare/v2.11.0...v2.11.1)
- ⬆️ Bump pytest-cov from 2.10.1 to 2.11.0.
  Bumps [pytest-cov](https://github.com/pytest-dev/pytest-cov) from 2.10.1 to 2.11.0.
  - [Release notes](https://github.com/pytest-dev/pytest-cov/releases)
  - [Changelog](https://github.com/pytest-dev/pytest-cov/blob/master/CHANGELOG.rst)
  - [Commits](https://github.com/pytest-dev/pytest-cov/compare/v2.10.1...v2.11.0)

##### 🌱 Other

- Bumping version from 1.0.0 to 1.0.1.


#### api-client-pydantic `v1.0.0` (2021-01-17)

##### ♻️ Changes

- Publish job.

##### 🌱 Other

- Bumping version from 0.1.0 to 1.0.0.
- Move api_client_pydantic to apiclient_pydantic.
  now import `from apiclient_pydantic import *`


#### api-client-pydantic `v0.1.1` (2021-01-16)

##### ♻️ Changes

- Auto generate changelog.
- Fix Changelog template.

##### 📝 Docs

- Update README.md.
- Prepare for generate CHANGELOG.md.


#### api-client-pydantic `v0.1.0` (2021-01-15)

##### New ✨

- Basic functionality.

##### ♻️ Changes

- Configs.

##### ⬆️ Dependencies

- ➕ dependencies and pyproject.

##### 📝 Documentation

- Common files.
- Init readme.

##### 🌱 Other

- CI Actions.
- Add tests.
- Initial commit.
