kubeconfig:
	@echo "cluster=${CLUSTER}"
	@eksctl utils write-kubeconfig --cluster "${CLUSTER}" --region "${AWS_DEFAULT_REGION}"

portforward:
	# @SVC_PORT=$(shell kubectl -n kubeflow get svc/ml-pipeline -o json | jq ".spec.ports[0].port")
	# @echo $(shell kubectl -n kubeflow get svc/ml-pipeline -o json | jq ".spec.ports[0].port")
	@kubectl port-forward -n kubeflow svc/ml-pipeline ${SVC_PORT}:$(shell kubectl -n kubeflow get svc/ml-pipeline -o json | jq ".spec.ports[0].port")

.PHONY: kubeconfig portforward
