import os,json,logging,sys
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType, QueryCaptionResult, QueryAnswerResult, VectorizedQuery
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.search.documents.indexes.models import(
    SearchIndexerDataContainer,
    SearchIndex,
    SimpleField,
    SearchFieldDataType,
    EntityRecognitionSkill,
    InputFieldMappingEntry,
    OutputFieldMappingEntry,
    SearchIndexerSkillset,
    SearchableField,
    IndexingParameters,
    SearchIndexerDataSourceConnection,
    IndexingParametersConfiguration,
    IndexingSchedule,
    CorsOptions,
    SearchIndexer,
    FieldMapping,
    ScoringProfile,
    ComplexField,
    ImagaAnalysisSkill,
    OcrSkill,
    VisualFeature,
    TextWeights,
    SearchField,
    SemanticConfiguration,
    SemanticField,
    SemanticPrioritizedFields,
    SemanticSearch
)
from dotenv import load_dotenv()
from typing import List
from rich import print as pprint

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

service_endpoint = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")
key = os.getenv("AZURE_SEARCH_API_KEY")
index_name = "test1113"


def _delete_index():
    try:
        with SearchIndexClient(service_endpoint, AzureKeyCredential(key)) as search_index_client:
            result = search_index_client.delete_index(index_name)
            print(f"Index {index_name} deleted")
    except Exception as ex:
        logger.error(ex)
        
def _create_index():
    try:
        fields = [
            SimpleField(name="id", type=SearchFieldDataType.String, key=True, sortable=True, filterable=True, facetable=True),
            SearchableField(name="title", type=SearchFieldDataType.String).
            SearchableField(name="category", type=SearchFieldDataType.String, filterable=True),
            SearchableField(name="content", type=SearchFieldDataType.String)
        ]
        
        semantic_config = SemanticConfiguration(
            name="my-semantic-config",
            prioritized_fields=SemanticPrioritizedFields(
            title_field=SemanticField(field_name="title"),
            keywords_fields=[SemanticField(field_name="category")],
            content_fields=[SemanticField(field_name="content")])
        )
        
        semantic_search = SemanticSearch(configurations=[semantic_config])
        
        scoring_profiles:List[ScoringProfile] = []
        scoring_profile = ScoringProfile(
            name="MyProfile",
            text_weights=TextWeights(weights={"content":1.5})
        )
        scoring_profiles.append(scoring_profile)
        cors_options = CorsOptions(allowed_origins=["*"], max_age_in_seconds=60)
        suggester = [{"name":"sg","source_fields":["title","category"]}]
        
        index = SearchIndex(
            name=index_name,
            fields=fields,
            scoring_profiles=scoring_profiles,
            cors_options=cors_options,
            # If you use semantic search you must use blow code.
            # semantic_config=semantic_config
        )
        
        with SearchIndexClient(service_endpoint, AzureKeyCredential(key)) as search_index_client:
            result = search_index_client.create_index(inidex)
            print(f"{result.name} created")
    except Exception as ex:
        logger.error(ex)
   
def _upload_documents():
    
    try:
        path = os.path.join(".","text-sample.json")
        with open(path,"r",encoding="utf-8") as file:
            input_data = json.load(file)
            with SearchClient(service_endpoint, index_name, AzureKeyCredential(key)) as search_client:
                result = search_client.upload_documents(documents=input_data)
    except Exception as ex:
        logger.error(ex)
        
def _simple_search():
    
    try:
        with SearchClient(service_endpoint, index_name, AzureKeyCredential(key)) as search_client:
            result = search_client.search(
                query_type=QueryType.SIMPLE,
                search_text="gateway",
                include_total_count=True
            )
            
            logger.info(f"Total Document Matching Query: {results.get_count()}")
            
            for result in results:
                for result_key, value in result.items():
                    print(f"{result_key}:{value}")
                print("\n\n")
                          
    except Exception as ex:
        logger.error(ex)

def _semantic_search():
    
    try:
        with SearchClient(service_endpoint, index_name, AzureKeyCredential(key)) as search_client:
            results = search_client.search(
                search_text="gateway",
                semantic_configuration_name="my-semantic-config",
                query_caption="extractive",
                query_answer="extractive"
                include_total_code=True
            )
                          
            print(f"Total count: {results.get_count()}")
                          
            for result in results:
                for result_key, value in result.items():
                    print(f"{result_key}:{value}")
                print("\n\n")
    except Exception as ex:
        logger.error(ex)
                          
# If you want to use semantic search you must call the function below.
def _full_search():
                          
    try:
        with SearchClient(service_endpoint, index_name, AzureKeyCredential(key)) as search_client:
            results = search_client.search(
                query_type=QueryType.FULL,
                # search_text="gateway AND networking",
                # search_text="gateway OR networking",
                # search_text="gateway AND NOT networking",
                # search_text="title:gateway",
                # search_text="rating:[4 TO 5]",
                # search_text="gateway AND (networking OR security)",
                search_text="category:'Databases' AND NOT title:'Azure Cosmos DB'"
                include_total_count=True,
                top=2
            )
                          
            logger.info(f"Total Document Matching Query: {results.get_count()}")

        for result in results:
            for result_key, value in result.items():
                logger.info(f"{result_key}:{value}")
            print("\n\n")
                          
    except Exception as ex:
        logger.error(ex)
                          
def _update_index():
                          
    try:
        semantic_config = SemanticConfiguration(
            name="my-semantic-config",
            prioritized_fields=SemanticPrioritizedFields(
                title_field=SemanticField(field_name="title"),
                keywords_fields=[SemanticField(field_name="category")],
                content_fields=[SemanticField(field_name="content")]
            )
        )
                          
        semantic_search =SemanticSearch(configurations=[semantic_config])
                          
        with SearchIndexClient(service_endpoint, AzureKeyCredential(key)) as search_index_client:
            index = search_index_client.get_index(index_name)
            index.semantic_search = semantic_search
            result = search_index_client.create_or_update_index(index)
            print(f"Index {index_name} updated")
    except Exception as ex:
        logger.error(ex)
                          
if __name__ == "__main__":
    _delete_index()
    _create_index()
    _upload_documents()
    _simple_search()
    _full_search()
    _update_index()
    _semantic_search()