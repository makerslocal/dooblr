v3.0.0 (release date: 2017-11-01)
---------------------------------

- `7fcd758 <http://github.com/makerslocal/dooblr/commit/7fcd7586cff04978dd0a5d3a944707c8cdeeca76>`_ - Refactor dooblr to be more pluggable. This will require slight config changes.

v2.1.0 (release date: 2016-11-01)
---------------------------------

- `32f1709 <http://github.com/makerslocal/dooblr/commit/32f1709812e7e32d12a544333b4eb23e7dc90c3f>`_ - Merge pull request #32 from makerslocal/add-dryrun
- `04cf381 <http://github.com/makerslocal/dooblr/commit/04cf3812b19ea9b0e73a8a5fa4f227d21688ec98>`_ - Merge pull request #33 from makerslocal/fix-opt-tags
- `fa0fb00 <http://github.com/makerslocal/dooblr/commit/fa0fb003e8fd8da4fb3fcb8c837d3618198a71c3>`_ - Merge pull request #34 from makerslocal/remove-print

v2.0.0 (release date: 2016-08-20)
---------------------------------

- `5fd5fd1 <http://github.com/makerslocal/dooblr/commit/5fd5fd17fc790923c8a87fb5cf8f635463613159>`_ - Merge remote-tracking branch 'origin/on_subscribe' into yaml_configs
- `9bffd03 <http://github.com/makerslocal/dooblr/commit/9bffd036e4f7ed09623f72d6931361f0ce5b06cb>`_ - Merge pull request #19 from makerslocal/yaml_configs
- `e018160 <http://github.com/makerslocal/dooblr/commit/e018160b22cb7c5b4ed451d1a8674ca47a487561>`_ - Merge pull request #20 from makerslocal/flake8
- `2e6977b <http://github.com/makerslocal/dooblr/commit/2e6977b2bb5161f1b008d8b8700f95acc2dd4269>`_ - Merge pull request #21 from makerslocal/add-license
- `df8c1d1 <http://github.com/makerslocal/dooblr/commit/df8c1d18107f30a5508f8bbedd5ed9a8b42a4743>`_ - Merge pull request #22 from makerslocal/Fix_Empty_Tags
- `3e225b6 <http://github.com/makerslocal/dooblr/commit/3e225b6a5b9796cb6dadbea25300b358b0918a9a>`_ - Merge pull request #23 from makerslocal/readme-improvements
- `6c73cbc <http://github.com/makerslocal/dooblr/commit/6c73cbc543a68b8112f9c6eb748d8a44ee100ee0>`_ - Merge pull request #27 from makerslocal/auto-config
- `bb927c1 <http://github.com/makerslocal/dooblr/commit/bb927c1724b837db5fd25484f5f2e514877a5bfe>`_ - Merge pull request #28 from makerslocal/optional-tags

v1.0.0 (release date: 2016-08-20)
---------------------------------

- `f66f533 <http://github.com/makerslocal/dooblr/commit/f66f5334f6635f5e5b5be6da1444343b76ea7db9>`_ - Convert README to RST.
- `e6a4eb4 <http://github.com/makerslocal/dooblr/commit/e6a4eb4dde2e660e21b84710c0e48ad8994608cc>`_ - Update Dockerfile to use new dooblr install.
- `f96748b <http://github.com/makerslocal/dooblr/commit/f96748b1940d7d6bd6a035d448d17b3680bde6a9>`_ - Merge pull request #10 from makerslocal/pypi-prep
- `0f10dac <http://github.com/makerslocal/dooblr/commit/0f10dacce6d07dac6238b0b6654b6d0a80434e8e>`_ - Merge pull request #11 from makerslocal/fix-topic-match


v0.0.1 (release date: 2016-08-20)
---------------------------------
- `295a21e <http://github.com/makerslocal/dooblr/commit/295a21e3ceeda8194ccf3975abc85449931457fc>`_ - Implement config-parser and tests
- `13230d3 <http://github.com/makerslocal/dooblr/commit/13230d3344d9aadeb17d38f2686ba7a65bd816eb>`_ - Merge pull request #1 from makerslocal/get-travisci-working
- `b72b492 <http://github.com/makerslocal/dooblr/commit/b72b4921549a8a60a5155dd77a860c76dc8446c5>`_ - Merge pull request #2 from makerslocal/add-logo
- `fecd652 <http://github.com/makerslocal/dooblr/commit/fecd65242fde9fd943fafae0592a448fc6810491>`_ - Merge pull request #3 from makerslocal/fix-logo
- `d81d1f2 <http://github.com/makerslocal/dooblr/commit/d81d1f254d270cda561087ab752353329e1f4362>`_ - Support Python3
- `9443736 <http://github.com/makerslocal/dooblr/commit/94437366be01dcf232aaec0ec1ce6a595be9f0a9>`_ - Merge pull request #4 from makerslocal/py2-and-py3
- `83475f5 <http://github.com/makerslocal/dooblr/commit/83475f5d255ae21d9dc75c27ea8351166c371c1a>`_ - Merge pull request #5 from makerslocal/handle-mqtt
- `1627023 <http://github.com/makerslocal/dooblr/commit/162702319a36c8d6c7011e345cecfad2cea5a398>`_ - Merge pull request #6 from makerslocal/main-config
- `445a91a <http://github.com/makerslocal/dooblr/commit/445a91adec605faf5ff847f8975bc3d24ef315dc>`_ - Merge pull request #7 from makerslocal/dos2unix
- `77e6a05 <http://github.com/makerslocal/dooblr/commit/77e6a0586ea1f1ee6945e17682046a704e979dbc>`_ - Merge pull request #8 from makerslocal/add-influxdb
- `25912cb <http://github.com/makerslocal/dooblr/commit/25912cbc8930bc5ee2f9d74626f023ea1f75635d>`_ - Add Dockerfile


..
  Change log based off this one-liner
  git log $(git tag -l | sort -rn | head -n 1).. --pretty=format:'[%h](http://github.com/makerslocal/dooblr/commit/%H) - %s' --reverse | grep "#changelog"
