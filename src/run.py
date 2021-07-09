import requests
import json
import sys
import os
import csv
import logging


CONFORMITY_REGIONS = [
    "eu-west-1",
    "ap-southeast-2",
    "us-west-2",
]


logging.getLogger("urllib3").setLevel(logging.WARNING)
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logigng_format = "%(levelname)s: %(message)s"
logging.basicConfig(format=logigng_format, level=LOG_LEVEL)


class ConformityReports:
    def __init__(self):
        try:
            print("Obtaining required environment variables...")
            self.CONFORMITY_REGION = os.environ["CONFORMITY_REGION"].lower()

            if self.CONFORMITY_REGION not in CONFORMITY_REGIONS:
                sys.exit(
                    'Error: Please ensure "CONFORMITY_REGIONS" is set to a region which is supported by Cloud Conformity'
                )

            self.api_key = os.environ["CONFORMITY_API_KEY"]

            self.headers = {
                "Content-Type": "application/vnd.api+json",
                "Authorization": "ApiKey " + self.api_key,
            }

        except KeyError:
            sys.exit("Error: Please ensure all environment variables are set")

    def _get_report_entries(self):
        cfn_scan_endpoint = (
            f"https://{self.CONFORMITY_REGION}-api.cloudconformity.com/v1/reports/"
        )

        resp = requests.get(cfn_scan_endpoint, headers=self.headers)
        report_entries = json.loads(resp.text)
        msg = report_entries.get("Message")

        if msg and "explicit deny" in msg:
            print(
                f"Error: {msg}\nPlease ensure your API credentials are correct, and that you've set the correct "
                f"region"
            )
            sys.exit(1)

        return report_entries

    @staticmethod
    def _get_latest_report_only(reports):
        logging.info('Obtaining details on only the latest reports.')
        latest_report_name = set()
        all_reports = []

        for report in reports["data"]:
            report_title = report["attributes"]["title"]

            if report_title in latest_report_name:
                logging.debug(f'Seen report "{report_title}" before. Skipping it.')

            else:
                logging.debug(f'Have not seen report "{report_title}" before. Adding it it.')
                all_reports.append(report)
                latest_report_name.add(report_title)

        latest_reports = {'data': all_reports}

        return latest_reports

    def get_report_entries(self, latest_only: bool = True) -> dict:
        all_report_entries = self._get_report_entries()

        if latest_only:
            latest_report_entries = self._get_latest_report_only(all_report_entries)

            return latest_report_entries

        else:
            return all_report_entries

    def download_reports(self, report_format: str = "csv") -> dict:
        report_entries = self.get_report_entries()

        reports = {}

        get_all_reports = report_entries["data"]

        for report in get_all_reports:
            report_id = report["id"]
            report_title = report["attributes"]["title"]
            entity_id = report["attributes"]["entity-id"]
            report_url = f"https://{self.CONFORMITY_REGION}-api.cloudconformity.com/v1/reports/{report_id}/{entity_id}/{report_format}/"

            logging.info(f'Downloading report "{report_title}". This may take a few seconds.')

            report_data = requests.get(report_url, headers=self.headers).text.split('\n')
            formatted_report_data = self._format_report_entry(report_title, report_data)
            reports[report_title] = formatted_report_data
            logging.debug(f'Finished processing "{report_title}".')

        return reports

    @staticmethod
    def _format_report_entry(report_title, report_data) -> list:
        logging.debug(f'Formatting log data for report "{report_title}".')
        formatted_entries = []

        get_csv_report_data = csv.reader(report_data, delimiter=',')
        csv_report_data = list(get_csv_report_data)
        report_headers = csv_report_data.pop(0)

        for report_entry in csv_report_data:
            if len(report_entry) < len(report_headers):
                logging.debug(f'Skipping report entry: {report_entry}')
                continue

            formatted_entry = dict(zip(report_headers, report_entry))
            formatted_entries.append(formatted_entry)

        return formatted_entries


def main():
    cr = ConformityReports()
    reports = cr.download_reports()


if __name__ == "__main__":
    main()
