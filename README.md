# Pangea Server

Pangea is a system to improve bioinformatics pipelines. Key features include:

- Organize projects, samples, and the results of analyses
- Automatically Sync results with S3 cloud storage
- Coordinate pipelines running across multiple sites

Pangea server is currently in alpha and being heavily developed.

## Getting Started

This readme documents how to run and test the Pangea server as a standalone application. Pangea server is based on the earlier MetaGenScope server `metagenscope-server` was a part of [`metagenscope-main`](https://github.com/longtailbio/metagenscope-main) and was usually be run as part of the complete stack.

### Prerequisites

You will also need to have PostgreSQL running locally with the following databases:

```sql
CREATE DATABASE metagenscope_prod;
CREATE DATABASE metagenscope_dev;
CREATE DATABASE metagenscope_test;
```

And plugins:

```sql
\c metagenscope_prod;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
\c metagenscope_dev;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
\c metagenscope_test;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

All local interactions with the server (developing, running, testing) should be done in a virtual environment:

```sh
$ python3.6 -m venv env  # Create the environment (only need be performed once)
$ source env/bin/activate  # Activate the environment
```

Set application configuration:

```sh
# Environment: development | testing | staging | production
$ export APP_SETTINGS=development
$ export SECRET_KEY=my_precious
$ export DATABASE_URL=postgres://username:password@localhost:5432/metagenscope_dev
$ export DATABASE_TEST_URL=postgres://username:password@localhost:5432/metagenscope_test
```

### Running Locally

Spin up server (runs on `http://127.0.0.1:5000/`):

```sh
$ python manage.py runserver
```

A startup script is provided to ensure that the application does not attempt to start before all service dependencis are accepting connections. It can be used like so:

```
$ ./startup.sh [host:port[, host:port, ...]] -- [command]
```

An example of waiting for Postgres and Mongo DBs running on localhost before starting the application would look like this:

```
$ ./startup.sh localhost:5435 localhost:27020 -- python manage.py runserver
```

## Testing

The entry point to test suite tools is the `Makefile`.

### Linting

Code quality is enforced using pylint, pycodestyle, and pydocstyle. The rules are defined in `.pylintrc`.

These tools may be run together using:

```sh
$ make lint
```

### Running Test Suite

To run the test suite (will execute `lint` prior to running tests):

```sh
$ make test
```

You may also run tests checking their coverage:

```sh
$ make cov
```

## Development

MetaGenScope uses the GitFlow branching strategy along with Pull Requests for code reviews. Check out [this post](https://devblog.dwarvesf.com/post/git-best-practices/) by the Dwarves Foundation for more information.

### API Documentation

The API for `metagenscope-server` is documented in [`swagger.yml`](swagger.yml) in the OpenAPI v3.0 spec.

**Viewing**

Swagger UI can be used to view an API spec URL. You can use the [public demo](https://petstore.swagger.io), or run it locally:

```sh
docker run -p 80:8080 -e API_URL=https://raw.githubusercontent.com/longtailbio/metagenscope-server/master/swagger.yml swaggerapi/swagger-ui:v3.19.5
```

**Editing**

Copying and pasting between your local editor and the [`Swagger Editor`](https://editor.swagger.io) seems to be the easiest way to edit.

## Continuous Integration

The test suite is run automatically on CircleCI for each push to Github. You can skip this behavior for a commit by appending `[skip ci]` to the commit message.

### Custom Docker Database Images

CircleCI does not allow running commands on secondary containers (eg. the database). To get around this, we use custom images for our database images. Changes to either image need to be built, tagged, and pushed to Docker Hub before CI can succeed.

- **Postgres** - Stock Postgres image with the `uuid-ossp` extension enabled. Located at `./database_docker/postgres_db`.
- **Mongo** - Stock Mongo image with a healthcheck script added. Located at `./database_docker/mongo_db`.

**Steps**

From the appropriate database docker subdirectory, build and tag the image:

```sh
$ export COMMIT_SHA=`git rev-parse HEAD`
$ docker build -t imagebuildinprocess .
$ docker tag imagebuildinprocess "metagenscope/postgres:${COMMIT_SHA::8}"
```

Push the image:

```sh
$ docker login
$ docker push "metagenscope/postgres:${COMMIT_SHA::8}"
```

Clean up:

```sh
$ docker rmi imagebuildinprocess "metagenscope/postgres:${COMMIT_SHA::8}"
```

## Contributing

Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository][project-tags].

## Release History

See [`CHANGELOG.md`](CHANGELOG.md).

## Authors

- **Benjamin Chrobot** - _Initial work_ - [bchrobot](https://github.com/bchrobot)

See also the list of [contributors][contributors] who participated in this project.

## License

This project is licensed under the MIT License - see the [`LICENSE.md`](LICENSE.md) file for details.

[project-tags]: https://github.com/longtailbio/metagenscope-server/tags
[contributors]: https://github.com/longtailbio/metagenscope-server/contributors
