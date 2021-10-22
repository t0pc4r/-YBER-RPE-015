import argparse
import json
import utils

from worker_pool import WorkerPool

def get_config_from_file(config_file):
    with open(config_file, "r") as f:
        return json.loads(f.read())

def init_connector(elastic_config, opencti_config, modules_config, connector_config):
    worker_pool = WorkerPool(opencti_config, max_workers=connector_config["max_workers"])
    worker_pool.start()
    modules = []


    worker_pool.add_data("init_labeler.InitLabeler", "actor", {"name": "DreadRiver"})

    for module_config in modules_config:
        module_class = utils.get_class_from_name(module_config["name"])
        if module_class is None:
            print("Error, module: %s is not found" % module_config["name"])
            continue
        module = module_class(elastic_config, module_config, worker_pool)
        modules.append(module)

    for module in modules:
        print("Starting module: %s" % module)
        module.start()

    for module in modules:
        module.join()
        print("Finished module: %s" % module)

    worker_pool.join()
    print("All workers finished")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--elastic-config-file", default="configs/elastic_config.json")
    parser.add_argument("--opencti-config-file", default="configs/opencti_config.json")
    parser.add_argument("--modules-config-file", default="configs/modules_config.json")
    parser.add_argument("--connector-config-file", default="configs/connector_config.json")
    args = parser.parse_args()

    elastic_config = get_config_from_file(args.elastic_config_file)
    opencti_config = get_config_from_file(args.opencti_config_file)
    modules_config = get_config_from_file(args.modules_config_file)
    connector_config = get_config_from_file(args.connector_config_file)

    init_connector(elastic_config, opencti_config, modules_config, connector_config)
    print("Done reading")
