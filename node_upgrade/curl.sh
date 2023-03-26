job_name="hello-world"
base_url="https://localhost:4646"
verify=False

# get allocations  of job
curl -s -k -X GET "${base_url}/v1/job/${job_name}/allocations" | jq '.' #| jq -r '.[] | .ID'
