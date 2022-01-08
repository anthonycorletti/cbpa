# cbpa

Coinbase Pro Automation for making buy orders from a default bank account.

## Quickstart

1. Install with pip

    ```sh
    pip install cbpa
    ```

1. [Create a Coinbase API Key](https://help.coinbase.com/en/pro/other-topics/api/how-do-i-create-an-api-key-for-coinbase-pro), you will need to select all fields of access.

1. (Optional). [Create a Discord webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks).

1. Make your config file. See the [examples](./examples) for more.

    ```yaml
    ---
    api:
        key: "myKey"
        secret: "mySecret"
        passphrase: "myPassphrase"
        url: "https://api.pro.coinbase.com"
    discord:
        webhook: https://discord.com/api/webhooks/123/abc
    account:
        auto_funding_limit: 20
        fiat_currency: USD
    buys:
        - send_currency: USD
            send_amount: 2
            receive_currency: BTC
        - send_currency: USD
            send_amount: 2
            receive_currency: ETH
        - send_currency: USD
            send_amount: 2
            receive_currency: DOGE
    ```

1. Make your orders!

    ```sh
    cbpa run -f my-buys.yaml
    ```

## Running `cbpa` in Google Cloud Run

You can run `cbpa` as a server in Google Cloud Run, which can called by Google Cloud Scheduler to automatically place buys for you each day, or on any cron schedule you like.

These steps assume you have installed and configured `gcloud` already.

1. Store your buy order file as a secret in GCP.

    ```sh
    gcloud secrets versions add my_buys --data-file=my-buys.yaml
    ```

1. Build and push your docker container to Google Cloud, and then deploy your container.

    ```sh
    ./scripts/docker-build.sh && ./scripts/docker-push.sh; SECRET_ID=my_buys ./scripts/gcloud-run-deploy.sh
    ```

1. [Create an authenticated scheduler](https://cloud.google.com/scheduler/docs/http-target-auth#using-the-console) that uses an http target to hit the `buy` endpoint.
