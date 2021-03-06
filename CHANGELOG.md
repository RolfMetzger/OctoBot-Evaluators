# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.3] - 2020-04-04
### Updated
- Exception logger API from Commons

### Fixed
- Travis CI file

## [1.4.2] - 2020-02-17
### Added
- Stop method to AbstractEvaluator

### Updated
- Evaluator, initialization, matrix APIs
- Matrix channel logger

## [1.4.1] - 2020-01-18
### Updated
- Use exchange_id in exchange channels

## [1.4.0] - 2020-01-14
### Added
- Matrices class to storage matrix instances

### Updated
**Requirements**
- Commons version to 1.2.2
- Channels version to 1.3.19
- Tentacles Manager version to 1.0.13

## [1.3.3] - 2020-01-12
### Added
- get_evaluator_classes_from_type API method

### Updated
- Typing for API methods
- Social evaluator intialization

## [1.3.2] - 2020-01-07
### Added
- Cryptocurrency related evaluator

## [1.3.1] - 2019-12-21
### Updated
**Requirements**
- Commons version to 1.2.0
- Channels version to 1.3.17

## [1.3.0] - 2019-12-14
### Changed
- EvaluatorMatrix to EventTree implementation (from Commons)

### Updated
**Requirements**
- Commons version to 1.1.51
- Channels version to 1.3.16

## [1.2.6] - 2019-11-09
### Updated
**Requirements**
- Cython version to 0.29.14
- Commons version to 1.1.49
- Channels version to 1.3.15

## [1.2.5] - 2019-10-30
### Changed
- OSX support

## [1.2.4] - 2019-10-11
### Changed
- Style improvements

## [1.2.3] - 2019-10-09
### Added
- PyPi manylinux deployment

## [1.2.2] - 2019-10-08
### Changed
- Setup install

## [1.2.1] - 2019-10-07
### Changed
- Improved matrix channel cancelling management

## [1.2.0] - 2019-10-05
### Added
- Evaluator types management
- Initialization API

## Moved
- config_manager to commons

### Fixed
- Channels package compatibility
- Commons package compatibility

## [1.1.0] - 2019-09-01
### Changed
- Improved API initialization
- Improved matrix management

### Fixed
- Channel package compatibility

## [1.0.0] - 2019-08-14
### Added
- Evaluator classes migrations from OctoBot project
- Matrix class that manage global evaluation dictionary
- Matrix channel, producer and consumer
- First API methods
