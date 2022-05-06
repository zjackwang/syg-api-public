from tests_private_api.test_client import run_local_api_tests, run_remote_api_tests


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("loc", type=str, help="local or remote")
    args = parser.parse_args()

    if args.loc == "local":
        run_local_api_tests()
    else:
        run_remote_api_tests()
