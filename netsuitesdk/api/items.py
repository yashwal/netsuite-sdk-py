from .base import ApiBase
from netsuitesdk.internal.utils import PaginatedSearch
import logging
from collections import OrderedDict

logger = logging.getLogger(__name__)

class Items(ApiBase):

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='Item')

    def get_all_generator(self, is_inactive=False):
        # Get Only Active Items using SearchBooleanField
        record_type_search_field = self.ns_client.SearchBooleanField(searchValue=is_inactive)
        basic_search = self.ns_client.basic_search_factory('Item', isInactive=record_type_search_field)

        paginated_search = PaginatedSearch(
            client=self.ns_client,
            type_name='Item',
            basic_search=basic_search,
            pageSize=20
        )

        return self._paginated_search_generator(paginated_search=paginated_search)
    def post(self, data) -> OrderedDict:
        assert data['externalId'], 'missing external id'
        file = self.ns_client.Items()

        if 'name' in data:
            file['name'] = data['name']

        if 'externalId' in data:
            file['externalId'] = data['externalId']

        if 'content' in data:
            file['content'] = data['content']

        if 'mediaType' in data:
            file['mediaType'] = data['mediaType']

        logger.debug('able to create file = %s', file)
        res = self.ns_client.upsert(file)
        return self._serialize(res)
