"""
Waypoint Migration Script!

Takes a config.yaml and calls /model/new 

Inputs:
    - File path to config.yaml
    - Proxy base url to your hosted proxy

Step 1: Reads your config.yaml
Step 2: reads `model_list` and loops through all models 
Step 3: calls `<proxy-base-url>/model/new` for each model
"""

import os
import sys

import requests
import yaml

_in_memory_os_variables = {}


def migrate_models(config_file, proxy_base_url):
    # Step 1: Read the config.yaml file
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    # Step 2: Read the model_list and loop through all models
    model_list = config.get("model_list", [])
    sys.stdout.write(" ".join(str(_output_value) for _output_value in ("model_list: ", model_list)) + "\n")
    for model in model_list:

        model_name = model.get("model_name")
        sys.stdout.write(" ".join(str(_output_value) for _output_value in ("\nAdding model: ", model_name)) + "\n")
        litellm_params = model.get("litellm_params", {})
        api_base = litellm_params.get("api_base", "")
        sys.stdout.write(
            " ".join(str(_output_value) for _output_value in ("api_base on config.yaml: ", api_base)) + "\n"
        )

        litellm_model_name = litellm_params.get("model", "") or ""
        if "vertex_ai/" in litellm_model_name:
            sys.stdout.write(
                " ".join(str(_output_value) for _output_value in ("\x1b[91m\nSkipping Vertex AI model\x1b[0m", model))
                + "\n"
            )
            continue

        for param, value in litellm_params.items():
            if isinstance(value, str) and value.startswith("os.environ/"):
                # check if value is in _in_memory_os_variables
                if value in _in_memory_os_variables:
                    new_value = _in_memory_os_variables[value]
                    sys.stdout.write(
                        " ".join(
                            str(_output_value)
                            for _output_value in (
                                "\x1b[92mAlready entered value for \x1b[0m",
                                value,
                                "\x1b[92musing \x1b[0m",
                                new_value,
                            )
                        )
                        + "\n"
                    )
                else:
                    new_value = input(f"Enter value for {value}: ")
                    _in_memory_os_variables[value] = new_value
                litellm_params[param] = new_value
        if "api_key" not in litellm_params:
            new_value = input(f"Enter api key for {model_name}: ")
            litellm_params["api_key"] = new_value

        sys.stdout.write(
            " ".join(str(_output_value) for _output_value in ("\nlitellm_params: ", litellm_params)) + "\n"
        )
        # Confirm before sending POST request
        confirm = input(
            "\033[92mDo you want to send the POST request with the above parameters? (y/n): \033[0m"
        )
        if confirm.lower() != "y":
            sys.stdout.write("Aborting POST request." + "\n")
            exit()

        # Step 3: Call <proxy-base-url>/model/new for each model
        url = f"{proxy_base_url}/model/new"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {master_key}",
        }
        data = {"model_name": model_name, "litellm_params": litellm_params}
        sys.stdout.write(" ".join(str(_output_value) for _output_value in ("POSTING data to proxy url", url)) + "\n")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code != 200:
            sys.stdout.write(f"Error: {response.status_code} - {response.text}" + "\n")
            raise Exception(f"Error: {response.status_code} - {response.text}")

        # Print the response for each model
        sys.stdout.write(
            f"Response for model '{model_name}': Status Code:{response.status_code} - {response.text}" + "\n"
        )


# Usage
config_file = "config.yaml"
proxy_base_url = "http://0.0.0.0:4000"
master_key = os.environ["WAYPOINT_MASTER_KEY"]
sys.stdout.write(f"config_file: {config_file}" + "\n")
sys.stdout.write(f"proxy_base_url: {proxy_base_url}" + "\n")
migrate_models(config_file, proxy_base_url)
