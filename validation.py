from marshmallow import Schema, fields


class SasRequestSchema(Schema):
    """
    Parameters:
     - container_name (str)
     - blob_name (str)
    """

    container_name = fields.Str(required=True)
    blob_name = fields.Str(required=True)


class ListRequestSchema(Schema):
    """
        Parameters:
         - container_name (str)
        """

    container_name = fields.Str(required=True)


class DeleteRequestSchema(Schema):
    """
        Parameters:
         - container_name (str)
         - blob_name (str)
        """

    container_name = fields.Str(required=True)
    blob_name = fields.Str(required=True)
