# METAvivor Classy Tools

While working on the implementation of Classy for [METAvivor](https://www.metavivor.org), we needed a way to do bulk uploads of offline check transations. This code provides a command line interface (CLI) for working with the [Classy API](https://developers.classy.org/api-docs/v2/index.html) to handle those bulk uploads.

## Prerequisites

This project uses [pipenv](https://pipenv.pypa.io/) to mange the Python virtual environment, dependencies, and running the CLI.

## Install dependencies

```sh
pipenv install
```

## Environment variables

This repo uses `pipenv`, which automatically loads up environment variables present in a `.env` file. Make a copy of `.env.template` and edit the values.

See Classy's documentation on [Requesting Access](https://developers.classy.org/overview/request-access) for information on obtaining the client ID and client secret.

- `CLASSY_CLIENT_ID` - OAuth2 client ID
- `CLASSY_CLIENT_SECRET` - OAuth2 client secret
- `CLASSY_ORG_ID` - your organization's ID. You can get this by signing into the Classy admin and copying it from the URL.
- `CLASSY_DEFAULT_CAMPAIGN_ID` - the default campaign ID to upload transactions to. You can get this by signing into the Classy admin and copying it or by setting `CLASSY_ORG_ID` and running the `list-campaigns` command.

## Transactions template

The included [transactions-template.csv](transactions-template.csv) can be used as a guide to see which fields are available and will be processed by the script. The mapping for how the data is formatted is in [prepare.py](prepare.py).

## Input and output

The CLI will read files from a folder named `input`. Place any CSVs you wish to use for batch uploading transactions in this folder.

The CLI will generate JSON reports and store them in a folder named `output`. You can inspect these reports, which will contain the payload to be sent (dry run) or the response data returned from the Classy API (actual run), formatted to contain one entry per transaction ID.

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

## API notes

Classy's [transaction API docs](https://developers.classy.org/api-docs/v2/index.html#transaction-transaction-post) don't have complete informaiton related to offline payments. They show only six available `offline_payment_info.payment_type`s, but there are more:

* cash
* check
* corporate_match
* cc
* crypto
* eft
* pledge
* sponsor
* stock_donations
* other

All `offline_payment_info` objects follow this format, **except** for check donations:

```json
{
    "offline_payment_info": {
        "description": "offline payment description",
        "payment_type": "eft",
        "sync_third_party": false
    }
}
```

Check donations also include a `check_number`:

```json
{
    "offline_payment_info": {
        "description": "offline payment description",
        "payment_type": "check",
        "check_number": 123456,
        "sync_third_party": false
    }
}
```

