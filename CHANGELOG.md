# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Fixed
- Fix HMP single-sample processor.
- Return from sample task body if sample is missing dependencies.

## [0.11.5] - 2019-01-15
### Changed
- Print more complete information for erros in `Sample.fetch_safe()` method.

## [0.11.1] - 2018-11-01
### Fixed
- Run `test_app` CI job for tags so that downstream deploy job can run.

## [0.11.0] - 2018-11-01
### Added
- Docker image tags for commits on develop and `major`, `major.minor`, and `major.minor.patch` semver tags.

### Changed
- Use PyTest for testing.
- Moved analysis result and tool results to top level packages.
- Use `library_uuid` in place of `sample_group_uuid` for Sample creation.

### Fixed
- Middleware endpoint timeout by moving all middleware heavy lifting into task body.
- Fixed how Flask context is passed to Celery task bodies.
- Handle empty abundance/prevalence values gracefully.

## [0.10.0] - 2018-10-06
### Added
- Endpoint to delete sample groups.
- Multi-Axis and Top Taxa fuzz values.

## [0.9.0] - 2018-05-11
### Added
- Basic Docker configuration.
- PostgreSQL Docker and SQLAlchemy configuration.
- Readme documentation about linting.
- Basic test suite and commands.
- 'clean' task to Makefile.
- Production release process and instructions.
- Code coverage for testing.
- Password to users.
- Authentication endpoints and tests.
- CircleCI configuration.

### Fixed
- Updated Celery to 4.2.1 to fix module name change on kombu ([source](https://stackoverflow.com/a/50464774)).

### Changed
- Moved API to blueprint.

## 0.0.1 - 2017-11-13
### Added
- Basic Flask project structure.

[Unreleased]: https://github.com/LongTailBio/metagenscope-server/compare/v0.11.5...develop
[0.11.5]: https://github.com/LongTailBio/metagenscope-server/compare/v0.11.1...v0.11.5
[0.11.1]: https://github.com/LongTailBio/metagenscope-server/compare/v0.11.0...v0.11.1
[0.11.0]: https://github.com/LongTailBio/metagenscope-server/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/LongTailBio/metagenscope-server/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/LongTailBio/metagenscope-server/compare/v0.0.1...v0.9.0
