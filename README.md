# METAvivor Classy Tools

While working on the implementation of Classy for [METAvivor](https://www.metavivor.org), we needed a way to do bulk uploads of offline check transations. This code provides a command line interface for working with the [Classy API](https://developers.classy.org/api-docs/v2/index.html) to handle those bulk uploads.

## Installation

```sh
pipenv install
```

## Environment variables

This repo uses `pipenv`, which automatically loads up environment variables present in a `.env` file. Make a copy of `.env.template` and edit the values.

See Classy's documentation on [Requesting Access](https://developers.classy.org/overview/request-access) for information on obtaining the client ID and client secret.

- `CLASSY_CLIENT_ID` - OAuth2 client ID
- `CLASSY_CLIENT_SECRET` - OAuth2 client secret
- `CLASSY_ORG_ID` - your organization's ID. You can get this by signing into the Classy admin and copying it from the URL.
- `CLASSY_DEFAULT_CAMPAIGN_ID` - the default campaign ID to upload transactions to. You can get this by signing into the Classy admin and copying it or by setting `CLASSY_OR_ID` and running the `list-campaigns` command.

## Using the CLI

Get a list of campaigns for an organization:

```sh
pipenv run python classy.py list-campaigns
```

Get a list of teams for an campaign:

```sh
pipenv run python classy.py list-teams CAMPAIGN_ID
```

Get a list of pages for an campaign:

```sh
pipenv run python classy.py list-pages CAMPAIGN_ID
```

Upload offline transactions from a CSV file:

```sh
pipenv run python classy.py upload-transactions FILE_PATH
```

Print help information:

```sh
pipenv run python classy.py --help
```

## About uploading transactions

The input for transactions should be a CSV file. The mapping from METAvivor's data to Classy's API can be found in [prepare.py](prepare.py). An example input file can be found in the `tests` folder.
