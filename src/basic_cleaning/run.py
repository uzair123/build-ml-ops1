#!/usr/bin/env python
"""
example of MLflow using wb
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################

    run = wandb.init(project="nyc_airbnb", group="eda", save_code=True)
    local_path = wandb.use_artifact("sample.csv:latest").file()
    df = pd.read_csv(local_path)

    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])
    #clean_sample.csv 
    df.to_csv("clean_sample.csv", index=False)
                  
    print(args.output_artifact)
    artifact = wandb.Artifact(args.output_artifact,type=args.output_type,description=args.output_description)
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)


                  
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help= "its a to do",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="todo",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="todo",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="todo",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="its a to do",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="todo",
        required=True
    )


    args = parser.parse_args()

    go(args)
