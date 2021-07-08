# Conformity Reports

Downloads Conformity reports and puts them into a dictionary. The data from the reports can then be passed into other reports and tools.

## Configuration

Specify the following environment variables:
* `CONFORMITY_API_KEY`
* `CONFORMITY_REGION`

## Example Output

Getting a list of reports:

```
pprint(list(reports.keys()))
['PCI Report',
 'ISO',
 'Well Architected Framework',
 'Cost Remediation',
 'Cost Optimization',
 'EC2-Issues',
 'SOC-2  Report',
 'NIST 800 - All Accounts',
 'AWS Well Arcitected Framework',
 'Compliance Based Reports',
 'Conformity General Report',
 'SOC  2 report',
 'CIS Framework V1.2.0',
 'Open Banking AWS Audit']
```

Checking how many results are in the `PCI Report` report:

```
len(reports['PCI Report'])
104437
```

Getting the first two results from the `PCI Report` report:

```
pprint(reports['PCI Report'][0:2])
[{'Account Name': 'TestAwsAccount',
  'Categories': 'security',
  'Check Status': 'FAILURE',
  'Cloud Provider': 'aws',
  'Cloud Provider Identifier': '123456789012',
  'Environment': 'Demo',
  'Failure Discovery Date': '2020-07-30T05:47:24.533Z',
  'Failure Resolved Date': '',
  'Last Updated Date': '',
  'Message': 'Account password policy does not enforce password expiration',
  'Provider Resource ID': '',
  'Region': 'global',
  'Resolution Page': 'https://www.cloudconformity.com/knowledge-base/aws/IAM/password-policy.html#A_pjRohp3',
  'Resource': 'PasswordPolicy',
  'Risk Level': 'Medium',
  'Rule ID': 'IAM-011',
  'Rule Release Date': '2017-01-01',
  'Rule Title': 'Password Policy Expiration',
  'Rule Update Date': '2018-09-27',
  'Service': 'IAM',
  'Tags': ''},
 {'Account Name': 'TestAwsAccount',
  'Categories': 'security',
  'Check Status': 'FAILURE',
  'Cloud Provider': 'aws',
  'Cloud Provider Identifier': '123456789012',
  'Environment': 'Demo',
  'Failure Discovery Date': '2020-07-30T05:47:24.533Z',
  'Failure Resolved Date': '',
  'Last Updated Date': '',
  'Message': 'Account password policy does not prevent reuse of historical '
             'passwords',
  'Provider Resource ID': '',
  'Region': 'global',
  'Resolution Page': 'https://www.cloudconformity.com/knowledge-base/aws/IAM/password-policy.html#A_pjRohp3',
  'Resource': 'PasswordPolicy',
  'Risk Level': 'Medium',
  'Rule ID': 'IAM-012',
  'Rule Release Date': '2017-01-01',
  'Rule Title': 'Password Policy Reuse Prevention',
  'Rule Update Date': '2018-09-27',
  'Service': 'IAM',
  'Tags': ''}]
  ```

## Roadmap

* Add success/fail filtering. This will enable users to choose whether they get only successul checks, failed checks or both.
* Add risk level filtering. This will enable users to get results which are equal to or greater than their specified level. 


# Contact

* Blog: oznetnerd.com
* Email: will@oznetnerd.com