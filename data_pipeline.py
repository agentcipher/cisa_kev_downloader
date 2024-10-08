import dlt
from dynaconf import Dynaconf
from dlt.sources.rest_api import rest_api_source, RESTAPIConfig
from typing import Dict, Any, Iterator
from utils import load_model_class
import traceback
from loguru import logger

# Load the configuration
settings = Dynaconf(
    settings_files=['config.yaml'],
    environments=True,
    load_dotenv=True,
)

# Create a DLT pipeline
@dlt.source(name=settings.source.name)
def data_source():
    # Define the source using RESTAPIConfig
    source = rest_api_source(
        RESTAPIConfig(
            client=settings.client,
            resources=settings.resources,
        )
    )

    # Dynamically load the data model
    columns = load_model_class(settings.models.model)

    # Define the DLT resource to process the data
    @dlt.resource(name=settings.pipeline.dataset_name, columns=columns, **settings.resource_defaults)
    def data_resource() -> Iterator[Dict[str, Any]]:
        # The resource name is now a list item, so we need to access it differently
        resource_name = settings.resources[0].name

        try:
            # Get the raw data from the API
            raw_data = source.resources[resource_name]

            # Load the correct class function
            response_class = load_model_class(settings.models.parse_data_function)
            response_obj = response_class(data=list(raw_data))

            data_items = list(response_obj.get_data())

            for data_item in data_items:
                yield data_item

        except Exception as e:
            logger.error(f'Error in data_resource: {e}')
            logger.error(traceback.format_exc())  # Logs the full traceback
            raise

    return data_resource

def run_pipeline():
    # Create the DLT pipeline
    pipeline = dlt.pipeline(
        pipeline_name=settings.pipeline.name,
        destination=settings.pipeline.destination,
        dataset_name=settings.pipeline.dataset_name
    )

    # Get the data source
    source = data_source()

    # Run the pipeline with the resource data
    load_info = pipeline.run(source)

    # Get row counts from the last pipeline trace
    row_counts = pipeline.last_trace.last_normalize_info

    print(row_counts)
    print("------")
    print(load_info)


# Add this to your main block
if __name__ == "__main__":
    run_pipeline()
