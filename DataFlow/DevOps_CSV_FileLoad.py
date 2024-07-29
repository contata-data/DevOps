import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io.gcp.bigquery import WriteToBigQuery, BigQueryDisposition
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import GoogleCloudOptions, StandardOptions
import os 
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/Vikas Kumar/Downloads/relevate-dev-403605-340c9af01a97.json"

class SplitRow(beam.DoFn):
    def process(self, element):
        import csv
        from io import StringIO

        reader = csv.reader(StringIO(element), delimiter='|')
        for row in reader:
            #print("printing row --------------")
            #print(row)
            yield {
                'FranchiseOwner': row[0],
                'Location': row[1],
                'MonthYear': row[2],
                'FirstName': row[3],
                'LastName': row[4],
                'Address': row[5],
                'City': row[6],
                'State': row[7],
                'Zip': row[8],
                'SaleDate': row[9],
                'NetPrice': row[10],
                'Type': row[11],
                'SycleExportDate': row[12]
            }

def run():
    # Set your pipeline options
    options = PipelineOptions()
    google_cloud_options = options.view_as(GoogleCloudOptions)
    google_cloud_options.project = 'relevate-dev-403605'
    google_cloud_options.region = 'us-central1'
    google_cloud_options.job_name = 'relevate-gcs-to-bq-df-2'
    google_cloud_options.staging_location = 'gs://relevate-dev-403605-devops2207/staging'
    google_cloud_options.temp_location = 'gs://relevate-dev-403605-devops2207/temp'
    options.view_as(StandardOptions).runner = 'DataflowRunner'       #DirectRunner

    # Define the pipeline
    with beam.Pipeline(options=options) as p:
        (
            p
            | 'Read from GCS' >> ReadFromText('gs://relevate-dev-403605-devops2207/DevOps_DataFlow.csv')
            | 'Split rows' >> beam.ParDo(SplitRow())
            | 'Write to BigQuery' >> WriteToBigQuery(
                'relevate-dev-403605:RelevateSystem.DevOpsDataFlow',
                schema='FranchiseOwner:STRING, Location:STRING, MonthYear:STRING, FirstName:STRING, LastName:STRING, Address:STRING, City:STRING, State:STRING, Zip:STRING, SaleDate:STRING, NetPrice:STRING, Type:STRING, SycleExportDate:STRING',
                create_disposition=BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=BigQueryDisposition.WRITE_TRUNCATE #WRITE_APPEND
                
            )
        )

if __name__ == '__main__':
    run()