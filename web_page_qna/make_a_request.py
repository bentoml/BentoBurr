if __name__ == "__main__":
    import argparse

    import bentoml

    parser = argparse.ArgumentParser()
    parser.add_argument("--service_url", type=str, default="http://localhost:3000")
    parser.add_argument("--web_page_url", type=str, required=True)
    parser.add_argument("--query", type=str, default="what's the title of the page?")
    args = parser.parse_args()

    client = bentoml.SyncHTTPClient(args.service_url)
    response = client.run(
        web_page_url=args.web_page_url,
        query=args.query,
    )
    print(response)