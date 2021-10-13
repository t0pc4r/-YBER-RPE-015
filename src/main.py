import argparse
import json
import .utils

from .worker_pool import WorkerPool

def get_config_from_file(config_file):
    with open(config_file, "r") as f:
        return json.loads(f.read())

def init_connector(elastic_config, rabbitmq_config, modules_config, connector_config):
    worker_pool = WorkerPool(rabbitmq_config, max_workers=connector_config["max_workers"])

    modules = []
    
    for module_config in modules_config:
        module_class = utils.get_class_from_name(module_config["name"])
        module = module_class(elastic_config, module_config, worker_pool)
        modules.append(module)
    
    for module in modules:
        module.start()
    
    for module in modules:
        module.join()
    
    worker_pool.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--elastic_config_file", required=True)
    parser.add_argument("--rabbitmq_config_file", required=True)
    parser.add_argument("--modules_config_file", required=True)
    parser.add_argument("--connector_config_file", required=True)
    args = parser.parse_args()

    elastic_config = get_config_from_file(args.elastic_config_file)
    rabbitmq_config = get_config_from_file(args.rabbitmq_config_file)
    modules_config = get_config_from_file(args.modules_config_file)
    connector_config = get_config_from_file(args.connector_config_file)