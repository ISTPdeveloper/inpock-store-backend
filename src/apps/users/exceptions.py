from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:

        if isinstance(response.data, dict):
            for data_key, data_array in response.data.items():
                if not (isinstance(data_array, list) and len(data_array) < 2):
                    continue
                if hasattr(data_array[0], "title"):
                    response.data[data_key] = data_array[0].title()
    return response
