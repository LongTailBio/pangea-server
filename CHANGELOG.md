# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/LongTailBio/metagenscope-server/compare/v0.10.0...HEAD
[0.10.0]: https://github.com/LongTailBio/metagenscope-server/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/LongTailBio/metagenscope-server/compare/v0.0.1...v0.9.0
